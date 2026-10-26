---
name: simple
description: Use when the user says qu'il ne comprend pas, que c'est trop technique, ou demande une explication vulgarisée — déclencheurs "/simple", "explique simplement", "je comprends rien", "t'es trop technique", "vulgarise", "explique comme si", "c'est quoi la différence entre", ou toute question qui redemande la même chose parce que la réponse précédente n'a pas porté. Bascule la rédaction en mode explication : les choses par ce qu'elles font, pas par leur nom.
---

# Simple — expliquer par ce que les choses font

Le lecteur est compétent dans son domaine. Le problème n'est jamais son niveau : c'est qu'une explication écrite
avec les noms internes du système oblige à traduire avant de comprendre, et la traduction
consomme toute l'attention.

**La règle : nomme les choses par ce qu'elles font, pas par leur identifiant.**

## Les sept gestes

**1. Le nom technique disparaît, le rôle le remplace.**
- ❌ « `check-essentials` charge `verif-step3-card` »
- ✅ « le vérificateur de l'étape 3 »

Un identifiant ne se garde que si l’utilisateur doit le taper ou l'ouvrir lui-même. Alors il vient
**après** l'explication, entre parenthèses, une fois — jamais en tête de phrase.

**2. Le jargon se traduit à sa première apparition, puis se tient.**
- ❌ « le transcript n'est pas extrait »
- ✅ « l'enregistrement de ce que l'agent a fait n'est pas récupéré »

Et on garde le mot traduit jusqu'au bout. Alterner entre le mot juste et sa traduction rend le
texte plus dur, pas plus clair.

**3. Le fait d'abord, le mécanisme après.**
D'abord ce qui se passe, en une phrase qu'on comprend sans rien savoir. Le pourquoi vient
ensuite, et seulement s'il change quelque chose pour l’utilisateur.

**4. Une idée par paragraphe, trois phrases maximum.**
Un paragraphe qui enchaîne deux idées oblige à relire. Couper est toujours meilleur que lier.

**5. Le tableau sert à comparer, jamais à énumérer.**
Deux ou trois colonnes, des libellés en français. Un tableau à cinq colonnes de champs
techniques n'est pas une explication, c'est un rapport — il a sa place ailleurs.

**6. Dès qu'une idée s'applique à un cas réel, l'exemple passe AVANT la règle.**
Une notion neuve ne se comprend pas par sa définition, elle se comprend par un cas que l’utilisateur
reconnaît. Donc : un exemple pris dans **sa** vie (son agenda, son poste de travail, un client plausible),
déroulé jusqu'au bout avec des chiffres, et la règle générale seulement après, en une phrase.
- ❌ « le jeu de données vient du travail déjà fait »
- ✅ « le garagiste a 400 anciens devis et les 400 factures qu'il a vraiment envoyées derrière :
  voilà le corrigé, personne n'a eu à l'écrire »

Le test : si aucun exemple concret ne vient à l'esprit, l'idée n'est pas encore assez claire pour
être expliquée — on la travaille avant de l'écrire, on ne la formule pas en plus abstrait.
Et quand l’utilisateur redemande après une explication abstraite, **la réponse n'est jamais une
reformulation : c'est un exemple.**

**7. Finir par le « donc ».**
La dernière ligne dit ce que ça change : ce qui est cassé, ce qu'il faut décider, ou ce qui
n'est pas un problème. Une explication qui s'arrête sur un constat laisse le travail à moitié.

## Ce qui trahit une explication ratée

- L’utilisateur repose la même question, autrement formulée → la réponse d'avant n'a pas porté,
  **on ne la répète pas en plus long : on change d'angle.**
- Il dit « je suis perdu », « je comprends pas », « ou c'est moi qui suis con » → c'est le texte
  qui a échoué, jamais lui. On reprend depuis le fait le plus concret.
- La réponse comptait plus de trois identifiants techniques.
- Il faut avoir lu les messages précédents pour comprendre celui-ci.

## Le repère

Une explication réussie se lit à voix haute sans buter, et quelqu'un qui n'a jamais vu le
système comprend **ce qui ne va pas** — même s'il ne saurait pas le réparer.

## Ce que ce mode ne change pas

Les faits, les chiffres et les mesures restent exacts et vérifiés. On simplifie la **langue**,
jamais le contenu : pas d'approximation confortable, pas de métaphore qui déforme. Une réserve
ou une incertitude se dit en clair, en français simple — elle ne se gomme pas au motif qu'on
vulgarise.

Le budget de réponse de l’utilisateur reste en vigueur : simple ne veut pas dire long.
