---
name: transcribe-audio
description: Transcribe audio OR video files to text with high quality, and OPTIONALLY produce a multi-agent synthesis (summary) of the content. Use when the user asks to transcribe audio (m4a, mp3, wav, ogg) or video (mp4, mkv, mov, etc.), dicter un audio/vidéo, "transcris", "retranscription", "speech to text", "transcript + synthèse", "résume cet audio", or downloads a media file from Drive or mail to get a text transcript. Two backends: faster-whisper large-v3 local on CUDA (default, offline), OR Groq Whisper API (cloud, ultra-fast, free) when the GPU is throttled or you want speed. For video, always extract audio with ffmpeg first. Synthesis is opt-in (raw transcript stays the default) and uses a multi-agent ensemble + consolidation + anti-fabrication verification.
---

# Transcribe Audio

## Deux livrables : brut (défaut) + synthèse (option)

Ce skill produit **toujours** le transcript brut (`.txt`). La **synthèse est opt-in** :

| L'utilisateur demande… | Livrable |
|------------------------|----------|
| « transcris », « retranscription », rien de plus | transcript brut `.txt` **uniquement** (défaut, rétrocompatible) |
| « transcript + synthèse », « résume », « fais-moi le topo de cet audio », passe l'arg `synthese` | transcript brut `.txt` **+** synthèse `.md` |

Workflow global : **transcrire d'abord** (sections ci-dessous) → si synthèse demandée, enchaîner la section **« Synthèse multi-agents »** plus bas.

> Pour un **compte-rendu de réunion** formaté (décisions / actions / suspens, propositions tâches / notes / e-mail), le skill dédié reste `analyse-reunion`. Ce skill-ci fait une synthèse **générique** qui s'adapte au type de contenu (réunion, cours, note vocale, interview). Si l'audio est clairement une réunion ET que l'utilisateur veut le format CR + next steps, proposer plutôt `analyse-reunion`.

## Backend choice — Groq (cloud) vs faster-whisper (local)

| Situation | Backend |
|-----------|---------|
| Pas de GPU, GPU bridé, ou on veut juste la vitesse | **Groq API** (52 min → 31 s) |
| Hors-ligne / pas de réseau / confidentialité stricte | faster-whisper local |
| Fichier > ~40 Mo après recompression mono 40k | local (ou chunker pour Groq) |

Groq = défaut quand on a le réseau et que la vitesse compte. Local = fallback offline.

## Video → audio first (ffmpeg)

Toujours extraire l'audio AVANT de transcrire une vidéo (mp4/mkv/mov). Mono bas débit = idéal pour Whisper et reste sous la limite Groq :

```bash
ffmpeg -y -i "input.mp4" -vn -ac 1 -b:a 40k "output.mp3" -loglevel error
ffprobe -v error -show_entries format=duration -of csv=p=0 "output.mp3"   # durée
```
40 kbps mono ≈ 0.3 Mo/min → 52 min ≈ 15 Mo, sous la limite free tier ~25-40 Mo.

## Mode Groq (cloud, ultra-rapide, gratuit)

La clé se lit dans la variable d'environnement `GROQ_API_KEY` (ou un fichier `.env` **hors dépôt**, ex. `~/.config/groq/.env`, jamais dans le dossier du skill). Jamais de clé écrite dans un fichier partagé. Si 401 → demander à l'utilisateur une clé à jour (console.groq.com/keys).

```bash
# GROQ_API_KEY doit être défini dans l'environnement
curl -s -X POST "https://api.groq.com/openai/v1/audio/transcriptions" \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -F "file=@output.mp3" \
  -F "model=whisper-large-v3" \
  -F "language=fr" -F "temperature=0" \
  -F "response_format=verbose_json" \
  -o "out.groq.json" -w "HTTP %{http_code} in %{time_total}s\n"

# Extraire le .txt propre
python3 -c "import json;d=json.load(open('out.groq.json',encoding='utf-8'));open('out.txt','w',encoding='utf-8').write(d['text'].strip())"
```

