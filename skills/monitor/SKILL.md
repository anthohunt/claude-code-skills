---
name: monitor
description: Use when a manager agent must WATCH several ongoing things over time (agents, measures, deployments, machines, dashboards) — "/monitor", "surveille", "tu dois monitorer", "mets-toi un contrôle", "vérifie tout ça régulièrement", "ajoute X à la surveillance", "retire Y de la surveillance", or whenever you launch background work that must be followed until done. Generic, any project. Keeps a LIVING WATCHLIST file (items added/removed as work starts/ends), one recurring check that reads it, fixes or relaunches what is stuck, and stops by itself when the list is empty or the goal is reached.
---

# monitor — une liste vivante de choses à surveiller

Principe : le manager surveille TOUT ce qui est en cours, pas seulement le chantier principal ; la liste évolue au fil du travail ; l'utilisateur ne doit jamais avoir à relancer.

Claude Code n'agit que lorsqu'un message arrive (tâche planifiée, événement, utilisateur). Entre deux, rien ne se passe : un contrôle qui se contente d'un « OK » laisse tout stagner. Ce skill organise donc un **réveil régulier qui vérifie, agit, puis replanifie**.

## 1. Le fichier de surveillance (la source unique)

`<dossier du projet>/surveillance/<chantier>.md` — une section par élément surveillé :

```
## <nom en clair>                       (ex. « Sauvegarde nocturne »)
- quoi : ce qui doit se passer, en une ligne
- vérifier : la commande / le fichier / l'agent à regarder
- ok si : le critère observable (fichier présent, fraîcheur < 20 min, compteur qui avance…)
- si ko : l'action (relancer l'agent X avec tel prompt, redéployer, prévenir l'utilisateur)
- fin : quand retirer l'élément (ex. « le déploiement répond 200 »)
- depuis : date/heure d'ajout
```

- **Ajouter** un élément dès qu'on lance un travail de fond (agent, déploiement, mesure, machine).
- **Retirer** un élément quand sa condition de fin est vraie (et le dire en une ligne à l'utilisateur). Les éléments finis ne restent pas : ils noieraient les éléments vivants.
- **Garder** en tête du fichier : l'objectif global et la condition d'ARRÊT de toute la surveillance.
- Une décision de l'utilisateur qui change ce qu'on surveille = modifier le fichier tout de suite.

## 2. Proposer d'abord, l'utilisateur valide

Avant de créer le moindre contrôle récurrent : écrire, à partir du contexte, **le message de surveillance proposé** — ce qui est surveillé, la fréquence, ce que chaque passage vérifie (preuve concrète), quand on prévient l'utilisateur, la condition d'arrêt — en quelques lignes, puis **attendre sa validation ou ses corrections**. Seulement ensuite : mettre à jour le fichier et créer le contrôle. Pas de contrôle créé avant son accord.
- **Forme** : le prompt du contrôle est un message que le manager s'adresse à lui-même, en sections numérotées : (1) chantier, tâches actives et fichier de surveillance ; (2) CONTRÔLE (un fait vérifié par élément, preuves brutes) ; (3) AGIR (« qu'est-ce qui peut avancer maintenant ? », ce que je tranche seul, ce qui va à l'utilisateur) ; (4) critères et enchaînements ; (5) entretien (flux d'événements, relances) ; (6) compte rendu et condition d'arrêt.
- **Boucle de validation** : s'il corrige ou redécrit ce qu'il veut, ce n'est PAS une validation → reformuler la liste en reprenant fidèlement ses mots, et redemander, jusqu'à un accord explicite. Ne jamais annoncer « c'est en place » sans lui avoir re-soumis la liste.

## 3. La boucle du manager : vérifier, agir, replanifier

