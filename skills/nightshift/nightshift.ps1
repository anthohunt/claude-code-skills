# nightshift.ps1 - shared coordinator for overnight agent tasks
# ASCII-only (PS 5.1 compatible). All registry access guarded by a named mutex.
#
# Verbs:
#   register -Desc "..." [-Agent "..."]  -> prints the new task id, starts watchdog
#   heartbeat -Id <id>                   -> refresh proof-of-life timestamp
#   done -Id <id>                        -> mark task completed
#   fail -Id <id>                        -> mark task failed/abandoned
#   check -Id <id>                       -> prints SHUTDOWN (and arms shutdown) or WAIT
#   status                               -> prints the registry as a table
#   watchdog                             -> internal: dead-man's-switch loop (do not call by hand)

param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('register', 'heartbeat', 'done', 'fail', 'check', 'status', 'watchdog')]
    [string]$Action,
    [string]$Id,
    [string]$Desc,
    [string]$Agent = ''
)

$ErrorActionPreference = 'Stop'

$Root        = Join-Path $env:USERPROFILE '.claude\nightshift'
$RegistryPath = Join-Path $Root 'registry.json'
$WatchdogLock = Join-Path $Root 'watchdog.lock'
$LogPath     = Join-Path $Root 'watchdog.log'
$ScriptPath  = $MyInvocation.MyCommand.Path

$StaleMinutes   = 30   # heartbeat older than this => agent presumed dead
$PollSeconds    = 300  # watchdog poll interval (5 min)
$ShutdownDelay  = 60   # grace period before the machine powers off (cancel: shutdown /a)

function Ensure-Root {
    if (-not (Test-Path $Root)) { New-Item -ItemType Directory -Path $Root -Force | Out-Null }
}

function Now-Iso { (Get-Date).ToString('s') }

function Log-Line {
    # Append a timestamped line to watchdog.log. Best-effort: never throws.
    param([string]$Msg)
    try {
        $line = '{0}  [pid {1}]  {2}' -f (Get-Date).ToString('s'), $PID, $Msg
        Add-Content -Path $LogPath -Value $line -Encoding ASCII -ErrorAction SilentlyContinue
    } catch { }
}

function With-Lock {
    param([scriptblock]$Body)
    $mutex = New-Object System.Threading.Mutex($false, 'Global\nightshift_registry')
    [void]$mutex.WaitOne()
    try { & $Body } finally { $mutex.ReleaseMutex(); $mutex.Dispose() }
}

function Read-Registry {
    if (-not (Test-Path $RegistryPath)) { return @() }
    $raw = Get-Content -Raw -Path $RegistryPath -ErrorAction SilentlyContinue
    if ([string]::IsNullOrWhiteSpace($raw)) { return @() }
    $data = $raw | ConvertFrom-Json
    if ($null -eq $data) { return @() }
    return @($data)
}

function Write-Registry {
    param($Entries)
    $json = ConvertTo-Json @($Entries) -Depth 6
    Set-Content -Path $RegistryPath -Value $json -Encoding ASCII
}

function Is-Alive {
    param($Entry)
    if ($Entry.status -ne 'running') { return $false }
    $hb = [datetime]$Entry.heartbeat
    return ((Get-Date) - $hb).TotalMinutes -lt $StaleMinutes
}

function Arm-Shutdown {
    # Idempotent: a second arm while one is pending just errors out harmlessly.
    # Set NIGHTSHIFT_DRYRUN=1 to test the protocol logic without ever powering off.
    if ($env:NIGHTSHIFT_DRYRUN -eq '1') {
        Log-Line 'ARM (DRYRUN): would power off'
        Write-Output 'DRYRUN: would arm shutdown'
        return
    }
    Log-Line ("ARM: running shutdown.exe /s /f /t {0}" -f $ShutdownDelay)
    # Primary path: shutdown.exe. Capture exit code + stderr instead of swallowing them.
    # /f forces blocking apps (terminals, node, unsaved editors) to close. Without it,
    # Windows returns exit 0 but silently aborts the shutdown when an app vetoes it
    # (root cause of the 2026-06-19 "armed but never powered off" bug).
    $rc = $null
    try {
        $err = & shutdown.exe /s /f /t $ShutdownDelay /c 'nightshift: toutes les taches sont terminees' 2>&1
        $rc = $LASTEXITCODE
        if ($err) { Log-Line ("shutdown.exe output: " + (($err | Out-String).Trim())) }
        Log-Line ("shutdown.exe exit code: " + $rc)
    } catch {
        Log-Line ("shutdown.exe threw: " + $_.Exception.Message)
    }
    if ($rc -eq 0)    { Log-Line 'ARM OK: power off scheduled via shutdown.exe'; return }
    if ($rc -eq 1190) { Log-Line 'ARM OK: a shutdown was already scheduled (1190)'; return }

    # Fallback: shutdown.exe failed (privilege/session/pending-update). Try Stop-Computer.
    Log-Line ("ARM: shutdown.exe failed (rc=" + $rc + ") -> fallback Stop-Computer -Force")
    try {
        Stop-Computer -Force -ErrorAction Stop
        Log-Line 'ARM OK: Stop-Computer issued'
    } catch {
        Log-Line ("FALLBACK FAILED: Stop-Computer threw: " + $_.Exception.Message)
    }
}

