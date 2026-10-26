---
name: illustrate
description: Use when the user wants to illustrate a slide or a point with a REAL web image — un screenshot de presse pour un fait/histoire (ex. « La société A rachète la société B pour 1 Md$ »), ou une image trouvée via Google Images pour un concept. Cherche, JUGE au visuel, pré-crop PIL, et place sans masquer le contenu. Déclencheurs : « illustre cette slide/ce point », « trouve une image pour X », « ajoute un screenshot d'article », « illustre la présentation ».
---

# Illustrate — poser une vraie image qui illustre un point

Deux modes. Constante : **je JUGE le rendu au visuel, jamais poser à l'aveugle.**

## Règles (garde-fous, apprises en conditions réelles)
- **Langue** : requête dans la langue du deck (deck EN → recherche EN, jamais une image FR sur un deck EN).
- **Pré-crop PIL, JAMAIS `ppt_crop_picture`** — le crop PPT + resize s'annulent et laissent du bruit. On recadre l'image AVANT insertion, c'est déterministe.
- **Placement qui lit les shapes** : `ppt_list_shapes` d'abord ; faire de la place (ex. narrow un textbox) pour ne RIEN masquer.
- **Autorité de source** : deck dirigeants → presse/officiel > infographie de blog / UGC. Pour un FAIT, préférer un screenshot de presse.
- **Je juge toujours** : voir les candidats ET le rendu final ; corriger une fois si besoin.

## Mode A — screenshot de presse (pour un fait / une histoire)
1. `WebSearch` le fait → repérer un article d'un média crédible (CNBC, Bloomberg, Reuters, Axios…).
2. Playwright : `browser_navigate` sur l'article.
3. **Fermer le mur cookies / retirer les overlays** via `browser_evaluate` :
   ```js
   () => { for(const f of document.querySelectorAll('iframe')){try{const d=f.contentDocument;if(d){const b=[...d.querySelectorAll('button')].find(x=>/accept|accepte|agree/i.test(x.textContent));if(b)b.click();}}catch(e){} f.remove();} document.querySelectorAll('[id*="consent" i],[class*="consent" i],[class*="onetrust" i],[class*="Ad-" i],[class*="hero" i]').forEach(e=>e.remove()); document.documentElement.style.overflow='auto'; document.body.style.overflow='auto'; return 'ok'; }
   ```
4. `browser_take_screenshot` — `filename` = chemin ABSOLU dans le scratchpad (il y est écrit).
5. **Pré-crop PIL** sur le bloc utile (titre + date + byline pour un clipping) :
   ```python
   from PIL import Image
   im = Image.open('shot.png')                 # noter im.size
   im.crop((x0, y0, x1, y1)).save('crop.png')  # box en pixels
   ```
   Déterminer (x0,y0,x1,y1) en REGARDANT le screenshot ; **vérifier le crop avec l'outil Read** avant de poser.
6. Poser : voir « Placement » ci-dessous.

## Mode B — Google Images (pour un concept / une illustration)
1. Playwright : `browser_navigate` `https://www.google.com/search?q=<requête+EN>&udm=2` (si le navigateur est déjà connecté à un compte Google → pas de mur cookies).
2. `browser_take_screenshot` de la grille → **JE regarde et je CHOISIS** la meilleure (fit + autorité + couleur/thème + langue).
3. Cliquer la vignette choisie (`browser_evaluate`, matcher par la légende du résultat), puis récupérer l'URL pleine résolution :
   ```js
   () => { const big=[...document.querySelectorAll('img')].filter(i=>i.naturalWidth>200 && /^https?:/.test(i.src) && !/gstatic|encrypted-tbn|google\.com\/(images|logos)/.test(i.src)); big.sort((a,b)=>b.naturalWidth*b.naturalHeight-a.naturalWidth*a.naturalHeight); return big[0] && {w:big[0].naturalWidth,src:big[0].src}; }
   ```
4. `ppt_add_picture_from_url` (param `url`) — OU télécharger et pré-crop PIL si l'image a du bruit autour.

## Placement (commun)
1. `ppt_list_shapes` sur la slide → repérer les zones libres et ce qu'il ne faut PAS masquer.
2. Faire de la place si besoin : `ppt_update_shape` (param `shape_name`) pour narrow un textbox (ex. verdict → `width` 500).
3. Poser : `ppt_add_picture` (param `file_path`) ou `ppt_add_picture_from_url` (param `url`), avec `left/top/width`. Régler `width` ET `height` en respectant l'aspect de l'image croppée (sinon distorsion). Si l'aspect dérape au resize, poser `width` seul puis ajuster.
4. `ppt_get_slide_preview` → vérifier : aucun chevauchement, lisible, cohérent avec la charte. Ajuster une fois.
5. Polish optionnel : ombre douce (`ppt_set_shadow`) pour décoller le clipping du fond.

## Notes techniques (vérifiées)
- Playwright bloque `file://` (pour un HTML local → le servir en http `python -m http.server`). Les URLs web externes marchent directement.
- Screenshot Playwright : passer un chemin ABSOLU du scratchpad comme `filename`.
- `ppt_add_picture` attend `file_path` ; `ppt_add_picture_from_url` attend `url`. Activer la présentation par index d'abord (`ppt_activate_presentation`).
- `ppt_update_shape` et `ppt_format_text` attendent `shape_name` (pas `shape_name_or_index` pour update ; l'inverse pour format — lire l'erreur si doute).
- PIL (Pillow) est dispo.

## Où s'en servir
À l'étape « illustration » d'une présentation : le storyboard peut porter une colonne illustration ; ce skill source et pose l'image point par point, dans les emplacements d'image du modèle (pleine page, image + texte) ou dans le vide d'une slide.
