---
name: data-sourcing
description: Use when a deliverable needs defensible figures — "/data-sourcing <sujet>", "source-moi des chiffres fiables sur X", "construis un data pack vérifié". Pipeline de sourcing rigoureuse : des agents chercheurs trouvent des chiffres dans des sources fiables, un juge adversarial essaie de les réfuter, et seuls ceux qui tiennent sortent, avec source primaire, date et fiabilité.
---

# Data-sourcing — chiffres vérifiés par cœur de métier (finders + juge adversarial)

## Why

Glaner des chiffres « à la main » (une recherche, un snippet) produit de la data faible : sources secondaires, métriques confondues (cloud vs LLM, utilisateurs vs part de marché, primo-acheteurs vs part installée), chiffres vendor non corroborés. Pour un livrable présenté à des dirigeants, chaque chiffre doit **survivre à une contestation**.

Ce skill est une **pipeline de sourcing rigoureuse** : une mission définit une liste de **cœurs** (fonctions métier ET/OU secteurs industriels) ; des **agents chercheurs** autonomes trouvent des chiffres dans des sources fiables ; un **juge adversarial** essaie de **refuter** chaque chiffre avant qu'il ne soit retenu. Sortie = par cœur, uniquement les chiffres qui ont tenu, chacun avec source primaire + date + fiabilité — et un « pas de data fiable » honnête là où rien ne tient.

Schéma classique « chercheurs → vérification → juge », focalisé sur la **donnée dure** et la **réfutation**, pas sur la rédaction.

## When to invoke

- `/data-sourcing <sujet>` ou « source-moi des chiffres fiables sur X », « trouve les vrais chiffres par secteur/fonction », « construis un data pack vérifié ».
- Quand un livrable (slide, deck, note) a besoin de **chiffres défendables** et pas d'approximations.

## Architecture (contraintes dures)

- **Max 5 agents en parallèle** (au-delà, la machine sature). Batcher si plus de cœurs.
- Les sous-agents ne spawnent pas d'agents — le leader (conversation principale) orchestre tout.
- Tout sous-agent : **bypass permissions**, `run_in_background`, **cherche en ligne d'abord** (WebSearch/WebFetch), **TL;DR résultat d'abord**, une seule question à la fois.

## Barème de fiabilité (le cœur du juge)

| ★ | Signification | Exemples de sources |
|---|---|---|
| ★★★ | Primaire tier-1 OU ≥2 sources indépendantes concordantes | Menlo Ventures, a16z, Ramp AI Index, Gartner/IDC/Forrester, Stanford AI Index, Epoch AI, McKinsey/Deloitte survey nommée, peer-reviewed |
| ★★ | Source unique crédible mais partielle, OU direction sans % dur, OU vendor corroboré | rapport vendor corroboré, OpenRouter (usage **dev**, à étiqueter), analyste secondaire sérieux |
| ★ | Faible — **rejeté par défaut** | blog SEO, repost LinkedIn/Facebook, « top 10 » non sourcé, source anonyme, métrique confondue |

