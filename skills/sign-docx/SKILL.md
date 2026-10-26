---
name: sign-docx
description: Use when the user needs to sign a .docx (attestation, courrier, mandat…) and produce a signed PDF. Orchestrates: open docx in Word → point to the signature image → wait for the user to insert it and save → convert docx to PDF. Trigger phrases: "il faut signer X", "signer cette attestation", "signe ce document", "j'ai un docx à signer".
---

# sign-docx — workflow de signature interactif (Windows + Word)

## Pourquoi un skill plutôt qu'un script

La signature est un acte personnel — l'utilisateur **doit voir le document avant de le signer** (relecture = sécurité juridique). On n'overlay PAS l'image programmatiquement (incompatible avec la review humaine, casse souvent la mise en page).

Le rôle de Claude : éliminer toutes les frictions techniques **autour** du moment de signature.

## Étapes (à suivre exactement, dans cet ordre)

### 1. Ouvrir le .docx dans Word
```bash
powershell -Command "Start-Process '<chemin absolu du .docx>'"
```
Word lance et ouvre le doc. L’utilisateur peut commencer à relire.

### 2. Mettre la signature à disposition

L'image de signature (PNG sur fond transparent ou blanc, recadrée) est un fichier que l'utilisateur fournit une fois pour toutes : son chemin se règle dans la variable `SIGNATURE_PNG` (ex. `%USERPROFILE%\\Documents\\signature.png`). Vérifier qu'elle existe ; sinon, demander son emplacement une fois (une question).

Dire à l'utilisateur où se trouve l'image, pour qu'il la prenne dans Word (Insertion > Image).

### 3. Attendre le signal de l’utilisateur

L’utilisateur :
- insère l'image signature dans Word (Insertion > Image > depuis Downloads),
- relit le document,
- sauvegarde (Ctrl+S),
- dit **"signé"** (ou variante : "c'est signé", "ok signé", "go").

**Ne pas** convertir en PDF avant ce signal — Word a un lock sur le fichier tant qu'il n'a pas été enregistré, et le .docx n'a pas la signature embarquée tant qu'il n'a pas sauvegardé.

### 4. Convertir le .docx en PDF via Word COM

Le .docx peut encore être ouvert dans Word — utiliser `ReadOnly=true` lors de l'open COM pour éviter le conflit de lock.

```powershell
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$doc = $word.Documents.Open($Src, $false, $true)  # ReadOnly=true
# wdFormatPDF = 17
$doc.SaveAs([ref]$Dst, [ref]17)
$doc.Close($false)
$word.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
```

Le PDF est généré au même endroit que le .docx (changer l'extension) sauf demande explicite de l’utilisateur.

### 5. Confirmer + utiliser le PDF

Annoncer brièvement le chemin du PDF + lancer l'étape suivante prévue (dépôt sur un portail, envoi par mail — après validation, cf. `confirm-external-send`). Ne pas se réjouir sur la signature elle-même — c'est juste une étape technique.

## Anti-context (ne pas refaire)

- ❌ **Ne PAS** insérer la signature image programmatiquement dans le .docx via python-docx / XML — incompatible avec le contrôle visuel de l’utilisateur et casse la mise en page.
- ❌ **Ne PAS** convertir en PDF avant que l'utilisateur dise "signé" — le doc serait converti sans la signature.
- ❌ **Ne PAS** utiliser `docx2pdf` package python — moins fiable que Word COM (rend mal certaines polices, échoue si Office n'est pas installé en mode silencieux).
- ❌ **Ne PAS** sauter l'étape 2 même si le .docx n'a apparemment pas besoin de signature visible — l’utilisateur peut décider de signer même un doc qui ne le demande pas explicitement (ex: tampon visuel sur courrier).

## Variantes connues

- **Word déjà ouvert sur le doc** : pas de souci, l'étape 4 utilise ReadOnly=true. Si l’utilisateur édite encore quand on lance l'étape 4, la dernière sauvegarde est ce qui sera converti.
- **Pas de Word installé** : fallback LibreOffice headless (`soffice --headless --convert-to pdf <docx>`) mais perte de fidélité possible. Word préféré.
- **Doc avec champs interactifs (form fillable PDF)** : si le besoin est un PDF Adobe signable (Fill & Sign), c'est un autre workflow — préférer la signature électronique native du PDF. Ne pas confondre avec ce skill (qui gère docx → signature image manuelle → PDF figé).