**Réveil** : un événement le réveille aussitôt (essai fini, machine tombée, agent bloqué, question d'un agent) ; sinon un passage régulier **dont il choisit lui-même la date**.

**À chaque réveil — un élément = au moins UNE action de vérification réelle :**
1. **Vérifier** : pour CHAQUE élément, exécuter sa ligne « vérifier » et noter le FAIT observé (un chiffre, une heure, un nom), pas une impression. Un élément sans action exécutée ce passage = contrôle NON fait. Un script global qui ne montre que les KO ne suffit pas : lire aussi les OK utiles. Preuves = fichiers, journaux, dernière activité réelle des agents ; jamais ce qu'un agent dit. Si la ligne « vérifier » est vague (« l'agent avance »), la rendre mesurable (commande + critère) avant de continuer.
2. **Agir** : chaque écart donne une action (« si ko »), puis « qu'est-ce qui peut avancer maintenant ? » : donner du travail à un poste libre, la suite à un agent qui a fini, réduire la charge si un quota baisse. Un agent arrêté avec du travail restant = le relancer immédiatement (prompt complet). Prévenir l'utilisateur en 3 phrases max, sans codes internes, seulement si ça change quelque chose pour lui.
3. **Retirer** les éléments dont la condition de fin est vraie.
4. **Replanifier** le prochain réveil selon la phase.
5. Tout OK → une ligne max, qui cite au moins un fait vérifié par élément (ex. « 6 postes notent, 312 courriels en 15 min ; sauvegarde : terminée il y a 3 min »). Jamais un « tout va bien » sans chiffre.

**Bornes de fréquence :**

| Phase | Prochain passage |
|---|---|
| Après un lancement, une relance ou un changement | toutes les 5 min, pendant 25 min |
| Moment décisif (livraison, examen, bascule) | toutes les 5 min |
| Calcul ou entraînement qui tourne | toutes les 15 min |
| Agents au travail | à chaque fin de tâche, et au moins toutes les 15 min |
| Pause ou repos | toutes les 3 h |

**Proactivité** : resserrer de soi-même au premier signe faible (une machine qui ralentit, un essai qui traîne, un journal qui n'avance plus) ; ne jamais allonger au-delà des bornes. Un élément « en attente » depuis plus de 30 min sans raison écrite = anomalie à traiter.

**Mécanique dans Claude Code** : le réveil choisi se pose avec `ScheduleWakeup` (mode dynamique) ; sinon un `CronCreate` **unique** (un seul passage), replanifié à chaque passage (l'ancien supprimé, le suivant créé à la date choisie). En parallèle, un flux d'événements (outil Monitor) sur les journaux utiles : il expire (souvent au bout de 30 min), donc **le ré-armer à chaque expiration**. Chaque événement = une action, pas un constat. Les tâches planifiées vivent dans la session : après un redémarrage de session, recréer le contrôle et le prochain réveil (le fichier de surveillance, lui, persiste).

**Trace de vie** : à chaque réveil, écrire l'heure du passage dans un fichier d'état (`dernier-passage-manager.txt`) : c'est ce qui permet de voir un manager bloqué.

## 4. Les cinq pièges (chacun né d'un incident)

1. **Une pause ne supprime jamais le contrôle.** Pendant une pause, chaque passage vérifie qu'elle tient. Supprimer le contrôle à la demande de pause laisse les agents tourner sans que personne ne le voie.
2. **Vérifier l'état voulu, pas seulement « ça tourne ».** Des processus vivants peuvent être un mauvais signe (un 2e lanceur qui relance des sessions pendant une pause). Contrôler aussi « aucune session démarrée depuis le gel ».
3. **Retirer les éléments finis** : sinon ils sont relus à chaque passage et noient les éléments vivants.
4. **Caler le flux d'événements sur le chantier en cours** (ses journaux, ses sessions), pas sur l'ancien : sinon il ne voit aucun des événements qui comptent.
5. **Un élément « conformité »** : les agents suivent-ils le protocole ? Preuves tirées des journaux (commandes réellement lancées), jamais de ce qu'un agent dit. Un réglage inventé par un agent et recopié dans un prompt se propage d'un passage à l'autre.

**Procédure de pause** (si la pause n'est pas un état du programme) :
1. Poser la pause : bloquer les mesures et poser le drapeau d'arrêt de chaque lanceur.
2. Geler tous les lanceurs et toutes les sessions (superviseurs compris : tmux, cron, systemd), en notant le numéro de processus et la commande de reprise. Piège : tmux relance aussitôt un processus de volet stoppé ; geler alors son enfant ou passer par le drapeau.
3. Afficher un bandeau de pause au tableau de bord et vérifier la page servie.
4. 10 min plus tard, vérifier qu'aucune session n'a démarré depuis le gel. La surveillance continue sur les contrôles de pause. Reprise seulement sur décision de l'utilisateur.

## 5. Fin

Objectif global atteint ou liste vide → supprimer le contrôle et prévenir l'utilisateur. Une pause n'est jamais une raison de supprimer le contrôle.

Messages à l'utilisateur : conclusion d'abord, 3 phrases max.