**Pièges que le juge DOIT traquer (rejet automatique si non résolu) :**
- **Cloud ≠ LLM** (« Cloud X 38 % » n'est pas une part de modèle).
- **Utilisateurs ≠ part de marché** (« 20 M d'utilisateurs de l'outil Y » ≠ 20 % du marché).
- **Primo-acheteurs ≠ part installée** (« Fournisseur A 73 % » = dépenses des nouveaux acheteurs, pas la base installée).
- **Métrique non étiquetée** (spend ≠ tokens ≠ adoption déclarée ≠ usage dev — ne jamais fusionner).
- **Source secondaire** présentée comme primaire (remonter au rapport d'origine).
- **Fait > 12 mois** sur un marché qui bouge en semaines.

## Pipeline

### Étape 0 — Définir la mission
Écrire un fichier mission `datapack/MISSION.md` :
- La **liste des cœurs** (fonctions et/ou secteurs), numérotés.
- Par cœur, **ce qu'on cherche** (par défaut : (a) modèle/fournisseur dominant + part si dispo · (b) taille de marché / adoption chiffrée · (c) 1-2 stats clés).
- Le **barème de fiabilité** (ci-dessus) et la **liste des sources à privilégier**.
- La **cible** : N cœurs, chacun idéalement ≥1 chiffre ★★★.

### Étape 1 — Finders (parallèle, max 5)
Répartir les cœurs en lots (≤5 agents). Chaque finder :
- Reçoit ses cœurs + le barème + la liste de sources tier-1.
- Cherche/fetch en ligne, **remonte à la source primaire** (WebFetch la page réelle).
- Rend, par chiffre : `valeur · cœur · sujet · métrique (type) · source (nom + URL) · date · ★ proposé · note`.
- Interdiction d'inventer : si pas de data → l'écrire.
- Sortie : `datapack/finder-<lot>.md`.

### Étape 2 — Juge adversarial (parallèle, max 5) — comme les *quality agents* d'`audit-loop`
**C'est l'étape qui fait la différence.** Le juge = **critique adversarial dont le job est de DÉMOLIR**, pas de ménager. Indépendant, impartial : il juge chaque chiffre **sur ses mérites**, sans savoir quel finder l'a produit ni « à quel point on y tient ». Pour chaque chiffre proposé :
- **Essaie activement de le refuter** : la source est-elle primaire ? le chiffre y figure-t-il **verbatim** ? la métrique est-elle bien celle annoncée (pas un des pièges ci-dessus) ? est-il récent ? un chiffre **indépendant** le corrobore-t-il ou le **contredit**-il ?
- WebFetch **ses propres** sources (ne pas se contenter de recocher l'URL du finder — vérif circulaire interdite).
- Défaut = **sceptique** : dans le doute, REJECTED ou WEAK, jamais CONFIRMED par complaisance.
- Verdict par chiffre : **CONFIRMED** (★★★) / **WEAK** (★★, à étiqueter) / **REJECTED** (+ raison précise + ce qu'il faudrait pour confirmer).
- Sortie : `datapack/judge-<lot>.md` (verdict + correction éventuelle + source indépendante trouvée).

Option renforcée (sujet sensible) : **panel de 2-3 juges** par chiffre, médiane des verdicts (jamais de débat entre juges : la médiane).

### Étape 3 — Boucle jusqu'à convergence (comme `audit-loop`)
On **reboucle** critique → re-sourcing → re-critique, jusqu'à convergence :
- Le leader relève les cœurs **REJECTED / WEAK / vides**. Pour ceux-là, relance des finders avec un **angle neuf** (autres sources tier-1, autre métrique, source primaire non encore fouillée) — pas re-tourner sur le même wording.
- Re-juge les nouveaux chiffres (mêmes juges adversariaux).
- **Convergence** = chaque cœur a ≥1 chiffre CONFIRMED **ou** est déclaré « pas de data fiable » après **2 tours à sec consécutifs** (on ne s'acharne pas : un « vide » honnête est un résultat valide). Ou arrêt explicite de l’utilisateur.
- À chaque tour, indiquer le **reste à faire** (cœurs encore non couverts).

### Étape 4 — Synthèse
Le leader compile `datapack/VERIFIED.md` + `datapack/verified.json` :
- Par cœur : uniquement les chiffres **CONFIRMED + WEAK** (étiquetés), chacun avec source + date + ★.
- Cœurs sans chiffre survivant → **« pas de data fiable par modèle »** explicite + le qualitatif solide s'il existe.
- En tête : combien de cœurs ont ≥1 ★★★, lesquels restent qualitatifs/vides (transparence).

### Étape 5 — Rapport + handoff
TL;DR à l'utilisateur : cœurs solides vs minces, pièges écartés, `verified.json` prêt à alimenter le livrable (slide/deck).

## Hard rules

- **Aucun chiffre ne sort sans avoir passé le juge.** Finder seul = candidat, pas un fait.
- **Juge ≠ modèle du finder** (anti self-preference) + **récupère ses propres sources** (anti vérif circulaire).
- **Étiqueter chaque métrique** (spend / tokens / adoption / usage dev) — jamais fusionner deux métriques dans un même chart.
- **Jamais inventer** pour remplir un cœur : un « pas de data fiable » honnête vaut mieux qu'un chiffre ★.
- **Max 5 agents parallèle.** Remonter toujours à la **source primaire**.
- Cœurs = **fonctions** (usages IA) ET/OU **secteurs** (industries) selon la mission.

## Output

- `datapack/MISSION.md` · `finder-*.md` · `judge-*.md` · `VERIFIED.md` · `verified.json`
- `verified.json` schéma : `{ cores: [ { id, kind:"function|sector", name, figures:[ {value, subject, metric, source, url, date, stars, verdict, note} ], status:"solid|thin|none", qualitative } ] }`
