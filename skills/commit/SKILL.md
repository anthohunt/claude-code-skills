---
name: commit
description: Use when the user asks to commit and push their work — "/commit", "commit et push", "commit ça", "pousse", "sauvegarde le travail". Splits what is lying around into ATOMIC commits (one per intention, never a catch-all), each with a descriptive title that stands alone in `git log --oneline` and a body that says WHY, then pushes each repository through its own channel. Aims for a history that reads like a story, not a string of "fix" and "wip".
---

# /commit — atomique, puis poussé

Deux règles, et tout le reste en découle.

**Un commit = une intention.** Pas « les modifs de l'après-midi ». Si le message a besoin d'un « et aussi », c'étaient deux commits. Un correctif qu'on veut annuler seul doit pouvoir l'être sans emporter le reste.

**Le message dit POURQUOI.** Le diff dit déjà quoi. Ce qui se perd, c'est ce qu'on a constaté avant de corriger — la mesure, le symptôme, ce qu'on a écarté. Écris-le : dans six mois c'est la seule chose qui manquera.

## Connaître ses dépôts

Un travail de session touche souvent plusieurs dépôts sans qu'on y pense (le code, les skills, les notes, un dépôt de configuration). Au début, dresse (ou relis) la carte : pour chaque dépôt, **où il est**, **son remote**, **comment on pousse** (clé SSH, jeton, dépôt en lecture seule depuis cette machine…). Si la carte n'existe pas, demande-la une fois et garde-la dans les notes du projet.

Pièges fréquents à noter dans la carte :
- un dépôt **sans remote** : le commit ne vit que sur cette machine — le dire à l'utilisateur, c'est un point ouvert ;
- un dépôt **en lecture seule** depuis cette machine : on commite ici, puis on tire le commit depuis une machine qui peut pousser (`git fetch <ssh-url> <branche> && git merge --ff-only FETCH_HEAD && git push`) ;
- un **auto-commit** automatique (outil de sauvegarde) : un `nothing to commit` n'est alors pas une anomalie — vérifie `git log --oneline -3`, le travail y est peut-être déjà sous un message générique ;
- un dossier suivi par un dépôt **plus large** (un dossier personnel entier) : n'y commite rien sans intention explicite.

## La marche à suivre

**1. Regarde partout.**
```bash
for d in <dépôt-1> <dépôt-2> <dépôt-3>; do echo "== $d"; git -C "$d" status --short | head -20; done
```

**2. Groupe par intention, pas par dépôt ni par fichier.** Lis le diff, pas seulement les noms : deux fichiers touchés ensemble ne sont pas forcément le même changement, et un seul fichier peut en porter deux. Écris la liste des commits que tu vas faire avant d'en faire un seul.

**3. Commite groupe par groupe**, en nommant les chemins — jamais `git add -A` quand plusieurs intentions coexistent dans le même dépôt. Vérifie ce qui est mis en scène (`git diff --cached --stat`) : aucun secret, aucun fichier généré, aucune sauvegarde `.bak`.

**4. Pousse chaque dépôt par son canal**, et **vérifie** : `git rev-list --left-right --count @{u}...HEAD` → `0 0` = à jour. Un `push` silencieux qui a échoué ressemble à un succès.

**5. Rends compte en une ligne par dépôt** : le hash, et poussé ou non.

**6. Donne le lien où l'utilisateur ira vérifier.** Un hash seul ne se vérifie pas. La ligne de compte rendu porte l'URL de la **branche** et celle du **commit** (la branche bouge, le commit non). Pour un dépôt sans interface web ou sans remote, le dire franchement et donner la commande pour le lire (`git -C <dépôt> show <hash>`).

## La ligne de titre — c'est elle qu'on relira

`git log --oneline` est la vue par défaut. Un titre qui n'apprend rien rend l'historique illisible, quelle que soit la qualité du corps.

**Une ligne de 72 caractères** qui se lit comme une phrase : `<portée> : <ce qui change>`, à l'indicatif présent, sans point final. La portée est le composant touché, pas le nom du fichier.

| ❌ | ✅ |
|---|---|
| `fix bug` | `scheduler : basculer de compte avant de s'éteindre sur un quota atteint` |
| `update skill` | `verification : un verdict conforme est acquis, registre des verdicts` |
| `wip` · `divers` · `maj` | `runs : deux exécutions de la même pipeline peuvent tourner en parallèle` |
| `modif index.html` | `recharge : une heure par fenêtre, pas une pour les deux` |

**Le test** : quelqu'un qui lit `git log --oneline` un mois plus tard, sans ouvrir le diff, doit savoir ce que ce commit a changé et pouvoir décider s'il l'ouvre. « fix », « wip », « update », un nom de fichier seul, ou un titre qui pourrait coiffer n'importe quel commit du dépôt : réécris-le.

**Le corps est séparé du titre par une ligne vide** — sans elle, git traite tout comme un titre et `--oneline` devient un pavé.

## L'historique se lit comme un récit

- **Une suite de commits qui se réparent l'un l'autre.** Trois `fix` d'affilée sur le même fichier disent que le premier n'était pas fini. Tant que rien n'est poussé, corrige avant de commiter plutôt que d'empiler.
- **Des titres qui ne se distinguent pas entre eux.** Deux commits « corrections UI » dans la même journée sont deux commits qu'on ne pourra plus démêler.
- **Un commit géant en fin de journée.** Ce n'est pas un historique, c'est une sauvegarde.

## La forme d'un message

```
<portée> : <ce qui change, à l'indicatif présent>

<Le symptôme ou la mesure qui a motivé le changement — ce qu'on a constaté,
avec des chiffres quand il y en a.>

<Ce qui a été fait, et surtout ce qui a été ÉCARTÉ et pourquoi.>

<Ce qui a été constaté après : la preuve que ça marche.>
```

Termine par la ligne de co-auteur que l'environnement demande (`Co-Authored-By: …`), si l'utilisateur ou le projet en demande une.

**Par SSH, écris le message sans accents** si le canal les abîme : un commit parti avec des caractères cassés ne se corrige plus une fois poussé. Le corps peut être long — c'est là que vit le pourquoi.

## Ce qu'on ne fait pas

- **Pas de `--no-verify`, pas de `--no-gpg-sign`.** Un hook qui échoue signale quelque chose : on répare la cause.
- **Pas d'amend** sur un commit déjà poussé.
- **Pas de commit qui mélange** une correction et un renommage, ou un correctif et sa documentation dans un autre dépôt : ce sont deux commits, dans deux dépôts, et c'est très bien.
- **Rien n'est poussé que le travail ne soit vérifié.** Si des tests existent et qu'ils n'ont pas tourné, dis-le dans ta réponse — pas dans le message de commit.