- `model=whisper-large-v3` qualité max FR ; `whisper-large-v3-turbo` si + rapide.
- `verbose_json` donne `segments` avec timestamps si besoin de sous-titres.
- Free tier : 7200 s/h, 2000 req/jour, 0 €.

## Why faster-whisper over openai-whisper

- **Same model weights** as openai-whisper large-v3 → identical transcription quality
- **4-8× faster on GPU**: CTranslate2 backend keeps GPU in P0 state; openai-whisper stays in P4 because of CPU overhead between kernels
- **Lower VRAM**: ~4-5 GB vs ~11-12 GB for openai-whisper large-v3
- Installation : `pip install faster-whisper` (vérifier : `python3 -c "import faster_whisper"`)

**Don't use `python -m whisper` (openai-whisper) unless explicitly requested.** It wastes time and GPU.

## Default pipeline (French, high quality)

```bash
# 1. Audio path
AUDIO="$TMPDIR/source_audio.m4a"
OUT_DIR="$TMPDIR/whisper_out"
mkdir -p "$OUT_DIR"

# 2. Transcribe — faster-whisper large-v3 on CUDA, FR, beam_size=5
python -c "
from faster_whisper import WhisperModel
model = WhisperModel('large-v3', device='cuda', compute_type='float16')
segments, info = model.transcribe(r'$AUDIO', language='fr', beam_size=5, vad_filter=True)
import os
base = os.path.splitext(os.path.basename(r'$AUDIO'))[0]
with open(r'$OUT_DIR/' + base + '.txt', 'w', encoding='utf-8') as f:
    for s in segments:
        f.write(s.text.strip() + '\n')
print('done:', r'$OUT_DIR/' + base + '.txt')
"
```

Key settings:
- `compute_type='float16'` on a recent NVIDIA GPU — fastest without quality loss. Use `'int8_float16'` if VRAM-constrained.
- `beam_size=5` — matches openai-whisper default, best quality. Drop to 1 only if speed > quality.
- `vad_filter=True` — skips silence, improves speed and avoids hallucinations in silent segments.
- `language='fr'` explicit — skips auto-detect and avoids mis-detection on short intros.

## Récupérer un fichier depuis Google Drive (motif récurrent)

