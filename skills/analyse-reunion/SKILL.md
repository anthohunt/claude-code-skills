---
name: analyse-reunion
description: Use when the user provides a meeting transcript (visio recording transcribed) and wants it analyzed — triggers like "analyse cette réunion", "fais-moi le CR de cette visio", "j'ai un transcript de réunion à traiter", "résume cette réunion", or `/analyse-reunion`. Reads a text transcript (.txt/.docx/.vtt/.srt, or pasted; audio/video → transcribe first), produces ONE structured analysis (synthèse, décisions, actions, points en suspens), writes a dated .md next to the source, then PROPOSES next steps (task list, project notes, email minutes) without executing them.
---

# Analyse de réunion

Transforme un transcript de réunion en analyse structurée, puis propose les suites. Le skill **s'arrête à l'analyse + propositions** — il ne crée jamais de tâches, ne touche jamais aux notes du projet, n'envoie aucun email sans validation explicite de l’utilisateur.

## Principe directeur : ne rien fabriquer

Tout ce qui est écrit doit provenir du transcript. Si une info manque (échéance, responsable d'une action, qui a tranché), écrire **« non précisé »** — jamais inventer. Si le transcript est ambigu sur le locuteur, le signaler plutôt que d'attribuer au hasard.

## Étape 1 — Récupérer le transcript

Cas nominal : un **fichier texte** (`.txt`, `.docx`, `.vtt`, `.srt`) que l’utilisateur pointe, ou du texte **collé** dans le chat.

- Fichier `.vtt`/`.srt` : ignorer les timestamps/numéros de cue, ne garder que le texte + les noms de locuteurs.
- Si l’utilisateur fournit un **audio/vidéo brut** (`.m4a`, `.mp3`, `.mp4`, etc.) : invoquer d'abord le skill `transcribe-audio` pour obtenir le texte, puis revenir ici.
- Si rien n'est fourni, demander où est le transcript (une seule question).

Lire l'intégralité du transcript avant d'analyser.

## Étape 2 — Produire l'analyse (7 rubriques)

Rédiger UN seul document en français, ton neutre et factuel, puces `•` (jamais de tirets). Rubriques dans cet ordre :

1. **En-tête** — titre de la réunion (déduit du contenu si non donné), date, durée estimée, participants détectés (depuis les noms du transcript).
2. **Synthèse (TL;DR)** — 4 à 6 lignes : de quoi on a parlé, où on a atterri. Lisible en 20 secondes.
3. **Sujets abordés** — organisés par thème (pas chronologiquement). Pour chaque sujet : l'essentiel des échanges + les positions des participants en cas de désaccord.
4. **Décisions prises** — une décision par ligne, claire ; préciser qui a tranché si pertinent.
5. **Actions / to-do** — tableau `Qui | Quoi | Échéance`. Échéance uniquement si mentionnée, sinon « non précisé ». (C'est ce bloc qui alimentera la liste de tâches à l'étape 4.)
6. **Points en suspens / à reclarifier** — questions ouvertes, sujets reportés, désaccords non résolus.
7. **Citations notables** (optionnel) — 2-3 verbatims importants avec le locuteur, seulement si le transcript en contient de marquants.

## Étape 3 — Écrire le livrable

- Écrire l'analyse dans un fichier `.md` **daté**, dans le **même dossier que le transcript source** : `<dossier-source>/<YYYY-MM-DD>-analyse-<slug-titre>.md`. Si le transcript a été collé (pas de fichier source), écrire dans `~/Downloads/`.
- Afficher dans le chat l'**en-tête + la synthèse + les décisions + les actions** (le cœur), et indiquer le chemin du fichier complet.

## Étape 4 — Proposer les next steps (NE PAS exécuter)

Lister les suites possibles et laisser l’utilisateur choisir au cas par cas :

• **Créer les actions dans l'outil de tâches** de l'utilisateur (Google Tasks, Todoist, fichier…).
• **Tracer / suivre dans les notes du projet** (Notion, dépôt, mémoire…).
• **Préparer un email de compte-rendu** aux participants → en brouillon, montré à l'utilisateur et soumis au skill `confirm-external-send` avant tout envoi.

Aucune de ces actions ne se lance sans un OK explicite de l’utilisateur pour cette action précise.

## Règles à respecter

- Puces `•`, jamais de tirets/traits.
- Ne rien fabriquer ; « non précisé » par défaut.
- Le skill produit l'analyse, propose, et s'arrête. Pas d'effet de bord externe sans validation.
