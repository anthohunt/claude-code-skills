---
name: add-autonomous-task
description: >-
  Fixer une tâche autonome pour plus tard, SANS la lancer : but, critères de réussite vérifiables
  validés par l’utilisateur, contexte, plan, garde-fous, rangés dans le registre des tâches autonomes.
  Déclencheurs : « /add-autonomous-task », « ajoute une tâche autonome », « fixe une tâche autonome »,
  « tâche autonome pour plus tard », « à faire en autonome quand je le dirai ». Le lancement se fait
  ensuite avec `launch-autonomous-task`.
---

# add-autonomous-task — fixer maintenant, lancer plus tard

Une tâche autonome est fixée maintenant et lancée **uniquement quand l’utilisateur le décide**, avec
`launch-autonomous-task`. Une fois lancée, elle tourne seule sous une boucle `monitor` et s'arrête
d'elle-même quand tous ses critères de réussite sont atteints et constatés.

Distinct de `mission` (lancée tout de suite, dépôt `mission-loop`) et de `nightshift` (extinction du PC).

## Le registre

Un fichier par tâche : `~/.claude/autonomous-tasks/<slug>.md` (le mod `taches-autonomes` du dépôt `claude-code-mods` affiche ce dossier dans un panneau)

```markdown
---
slug: <slug>
statut: brouillon | prête | en cours | réussie | arrêtée
fixée: YYYY-MM-DD
lancée:
terminée:
---

## But
<une phrase : ce qui doit être vrai à la fin>

## Critères de réussite
- [ ] C1 — <fait observable> · se vérifie par : <commande, fichier, capture, URL>

## Contexte
<dépôts, serveurs, fichiers, accès, contraintes : tout ce qu'un agent frais doit savoir>

## Plan
1. …

## Garde-fous
<ce qu'il ne faut PAS faire ; les points où l'on s'arrête pour demander (décision qui revient à l'utilisateur, envoi externe, argent, production…)>

## Journal
- YYYY-MM-DD HH:MM — <événement>
```

## Étapes

1. Écrire le **but** en une phrase à partir de ce que l’utilisateur a dit.
2. Chercher soi-même le **contexte** (dépôts, notes du projet, serveurs, transcript) avant de
   demander quoi que ce soit.
3. Proposer les **critères de réussite** : chacun est un fait observable avec sa façon de le
   vérifier. Jamais « ça marche ». Un symptôme visuel se vérifie par une image.
4. Écrire le fichier avec `statut: brouillon`.
5. **Faire valider les critères par l’utilisateur (OUI explicite)**, une question à la fois, avec une
   option ouverte. Au OUI : `statut: prête`, une ligne au journal.
6. Réponse finale : le slug, le but, les critères, « prête — à lancer avec launch-autonomous-task ».

Ne JAMAIS lancer la tâche depuis ce skill, même si tout est prêt.