function Watchdog-Running {
    if (-not (Test-Path $WatchdogLock)) { return $false }
    $pidTxt = (Get-Content -Raw -Path $WatchdogLock -ErrorAction SilentlyContinue).Trim()
    if (-not $pidTxt) { return $false }
    $proc = Get-Process -Id ([int]$pidTxt) -ErrorAction SilentlyContinue
    return ($null -ne $proc)
}

function Start-Watchdog {
    if (Watchdog-Running) { return }
    Start-Process -FilePath 'powershell.exe' `
        -ArgumentList @('-NoProfile', '-WindowStyle', 'Hidden', '-File', $ScriptPath, '-Action', 'watchdog') `
        -WindowStyle Hidden | Out-Null
}

switch ($Action) {

    'register' {
        if (-not $Desc) { throw 'register requires -Desc' }
        Ensure-Root
        $newId = [guid]::NewGuid().ToString()
        With-Lock {
            $entries = @(Read-Registry)
            $anyAlive = $false
            foreach ($e in $entries) { if (Is-Alive $e) { $anyAlive = $true; break } }
            if (-not $anyAlive -and $entries.Count -gt 0) {
                # Previous batch fully resolved -> archive and start a fresh night.
                $stamp = (Get-Date).ToString('yyyyMMdd-HHmmss')
                $archive = Join-Path $Root ("registry.$stamp.json")
                Copy-Item -Path $RegistryPath -Destination $archive -ErrorAction SilentlyContinue
                $entries = @()
            }
            $entry = [pscustomobject]@{
                id          = $newId
                description = $Desc
                agent       = $Agent
                status      = 'running'
                started     = (Now-Iso)
                heartbeat   = (Now-Iso)
            }
            $entries += $entry
            Write-Registry $entries
        }
        Start-Watchdog
        Write-Output $newId
    }

    'heartbeat' {
        if (-not $Id) { throw 'heartbeat requires -Id' }
        With-Lock {
            $entries = @(Read-Registry)
            foreach ($e in $entries) { if ($e.id -eq $Id) { $e.heartbeat = (Now-Iso) } }
            Write-Registry $entries
        }
    }

    'done' {
        if (-not $Id) { throw 'done requires -Id' }
        With-Lock {
            $entries = @(Read-Registry)
            foreach ($e in $entries) { if ($e.id -eq $Id) { $e.status = 'done'; $e.heartbeat = (Now-Iso) } }
            Write-Registry $entries
        }
    }

    'fail' {
        if (-not $Id) { throw 'fail requires -Id' }
        With-Lock {
            $entries = @(Read-Registry)
            foreach ($e in $entries) { if ($e.id -eq $Id) { $e.status = 'failed'; $e.heartbeat = (Now-Iso) } }
            Write-Registry $entries
        }
    }

    'check' {
        if (-not $Id) { throw 'check requires -Id' }
        $result = 'WAIT'
        With-Lock {
            $entries = @(Read-Registry)
            $othersAlive = $false
            foreach ($e in $entries) {
                if ($e.id -eq $Id) { continue }
                if (Is-Alive $e) { $othersAlive = $true; break }
            }
            if (-not $othersAlive) { $script:result = 'SHUTDOWN' } else { $script:result = 'WAIT' }
        }
        if ($result -eq 'SHUTDOWN') { Arm-Shutdown }
        Write-Output $result
    }

    'status' {
        $entries = @(Read-Registry)
        if ($entries.Count -eq 0) { Write-Output 'registry empty'; break }
        $entries | ForEach-Object {
            $alive = if (Is-Alive $_) { 'ALIVE' } else { 'dead/done' }
            '{0}  {1,-9} {2,-9} hb={3}  {4}' -f $_.id.Substring(0,8), $_.status, $alive, $_.heartbeat, $_.description
        } | Write-Output
    }

    'watchdog' {
        # Singleton dead-man's switch. Exits once it has armed shutdown or has nothing left to guard.
        Ensure-Root
        Set-Content -Path $WatchdogLock -Value $PID -Encoding ASCII
        Log-Line ("WATCHDOG start (poll={0}s, stale={1}min)" -f $PollSeconds, $StaleMinutes)
        while ($true) {
            Start-Sleep -Seconds $PollSeconds
            $entries = @(Read-Registry)
            if ($entries.Count -eq 0) { Log-Line 'WATCHDOG: registry empty -> exit'; break }
            $anyAlive = $false
            foreach ($e in $entries) { if (Is-Alive $e) { $anyAlive = $true; break } }
            $alive = @($entries | Where-Object { Is-Alive $_ }).Count
            Log-Line ("WATCHDOG poll: {0} entries, {1} alive" -f $entries.Count, $alive)
            if (-not $anyAlive) { Log-Line 'WATCHDOG: no task alive -> arming shutdown'; Arm-Shutdown; break }
        }
        Log-Line 'WATCHDOG exit'
        Remove-Item -Path $WatchdogLock -ErrorAction SilentlyContinue
    }
}
