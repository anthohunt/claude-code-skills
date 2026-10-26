---
name: nightshift
description: Use when the user hands a long task to an agent to run overnight and wants the machine to power off once ALL such tasks are done. Triggers — "fais cette tache en mode nightshift", "lance ca en nightshift", "tache de nuit", "mode nuit, eteins le PC quand tout est fini", or being told a task should follow the nightshift protocol. Each agent self-registers in a shared registry, works, marks itself done, then powers the machine off only if every other task is finished or dead.
---

# Nightshift — protocole d'extinction collective (Windows)

## Quand l'utiliser

L’utilisateur confie une tache potentiellement longue a un agent (par exemple une migration, une generation en masse, une longue analyse) et dit de la faire **en mode nightshift**. Plusieurs agents nightshift tournent en parallele le soir. Le but : le PC s'eteint tout seul **une fois que toutes les taches sont terminees**, et pas avant.

Chaque agent applique ce protocole a **sa propre** tache. Il ne supervise pas les autres : il ne fait que s'inscrire, bosser, se marquer fini, puis verifier s'il est le dernier.

## Regle cardinale : autonomie totale

Une fois la tache passee en nightshift, **l’utilisateur dort et ne repondra plus a AUCUNE question.** L'agent est seul jusqu'au bout.

Consequences absolues :
- **Aucune question, aucune confirmation, aucune attente d'input** apres le demarrage. Un agent bloque sur un prompt ne fait plus de heartbeat → le veilleur le croit mort → le PC peut s'eteindre en pleine tache.
- Face a un imprevu ou une ambiguite en cours de route : **prends la decision la plus raisonnable toi-meme, note-la dans ton compte-rendu, et continue.** Ne t'arrete jamais pour demander.
- Si un blocage est reellement insurmontable et qu'aucune decision sure n'est possible : marque la tache `fail` avec une raison claire (voir etape 3) plutot que de rester suspendu. Ne laisse JAMAIS l'agent en attente indefinie.

C'est pourquoi la tache doit etre **parfaitement definie avant** d'entrer en nightshift (etape 0 ci-dessous).

## Le document commun

Un registre JSON partage : `%USERPROFILE%\.claude\nightshift\registry.json` (Windows).
Tous les acces passent par le helper `nightshift.ps1` (verrou mutex, ASCII, PS 5.1). **Ne jamais editer le JSON a la main.**

Helper : `%USERPROFILE%\.claude\skills\nightshift\nightshift.ps1`

## Le protocole (a suivre dans l'ordre)

### 0. Lever TOUS les doutes — AVANT de s'inscrire
Avant de toucher au registre, verifie que la tache est **sans aucune ambiguite** : objectif precis, perimetre (ce qui est inclus / exclu), criteres de "fini", emplacements/fichiers concernes, choix techniques tranches.

S'il reste **le moindre doute** sur ce qu'il faut faire :
- **Pose les questions a l’utilisateur MAINTENANT**, tant qu'il est encore la. Apres, ce sera trop tard.
- Compose-les avec soin : regroupe tout ce que tu dois savoir, formule des questions nettes (de preference a choix multiples).
- **Une seule question a la fois** (regle generale) : attends chaque reponse avant la suivante.

Ne fais `register` (etape 1) **que lorsque la tache est limpide** et que tu pourrais la mener seul, sans jamais avoir besoin de lui reparler.

### 1. S'inscrire — premier geste une fois la tache claire
Avant de commencer le moindre travail :

```powershell
$id = & "$env:USERPROFILE\.claude\skills\nightshift\nightshift.ps1" -Action register -Desc "<description courte de la tache>"
```

Garde la valeur `$id` retournee : c'est ta cle pour tout le reste. Le premier `register` de la soiree lance aussi le veilleur (filet de securite) automatiquement.

### 2. Bosser — avec preuve de vie
Fais la tache. A **chaque etape majeure** (fin d'une sous-etape, boucle, gros appel), touche ton heartbeat :

```powershell
& "$env:USERPROFILE\.claude\skills\nightshift\nightshift.ps1" -Action heartbeat -Id $id
```

Un heartbeat qui n'est pas rafraichi depuis plus de 30 min fait presumer l'agent mort.

### 3. Se marquer fini — SEULEMENT si c'est vraiment fini
Quand — et uniquement quand — le travail est **reellement** termine :

```powershell
& "$env:USERPROFILE\.claude\skills\nightshift\nightshift.ps1" -Action done -Id $id
```

Si tu dois abandonner la tache (echec irrecuperable), utilise `-Action fail` a la place. Un `fail` libere l'extinction comme un `done` — donc ne l'utilise que si tu renonces pour de bon.

### 4. Verifier si je suis le dernier
Juste apres `done`/`fail` :

```powershell
$verdict = & "$env:USERPROFILE\.claude\skills\nightshift\nightshift.ps1" -Action check -Id $id
```

- `$verdict` vaut **`SHUTDOWN`** → toutes les autres taches sont finies ou mortes. Le helper a deja arme l'extinction (`shutdown /s /t 60`, annulable par `shutdown /a` pendant 60 s). Annonce-le brievement et arrete-toi.
- `$verdict` vaut **`WAIT`** → au moins une autre tache tourne encore. **Ne fais rien d'autre.** N'eteins pas. Arrete-toi simplement.

## Regles strictes (ne jamais enfreindre)

- **JAMAIS** poser de question ni attendre un input apres l'etape 0 : L’utilisateur dort. Tous les doutes se levent AVANT le `register`. En cours de route, tu decides seul (ou tu `fail` proprement), jamais tu n'attends.
- **JAMAIS** marquer `done` si la tache n'est pas reellement terminee. Un `done` premature peut declencher l'extinction et tuer les autres agents.
- **JAMAIS** eteindre la machine toi-meme (pas de `shutdown` manuel). C'est le helper qui l'arme, et uniquement quand `check` renvoie `SHUTDOWN`.
- **JAMAIS** editer `registry.json` directement — toujours via le helper.
- Si `check` renvoie `WAIT`, tu t'arretes en silence : tu n'es pas le dernier, ce n'est pas ton role d'eteindre.

## Le filet de securite (pour info, automatique)

Au premier `register`, un veilleur singleton (`watchdog`) demarre en arriere-plan. Toutes les 5 min il relit le registre ; si **toutes** les entrees sont finies/mortes (heartbeat > 30 min) il arme lui-meme l'extinction. Ainsi, meme si le **dernier** agent plante avant d'avoir pu faire son `check`, le PC finit par s'eteindre (latence max ~35 min). Tu n'as rien a faire pour ca.

## Verifier l'etat (debug)

```powershell
& "$env:USERPROFILE\.claude\skills\nightshift\nightshift.ps1" -Action status
```

Le veilleur ecrit aussi un journal horodate dans `%USERPROFILE%\.claude\nightshift\watchdog.log` :
chaque poll, le moment ou il arme l'extinction, le code retour de `shutdown.exe` et l'eventuel
fallback `Stop-Computer`. A consulter si le PC ne s'est pas eteint comme prevu.
