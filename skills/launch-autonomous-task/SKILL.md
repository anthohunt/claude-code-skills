---
name: launch-autonomous-task
description: >-
  Lancer les tâches autonomes fixées avec `add-autonomous-task` : une tâche nommée, ou TOUTES les
  tâches prêtes. Chaque tâche tourne seule sous une boucle `monitor` qui re-vérifie ses critères et
  s'arrête d'elle-même quand ils sont tous atteints. Déclencheurs : « /launch-autonomous-task »,
  « lance les tâches autonomes », « lance la tâche autonome X », « lance X en autonome »,
  « où en sont les tâches autonomes », « liste les tâches autonomes », « arrête la tâche autonome X ».
---

# launch-autonomous-task — lancer, surveiller, s'arrêter seule

Registre : `~/.claude/autonomous-tasks/<slug>.md` (format dans `add-autonomous-task`).
Lancer une tâche est la décision de l’utilisateur : ce skill ne s'exécute que sur sa demande.

## 1. Choisir quoi lancer

- « lance les tâches autonomes » → toutes celles en `statut: prête`.
- « lance X » → celle-là. En `brouillon` : faire d'abord valider ses critères (une question), puis lancer.
- Rien de prêt → le dire en une ligne, avec la liste des brouillons.

## 2. Lancer une tâche

1. Relire le fichier en entier. `statut: en cours`, `lancée:` rempli, une ligne au journal.
2. **Ouvrir la surveillance : invoquer le skill `monitor`**, chantier = le slug :
   - un élément par critère (« ok si » = le critère, « vérifier » = sa façon de le vérifier) ;
   - un élément pour le travail lui-même (l'agent ou le processus qui avance) ;
   - condition d'ARRÊT de toute la surveillance = tous les critères cochés.
3. Lancer le travail : agent(s) en arrière-plan, bypass permissions, prompt complet (but, critères,
   contexte, plan, garde-fous du fichier, et les règles à propager de tes règles globales). L'agent coche un
   critère dans le fichier quand il l'a constaté, preuve à l'appui dans le journal.
4. Répondre en une ou deux lignes : ce qui est parti, et le rythme de la boucle.

Plusieurs tâches → une surveillance par tâche, lancées en parallèle si elles ne touchent pas les
mêmes fichiers ; sinon l'une après l'autre.

## 3. À chaque passage de la boucle

C'est `monitor` qui passe. Pour une tâche autonome, en plus :
- **re-vérifier soi-même** chaque critère coché (on ne croit pas l'agent sur parole) ; un critère qui
  ne tient plus est décoché, avec la raison au journal ;
- un travail bloqué se relance ou se reprend sous un angle neuf (chercher en ligne, agent frais) ;
  « j'ai épuisé mes idées » n'est pas une sortie ;
- s'arrêter pour demander seulement sur un blocage réel (décision qui revient à l'utilisateur, envoi externe, argent…) ou un garde-fou du fichier.

## 4. Arrêt

- **Réussite** : tous les critères cochés ET re-vérifiés au dernier passage → `statut: réussie`,
  `terminée:` rempli, **arrêter la boucle** (supprimer le cron du `monitor`, vider sa liste), compte
  rendu court à l’utilisateur : critères, preuves, ce qui a changé.
- **« arrête X »** : `statut: arrêtée`, arrêter la boucle et les agents (par PID ou pattern, jamais
  par nom de processus), noter où on en était.
- Jamais d'arrêt sur « je pense que c'est bon » : seulement sur critères constatés.

## 5. Lister / suivre

« liste les tâches autonomes » → tableau : slug · statut · critères cochés / total · dernière ligne
du journal. « où en est X » → ses critères et les 3 dernières lignes du journal.
