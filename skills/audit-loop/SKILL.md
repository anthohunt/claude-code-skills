---
name: audit-loop
description: Boucle d'audit & amélioration d'une app web (UX/UI, cohérence, accessibilité, flux, ce qui manque). Lance des "quality agents" INDÉPENDANTS qui critiquent l'app via Playwright (ils ne réparent JAMAIS), puis l'agent principal (toi) répare et nettoie, puis on reboucle jusqu'à convergence. Déclencheurs : "lance une boucle d'audit", "boucle d'amélioration", "audit loop", "audite l'appli", "critique l'app", "lance les quality agents", "fais une passe d'audit UX".
metadata:
  type: reference
---

# Audit-Loop — boucle critique → réparation → re-critique

Quand l’utilisateur dit « lance une boucle d'audit » / « boucle d'amélioration » sur une app web, exécute ce protocole.

## Principe (rôles séparés — NON négociable)
- **Quality agents = critique SEULEMENT.** Ils explorent l'app via Playwright (vrai navigateur, vrais clics, screenshots), cherchent un MAXIMUM de failles, et rendent un verdict structuré. **Ils ne modifient AUCUN fichier.** Ils sont indépendants et adversariaux : leur job est de démolir, pas de ménager.
- **Quality agents = VIERGES de toute connaissance du projet (impartialité).** On ne leur donne NI le nom du produit, NI son objectif, NI la liste des features, NI le vocabulaire métier. Juste la/les URL(s) + leur lentille. Ils **découvrent l'app uniquement en l'explorant et en interagissant**, exactement comme un utilisateur qui arrive à froid sans mode d'emploi. C'est ce qui rend leur jugement impartial et révèle la vraie découvrabilité (« est-ce compréhensible sans qu'on m'explique ? »). S'ils ne comprennent pas à quoi sert tel élément, c'est un finding, pas une lacune de l'agent.
  - Toi (agent principal), tu connais le projet et l'objectif — c'est TOI qui juges si une critique « je n'ai pas compris X » est un vrai problème d'UX ou un faux positif. Les agents fournissent le regard neuf ; toi tu apportes le contexte au moment de la synthèse.
- **Toi (agent principal) = réparation + nettoyage.** Tu synthétises leurs critiques, priorises, puis tu corriges et tu nettoies toi-même. Tu vérifies chaque correctif **comme un utilisateur** (Playwright / la vraie URL), pas juste les logs.
- Puis tu **reboucles** : nouvelle passe de critique sur l'app corrigée, jusqu'à ce qu'il ne reste que du mineur OU que l’utilisateur dise stop.

## Étape 1 — Cadrer la cible
- URL(s) à auditer (ex. page principale + sous-pages), parcours cœur attendu, et tout contexte produit (à quoi sert l'app, qui l'utilise).
- Note l'état courant (git/working tree) avant de modifier, pour pouvoir revenir en arrière (backups).

## Étape 2 — Lancer les quality agents (parallèle, lentilles distinctes)
Dispatch 3–5 agents `Agent` EN PARALLÈLE (un seul message, plusieurs appels), chacun une **lentille adversariale distincte** pour ne pas se recouvrir :
1. **Première impression / onboarding** : on arrive à froid — sait-on quoi faire, où cliquer ? hiérarchie visuelle, guidage, libellés, « empty states », charge cognitive au premier regard.
2. **Architecture de l'information / cohérence** : doublons et chevauchements (ex. mêmes concepts dans le header ET ailleurs), nommage incohérent, modèle mental, regroupements illogiques.
3. **Interaction / flux / états** : peut-on accomplir le parcours cœur de bout en bout ? interactions cassées/confuses, feedback, erreurs, états de chargement, responsive.
4. **Accessibilité & qualité front** : contraste, focus clavier, aria, tailles de cible, erreurs console, performance perçue.
5. **Épure / signal vs bruit (PRINCIPE CARDINAL)** : trop de texte ? trop de boutons/options visibles d'un coup ? l'action essentielle est-elle noyée ? **La complexité doit vivre dans l'ingénierie (le code), PAS dans l'interface.** L'UI va à l'essentiel : peu de texte, peu de boutons, style épuré, une action principale évidente par écran. Toute surcharge visuelle (compteurs redondants, champs secondaires, libellés bavards, boutons rarement utiles) = **finding majeur**, pas cosmétique. Demander : « qu'est-ce qu'on peut RETIRER sans rien perdre ? ».
6. (option) **Parité / complétude métier** : ce qui manque vs l'intention produit.

Consigne à CHAQUE agent (mets-la dans le prompt) :
- « Tu CRITIQUES uniquement, tu ne modifies AUCUN fichier. Tu ARRIVES À FROID : tu ne sais RIEN de cette app (ni nom, ni objectif, ni features). Découvre-la EN L'EXPLORANT via Playwright (navigate, screenshot, snapshot, **clique partout, remplis les champs, lance les actions**) sur la/les URL(s) suivantes : <URLs>. Juge ce que tu vis : est-ce clair ? sait-on quoi faire ? qu'est-ce qui casse / déroute / manque ? Sois adversarial : trouve le MAXIMUM de problèmes. »
- NE DONNE PAS à l'agent : le nom du produit, son but, son vocabulaire, sa liste de fonctions, ni ce passage de contexte. Donne SEULEMENT : les URL(s), sa lentille, et le format de rendu.
- Pour chaque problème : **localisation précise** (page, élément, capture), **sévérité** (bloquant / majeur / mineur), **pourquoi c'est un problème** (impact utilisateur), **suggestion** d'amélioration. Plus : « qu'as-tu compris de l'app rien qu'en l'explorant ? » (révèle les malentendus = findings).
- Rendre une liste priorisée + un verdict global (note /10 + 3 forces + les pires problèmes).
- Propager les règles : incertitude → WebSearch d'abord ; une question à la fois ; répondre en français.

## Étape 3 — Synthèse (toi)
- Agrège les findings des agents, **déduplique**, **priorise** (bloquant → mineur), retire les faux positifs (vérifie toi-même les cas douteux).
- Écris une todo claire (fichier `dist/AUDIT-<date>.md` ou TodoWrite).

## Étape 4 — Réparer + nettoyer (toi)
- Corrige par lots, du plus impactant au moins. Édits sûrs (backup, ancrés si fichier partagé/prod), vérifiés.
- **Vérifie chaque correctif comme un utilisateur** (Playwright / vraie URL), pas seulement la syntaxe.

## Étape 5 — Reboucler
- Relance une passe de quality agents sur l'app corrigée. Compare : les problèmes traités ont-ils disparu ? nouveaux problèmes introduits ?
- Continue jusqu'à : plus que du mineur, ou l’utilisateur dit stop. Indique à chaque tour le « reste à faire ».

## Conventions
- Les agents n'écrivent jamais ; seul toi écris. (Évite les conflits + garde la cohérence.)
- Si l'app est partagée/en prod, applique les correctifs en édits ancrés + backups, et vérifie la non-régression.
- Toujours montrer à l’utilisateur : (a) le verdict d'audit priorisé, (b) ce que tu as corrigé + preuve, (c) le reste.
