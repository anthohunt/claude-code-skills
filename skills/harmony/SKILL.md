---
name: harmony
description: Passe d'harmonisation visuelle sur un livrable qu'on REGARDE — schéma Google Slides, page HTML, deck, image générée. Corrige ce que le rendu révèle et que le code cache : texte tronqué, blocs qui se chevauchent, flèche qui traverse un libellé, colonnes désalignées, grand vide au milieu, débordement hors du cadre. Déclencheurs — "/harmony", "harmonise", "reharmonise", "y a des problèmes de centrage / de chevauchement / du texte cropped", "c'est mal aligné", "ça déborde", ou toute remarque de l’utilisateur sur l'ASPECT d'un livrable visuel. Règle qui commande tout : on ne juge JAMAIS sur le code, on juge sur une image du rendu.
---

# Harmony — harmoniser un livrable visuel

## La règle d'or

**On ne corrige jamais une mise en page sans avoir regardé l'image du rendu.**

Le code ment. Une boîte de 200 000 EMU de haut qui contient trois lignes de texte paraît
correcte dans le script et déborde à l'écran. Une flèche tracée entre deux boîtes traverse
un libellé que rien, dans le code, ne relie à elle. Un `<div>` bien construit se replie sur
lui-même dès que la police change.

Tant que tu n'as pas l'image sous les yeux, tu ne sais pas ce qui ne va pas. Tu devines. Et
une correction devinée en casse une autre.

## La boucle

1. **Rendre** — obtenir une image du livrable, à sa taille réelle.
2. **Regarder** — ouvrir l'image et lister les défauts, un par un, avec leur position.
3. **Corriger la géométrie** — jamais le contenu, sauf si le texte est vraiment trop long.
4. **Re-rendre et re-regarder** — une correction en révèle souvent une autre.
5. Boucler jusqu'à ce qu'une passe ne trouve plus rien.

**Deux passes minimum.** La première corrige les collisions grossières ; la seconde attrape
ce que la première a déplacé. Sur quatre planches d'un même atelier, chaque
planche a demandé exactement deux tours.

## Comment rendre, selon le support

**Google Slides** — l'API rend une image de n'importe quelle page :

```bash
gws slides presentations pages getThumbnail --params '{
  "presentationId":"<id>", "pageObjectId":"<page>",
  "thumbnailProperties.mimeType":"PNG",
  "thumbnailProperties.thumbnailSize":"LARGE"}'
```

Ça rend un `contentUrl` temporaire : `curl -s "$URL" -o shot.png`, puis **Read l'image**.
Attention : `gws` n'accepte pas `--presentationId`, tout passe par `--params`.

**Page HTML** — Chrome en mode sans fenêtre :
`chrome --headless --screenshot=shot.png --window-size=1600,900 file:///...`
Ou le MCP Chrome DevTools quand la page a besoin de tourner (skill `browser-testing-with-devtools`).

**Image déjà produite** — la lire directement, rien à rendre.

## Ce qu'on cherche en regardant

| Défaut | À quoi ça ressemble | Le geste |
|---|---|---|
| **Texte tronqué** | la dernière ligne est coupée net par le bord d'un bloc | agrandir le bloc, pas réduire la police en premier |
| **Chevauchement** | un bloc passe par-dessus un autre, ou un titre de bande est mangé par la boîte du dessous | écarter, et se donner une **voie libre** entre deux bandes |
| **Trait qui traverse** | une flèche coupe un libellé qui n'a rien à voir avec elle | déplacer le libellé hors du chemin, ou raccourcir le trait |
| **Débordement** | un élément sort du cadre, ou passe sous le bord bas | ramener dans le cadre, recompter la hauteur totale |
| **Grand vide** | une moitié de page déserte pendant que le reste est tassé | répartir les bandes sur toute la hauteur, pas les empiler en haut |
| **Désalignement** | des colonnes qui ne commencent pas à la même hauteur, des gouttières inégales | poser une grille et **calculer** les positions, jamais les saisir à la main |

## Les gestes qui évitent la récidive

**La grille se calcule, elle ne se tape pas.** Une rangée de N boîtes se pose ainsi :
`largeur = (total - (N-1) × gouttière) / N`, puis `x_i = x0 + i × (largeur + gouttière)`.
Écrire les positions une par une garantit un décalage d'un pixel quelque part.

**Chaque bande a trois voies** : son libellé, ses boîtes, et une voie vide entre elle et la
suivante où passent les flèches. Un libellé collé aux boîtes du dessous sera recouvert, à
coup sûr — le texte d'une boîte est centré verticalement et déborde vers le haut.

**Une flèche qui doit traverser une zone de texte est une flèche mal placée.** Soit le texte
bouge, soit la flèche part d'ailleurs.

**Un vide n'est pas une erreur en soi** — mais un vide au milieu avec du contenu tassé en
haut, si. Répartir : bandes également espacées sur la hauteur utile.

**On corrige la géométrie, pas le propos.** Raccourcir un texte parce qu'il déborde, c'est
perdre du fond pour une raison de forme. On agrandit d'abord le contenant. On ne coupe le
texte que s'il est réellement bavard — et alors c'est une décision de fond, à annoncer.

## Ce que ce skill ne fait pas

- Il ne redessine pas : il harmonise ce qui existe. Un livrable dont le **contenu** ne va pas
  se retravaille avec le skill du support (`architecture-diagram`, `frontend-design`,
  `design-on-the-go`), pas ici.
- Il n'invente pas de charte : il respecte les couleurs et les polices déjà en place.
- Il ne remplace pas `audit-loop`, qui juge une app entière (UX, parcours, accessibilité) ;
  `harmony` ne juge qu'une surface, et seulement sa mise en page.

## La sortie

Une phrase par défaut corrigé, pas plus — l’utilisateur veut savoir **ce qui a bougé**, pas
comment. Et le rappel de la seule chose qui compte : c'est vérifié sur rendu image, pas sur
le code.