Avec [`gws`](https://github.com/googleworkspace/cli) (CLI Google Workspace) connecté au compte :

```bash
# 1. Lister le dossier pour obtenir l'identifiant du fichier
gws drive files list --params '{"q":"'\''<FOLDER_ID>'\'' in parents and trashed = false","fields":"files(id,name,size)"}'

# 2. Télécharger
gws drive files get --params '{"fileId":"<FILE_ID>","alt":"media"}' --output "$TMPDIR/source_audio.m4a"

# 3. Transcrire (voir plus haut), puis ranger le .txt à l'endroit voulu

# 4. Nettoyer
rm -f "$TMPDIR/source_audio.m4a"
rm -rf "$TMPDIR/whisper_out"
```

## Model choice

| Need | Model |
|------|-------|
| High quality FR/EN (default) | `large-v3` |
| Quick draft, short clip | `medium` or `small` |
| Turbo (v3-turbo) — 8× faster, ~minor quality drop | `large-v3-turbo` |

If the user says "haute qualité" / "qualité optimale" → always `large-v3`, never turbo/medium.

## Performance benchmarks (indicatifs, GPU portable haut de gamme 16 Go)

- openai-whisper large-v3: ~1.4-1.6× realtime (GPU under-used)
- faster-whisper large-v3 fp16: ~5-8× realtime (GPU saturated, P0)
- faster-whisper large-v3-turbo fp16: ~12-15× realtime

43-min audio: openai-whisper ≈ 27 min, faster-whisper ≈ 6-8 min.

## Synthèse multi-agents (option)

Déclenchée **seulement** si l'utilisateur la demande (cf. tableau en tête). S'appuie sur le transcript brut déjà produit. Principe validé par l'état de l'art (multi-LLM summarization, agent-as-judge) : **plusieurs agents indépendants → consolidation → vérification anti-fabrication**. Le gain vient de l'agrégation de points de vue indépendants, pas de la diversité de modèles → on garde **le même modèle, des angles différents**.

Règle d'or, identique à `analyse-reunion` : **ne rien fabriquer**. Toute affirmation doit être sourçable dans le transcript ; sinon « non précisé ». C'est le rôle de l'agent vérificateur.

### Étape A — Détecter le type de contenu

Avant de lancer les agents, classer le transcript (lecture rapide, ou 1 mini-agent classifieur si ambigu) en un type, qui adapte les angles :

| Type | Indices | Angles privilégiés |
|------|---------|--------------------|
| **réunion** | plusieurs locuteurs, décisions, « on est d'accord », actions | décisions · actions/responsables · points en suspens |
| **cours / conférence** | un locuteur dominant, pédagogie, concepts | plan du contenu · notions clés · exemples & définitions |
| **note vocale / mémo** | un locuteur, idées en vrac, court | idées principales · to-do implicites · rappels |
| **interview** | Q/R alternées | thèmes abordés · réponses marquantes · citations |

L'utilisateur peut forcer le type en argument (ex. `synthese type=cours`).

### Étape B — Choix du niveau (auto selon la durée)

Lire la durée (déjà obtenue via `ffprobe`). Override possible : `--rapide` ou `--pro`.

| Durée | Niveau | Pipeline |
|-------|--------|----------|
| **< ~10 min** | rapide | **1 seul agent** synthèse (pas de consolidation/vote — overkill sur du court) |
| **≥ ~10 min** | pro | **pipeline multi-agents complet** (3 + 1 + 1) |
| **> ~15k mots (~1h30+)** | pro + chunk | chunker d'abord (cf. Étape E), puis pipeline complet sur les synthèses partielles |

### Étape C — Pipeline rapide (court)

Un seul appel : dispatcher **1 agent** (`Agent`, subagent_type `general-purpose`) avec le transcript entier + les angles du type détecté. Il rend directement la synthèse structurée. Pas de vérificateur séparé : lui demander explicitement de **ne citer que ce qui figure dans le transcript** et de marquer « non précisé » sinon.

### Étape D — Pipeline pro (long) : 3 agents → consolidateur → vérificateur

Lancer les **3 agents synthèse EN PARALLÈLE** (un seul message, 3 appels `Agent`), chacun avec un angle différent adapté au type. Chaque agent reçoit le **transcript complet** et ne renvoie QUE sa synthèse (données brutes, pas de message à l'utilisateur).

Exemple pour une **réunion** (adapter les 3 rôles selon le type — cf. Étape A) :
- **Agent 1 — Décisions & actions** : décisions prises (qui a tranché), actions `Qui | Quoi | Échéance`, engagements.
- **Agent 2 — Fil & sujets** : déroulé thématique, sujets abordés, positions/désaccords des participants.
- **Agent 3 — Suspens & risques** : questions ouvertes, points reportés, non-dits, risques, dépendances.

Prompt commun à injecter dans chaque agent :
> « Tu reçois le transcript intégral d'un/e {type}. Produis UNIQUEMENT la partie « {angle} » d'une synthèse, en français, puces `•`, ton factuel. **N'invente rien** : tout doit être sourçable dans le transcript, sinon écris « non précisé ». Si un locuteur est ambigu, signale-le, ne devine pas. Ta réponse EST la donnée de retour (pas de préambule). Si tu rencontres une difficulté ou un doute, cherche d'abord en ligne avant de supposer. Si tu dois poser une question, une seule à la fois. »

Puis **1 agent consolidateur** : reçoit les 3 synthèses partielles + le transcript, fusionne en **une** synthèse cohérente, dédoublonne, harmonise. Structure de sortie identique à `analyse-reunion` quand c'est une réunion (En-tête · TL;DR · Sujets · Décisions · Actions · Suspens · Citations), sinon structure adaptée au type.

Puis **1 agent vérificateur (agent-as-judge, adversarial)** : reçoit la synthèse consolidée + le transcript, et pour **chaque affirmation** vérifie qu'elle est étayée. Il **supprime ou marque « (non vérifié) »** tout ce qui n'est pas sourçable, et signale les sur-interprétations. Sa sortie = la synthèse finale nettoyée. Prompt :
> « Tu es vérificateur. Confronte chaque ligne de la synthèse au transcript. Supprime ce qui n'y figure pas, corrige les attributions de locuteur erronées, remplace toute affirmation non étayée par « non précisé ». Ne rajoute aucune information nouvelle. Rends la synthèse finale corrigée uniquement. »

### Étape E — Chunking (transcripts > ~15k mots seulement)

Map-reduce **sémantique** (par sujet, pas par tokens fixes) : 1 agent segmente le transcript en blocs thématiques (overlap ~10 % aux frontières) → 1 agent résume chaque bloc → on injecte ces résumés de bloc (au lieu du transcript entier) dans le pipeline pro de l'Étape D. En dessous du seuil, ne PAS chunker (tout tient dans le contexte d'Opus/Sonnet).

### Étape F — Écriture & restitution

- **UN SEUL fichier de synthèse, le résultat final.** Ne JAMAIS écrire les synthèses intermédiaires (les 3 angles, le consolidé non vérifié) sur disque, ni en doublon. Le seul `.md` écrit est la sortie de l'agent vérificateur (Étape D) ou de l'agent rapide (Étape C). Les sorties intermédiaires restent en mémoire, transmises d'agent en agent.
- **Modèle** : pour les agents de synthèse, préférer **Sonnet** (excellent sur les CR ; `model: "sonnet"` dans l'appel `Agent`). La transcription, elle, reste Groq/faster-whisper.
- **Fichiers** : `.txt` brut **toujours** + synthèse en **`.md` daté à côté du source** : `<dossier-source>/<YYYY-MM-DD>-synthese-<slug>.md`. Si la source vient de Drive (pas de fichier local persistant), écrire dans `~/Downloads/`. Si un `.md` de synthèse existe déjà pour cette source, l'écraser plutôt que d'en créer un second.
- **Chat** : afficher le cœur (En-tête + TL;DR + Décisions + Actions pour une réunion ; équivalent pour les autres types) et donner les deux chemins.
- **Ne pas** créer de tâches / notes / e-mail automatiquement — comme `analyse-reunion`, proposer les next steps et attendre un OK explicite.

### Coût / garde-fous

- Pipeline pro = 5 agents (+2 si chunking). Acceptable sur du long ; c'est pourquoi le court bascule en mono-agent automatiquement.
- Toujours produire le `.txt` brut **avant** de lancer la synthèse : si un agent échoue, le transcript est déjà sauvé.

## Troubleshooting

- **VRAM OOM**: Use `compute_type='int8_float16'` (halves VRAM, minimal quality impact).
- **CUDA not detected**: `python -c "import torch; print(torch.cuda.is_available())"` — must be True. Reinstall torch with CUDA if False.
- **cuDNN / cuBLAS errors**: faster-whisper needs cuDNN 8/9 DLLs. Install `nvidia-cudnn-cu12` via pip if missing.
- **Wrong language detected**: pass `language='fr'` explicitly, never rely on auto-detect for short or noisy clips.
- **Repeated hallucinations in silent parts**: enable `vad_filter=True` (already in default).

## What NOT to do

- Don't use `python -m whisper` (openai-whisper CLI) — 4-8× slower for identical quality.
- Don't drop `beam_size` below 5 when user asked for quality.
- Don't skip `language='fr'` — auto-detect can pick wrong language on French audio with English words.
- Don't write the transcript next to the Drive original — always to the work folder (`$TMPDIR/whisper_out/`), then move it.
- Don't forget to clean the temporary files once the transcript is stored.
