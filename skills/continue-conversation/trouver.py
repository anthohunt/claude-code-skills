#!/usr/bin/env python3
"""Retrouver et relire une conversation Claude Code crashée.

  trouver.py chercher "phrase 1" ["phrase 2" ...] [--heures 48]
      Cherche les transcriptions (*.jsonl) contenant TOUTES les phrases dans les dossiers
      ~/.claude*/projects de cet ordinateur, puis sur les autres machines déclarées dans
      CONTINUE_MACHINES. La session courante est exclue.
      Affiche : machine, date de modif, taille, chemin.

  trouver.py relire CHEMIN [--machine local|<alias>] [--n 60]
      Rapatrie la transcription si besoin et affiche les N derniers messages
      utilisateur/assistant (texte seul), triés par horodatage.

Autres machines (facultatif) : variable d'environnement CONTINUE_MACHINES, une liste séparée par des
virgules de « alias_ssh:systeme » avec systeme = linux (défaut) ou windows. Exemple :
  CONTINUE_MACHINES="serveur:linux,portable:windows"
Les alias sont ceux de ~/.ssh/config (connexion par clé, sans mot de passe).
"""
import argparse, glob, json, os, shlex, subprocess, sys, tempfile

LOCAL_GLOB = os.path.expanduser("~/.claude*/projects")
SCRATCH = tempfile.gettempdir()


def machines():
    out = []
    for item in filter(None, (x.strip() for x in os.environ.get("CONTINUE_MACHINES", "").split(","))):
        alias, _, systeme = item.partition(":")
        out.append((alias, systeme or "linux"))
    return out


def ssh(alias, cmd, timeout=120):
    try:
        r = subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=8", alias, cmd],
                           capture_output=True, text=True, errors="replace", timeout=timeout)
        return r.returncode, r.stdout
    except subprocess.TimeoutExpired:
        return 124, ""


def powershell(alias, script, timeout=300):
    """Le shell SSH d une machine Windows est cmd : passer par powershell -EncodedCommand (UTF-16LE base64)."""
    import base64
    enc = base64.b64encode(("[Console]::OutputEncoding=[Text.Encoding]::UTF8;" + script).encode("utf-16-le")).decode()
    return ssh(alias, f"powershell -NoProfile -NonInteractive -EncodedCommand {enc}", timeout)


def joignable(alias):
    return ssh(alias, "echo ok", 20)[1].strip() == "ok"


def session_courante():
    """sessionId de la session Claude qui lance ce script (remonte les processus parents)."""
    pid = os.getppid()
    while pid > 1:
        for f in glob.glob(os.path.expanduser(f"~/.claude*/sessions/{pid}.json")):
            try:
                return json.load(open(f)).get("sessionId", "")
            except ValueError:
                pass
        try:
            pid = int(open(f"/proc/{pid}/stat").read().rsplit(")", 1)[1].split()[1])
        except (OSError, IndexError, ValueError):
            break
    return os.environ.get("CLAUDE_SESSION_ID", "")


def chercher(phrases, heures):
    mins = int(heures * 60)
    greps = " | ".join(f"xargs -r grep -lF -e {shlex.quote(p)}" for p in phrases)
    bash = (f"find {{racines}} -name '*.jsonl' -mmin -{mins} -not -path '*/subagents/*' 2>/dev/null"
            f" | {greps} 2>/dev/null | xargs -r ls -lt --time-style=+%Y-%m-%d_%H:%M 2>/dev/null")
    courant = session_courante()
    # Cet ordinateur
    out = subprocess.run(["bash", "-c", bash.format(racines=LOCAL_GLOB)], capture_output=True, text=True).stdout
    for l in out.splitlines():
        if courant and courant in l:
            continue
        print("local ", l)
    # Autres machines
    for alias, systeme in machines():
        if not joignable(alias):
            print(f"{alias} injoignable")
        elif systeme == "windows":
            conds = " -and ".join(f"(Select-String -LiteralPath $_.FullName -SimpleMatch -Quiet -Pattern '{p.replace(chr(39), chr(39)*2)}')" for p in phrases)
            ps = ("Get-ChildItem $env:USERPROFILE -Directory -Filter '.claude*' -Force | ForEach-Object { "
                  "Get-ChildItem (Join-Path $_.FullName 'projects') -Recurse -Filter *.jsonl -ErrorAction SilentlyContinue } | "
                  f"Where-Object {{ $_.LastWriteTime -gt (Get-Date).AddHours(-{heures}) -and $_.FullName -notmatch 'subagents' }} | "
                  f"Where-Object {{ {conds} }} | Sort-Object LastWriteTime -Descending | "
                  "ForEach-Object { '{0:yyyy-MM-dd_HH:mm} {1} {2}' -f $_.LastWriteTime, $_.Length, $_.FullName }")
            print("".join(f"{alias} " + l + "\n" for l in powershell(alias, ps)[1].splitlines()), end="")
        else:
            print("".join(f"{alias} " + l + "\n" for l in ssh(alias, bash.format(racines="~/.claude*/projects"))[1].splitlines()), end="")


def relire(chemin, machine, n):
    if machine != "local":
        dest = os.path.join(SCRATCH, "conv-" + os.path.basename(chemin.replace("\\", "/")))
        src = chemin.replace("\\", "/")
        if subprocess.run(["scp", "-q", "-o", "ConnectTimeout=10", f"{machine}:{src}", dest]).returncode:
            sys.exit(f"échec scp depuis {machine}")
        chemin = dest
        print(f"(copie locale : {chemin})")
    msgs = []
    for l in open(chemin, encoding="utf-8", errors="replace"):
        try:
            d = json.loads(l)
        except ValueError:
            continue
        if d.get("type") not in ("user", "assistant") or d.get("isSidechain"):
            continue
        c = d.get("message", {}).get("content")
        t = c if isinstance(c, str) else " ".join(x.get("text", "") for x in c or [] if x.get("type") == "text")
        if t.strip() and not t.lstrip().startswith("<"):
            msgs.append((d.get("timestamp", "")[:19], d["type"], d.get("cwd", ""), t))
    msgs.sort()
    if msgs:
        print(f"cwd : {msgs[-1][2]} · {len(msgs)} messages")
    for ts, ty, _, t in msgs[-n:]:
        print(f"\n## {ts}Z {'UTILISATEUR' if ty == 'user' else 'AGENT'}\n{t[:3000]}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    s = p.add_subparsers(dest="cmd", required=True)
    a = s.add_parser("chercher"); a.add_argument("phrases", nargs="+"); a.add_argument("--heures", type=float, default=48)
    b = s.add_parser("relire"); b.add_argument("chemin"); b.add_argument("--machine", default="local"); b.add_argument("--n", type=int, default=60)
    x = p.parse_args()
    chercher(x.phrases, x.heures) if x.cmd == "chercher" else relire(x.chemin, x.machine, x.n)
