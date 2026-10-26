---
name: visuel-recherche
description: Use when the user wants to run an evolutionary visual-improvement tournament — triggers "visuel recherche", "/visuel-recherche", "round suivant", "nouveau challenger", "lance un tour", "améliore le visuel", "montre challenger vs champion". A goal-driven loop where Claude PROPOSES two visuals, the user judges (A/B or challenger-vs-champion), Claude RESEARCHES + designs the next challenger, and — critically — Claude maintains an explicit "Théorie du beau" it updates from each verdict so it learns on its own what makes a visual useful and beautiful (never iterating at random).
---

# Visuel Recherche — tournoi évolutif de visuels

Boucle d'amélioration continue d'un visuel ou d'une interface, pilotée par le goût de l'utilisateur, mais où **c'est Claude qui doit COMPRENDRE tout seul ce qui marche** (le vrai sujet). Pas d'itération au hasard : chaque tour teste une hypothèse falsifiable dérivée des verdicts passés.

## Le protocole (une boucle sans fin)

1. **Deux propositions.** Claude livre 2 visuels concurrents (au round 1 : 2 hypothèses opposées ; ensuite : **challenger vs champion actuel**). Toujours autonomes (un fichier qui s'ouvre seul), avec de vraies données quand c'est possible, jugés visuellement.
2. **Verdict + score d'ennui.** L'utilisateur désigne le gagnant (A/B, ou « challenger mieux / champion reste ») **ET donne un score d'ennui 0–3** (voir plus bas). Une seule question à la fois — demander le score d'ennui s'il ne l'a pas donné.
3. **Apprentissage (obligatoire).** Claude écrit dans la « Théorie du beau » CE QUI a fait gagner (mouvement, palette, densité, rythme, contraste, hiérarchie, lisibilité, profondeur…) et en tire **une hypothèse falsifiable**.
4. **Recherche.** Claude fait de vraies recherches en ligne (WebSearch/WebFetch) pour nourrir le prochain design : techniques, références primées (Awwwards, Information is Beautiful), principes de visualisation de données et de mouvement.
5. **Nouveau challenger, amplitude pilotée par l'ennui.** Claude conçoit la version suivante qui teste l'hypothèse contre le champion, avec une amplitude de variation dictée par le score d'ennui. Retour à l'étape 1.

Le champion reste tant qu'un challenger ne l'a pas battu. Toujours **afficher challenger et champion côte à côte** (captures + liens) pour le verdict.

## Critère de fond — beauté UTILE, pas beauté pure

Un visuel n'a de valeur que s'il **aide à lire et comprendre les données**, pas juste s'il est beau. Les effets purement décoratifs (pulsations, fils arbitraires, grain…) qui n'encodent AUCUNE donnée valent zéro en compréhension.
- **Chaque élément visuel encode un vrai signal** des données (catégorie, importance, fraîcheur, volume, rareté, parcours de lecture). Les données d'abord ; l'ambiance habille, elle ne remplace pas.
- Ne pas fabriquer de relations qui n'existent pas dans les données et les vendre comme du sens.
- Le juge pèse dans cet ordre : **1) ça aide à comprendre ? 2) c'est beau ?** La « Théorie du beau » devient « Théorie de la beauté utile ».

## Score d'ennui (0–3) — pilote l'amplitude de variation

L'utilisateur donne ce score à chaque round. Il règle **à quel point le prochain challenger doit s'éloigner du champion** (exploitation ↔ exploration) :

| Score | Sens | Consigne de design |
|---|---|---|
| **0** | Pas ennuyé, la piste est bonne | Micro-variation : raffine un seul paramètre autour du champion. |
| **1** | Un peu | Variation modérée sur l'axe qui paie actuellement (même dimension, pas plus). |
| **2** | Assez | Change de dimension/levier (structure → ambiance → couleur → mouvement → sens…), garde le squelette gagnant. |
| **3** | Max, ça lasse | **Varier fortement le contenu et la direction** : nouvelle métaphore visuelle, nouveau plan, nouvelle idée — quitte à casser le squelette du champion. |

Règle : **l'ennui prime sur l'inertie**. Un ennui à 2–3 impose de bifurquer même si un axe gagnait ; un ennui à 0 interdit les grands sauts.

### Ne pas abandonner une innovation aimée
Piège classique : à ennui 3, on innove ; l'utilisateur aime l'IDÉE mais garde l'ancien champion pour sa structure ; au tour suivant (ennui 0), on revient à un simple retouche du champion → **il le vit comme un recul**.
- **Une idée innovante aimée doit être PROLONGÉE et développée**, même si elle a perdu ce round-là. L'innovation garde son élan.
- **À ennui élevé, innover vraiment et durablement** : un nouveau comportement visible, pas un raffinement cosmétique. La rupture peut se faire SUR le squelette gagnant.
- Quand un acquis (la structure) et une idée aimée (la vie, les liens) coexistent, **les marier hardiment**, ne pas sacrifier l'un à l'autre.

## Règles dures

- **Tenir la « Théorie du beau » à jour** dans un fichier du projet (`THEORIE-DU-BEAU.md`, versionné v0 → v1 → v2…). C'est le cœur du système, pas un journal optionnel.
- **Jamais de design au hasard** : chaque challenger = une hypothèse explicite issue du dernier verdict + recherche.
- **Une seule question à la fois** à l'utilisateur ; propager la règle à tout sous-agent.
- **Vérifier avant de montrer** : test automatique sans fenêtre (navigateur headless) → zéro erreur console, puis capture d'écran lue avant d'envoyer.
- **Livrable** = un fichier autonome (HTML, sans dépendance réseau) + une capture PNG pour le jugement rapide.

## Test sans fenêtre (rappel)

```bash
node -e 'const p=require("puppeteer");(async()=>{const b=await p.launch({headless:"new",args:["--no-sandbox"]});const pg=await b.newPage();await pg.setViewport({width:1280,height:800});const e=[];pg.on("console",m=>{if(m.type()=="error")e.push(m.text())});pg.on("pageerror",x=>e.push("PE:"+x.message));await pg.goto("file://"+process.cwd()+"/FICHIER.html",{waitUntil:"load"});await new Promise(r=>setTimeout(r,1500));await pg.screenshot({path:"SORTIE.png"});console.log(e.length?e.join(" | "):"OK");await b.close()})()'
```
(`npm i puppeteer` d'abord.)

## À la fin de chaque round

Mettre à jour le fichier de suivi : champion, hypothèse testée, verdict, score d'ennui, liens, « Théorie du beau » incrémentée.
