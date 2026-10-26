---
name: debug-xr
description: Use when the user débogue un comportement XR/VR qui ne marche pas dans Unity (Meta Quest, Meta XR SDK, Interaction SDK, Building Blocks) — locomotion, téléport, rayon, UI world-space, manettes, hand tracking, rig, interactors, ActiveState. Déclencheurs — "/debug-xr", "ça marche pas en VR", "le rayon/le téléport/le menu ne marche pas", "regarde la doc et la scène", "fais des allers-retours". Rôle — imposer la boucle qui a fait ses preuves : la bible Meta AVANT le code, la comparaison au prefab de référence du SDK, une sonde persistante qui écrit ses mesures, et une mesure discriminante par hypothèse pour qu'UN SEUL run tranche.
---

# debug-xr — la boucle de débogage XR

## Pourquoi ce skill existe

Le XR pénalise trois réflexes qui marchent partout ailleurs :

1. **Lire le code ne suffit pas.** Un composant peut être correctement configuré et
   inerte au runtime, éteint par un `ActiveState` invisible dans l'inspecteur.
2. **Deviner coûte cher.** Chaque hypothèse fausse consomme un Play, et le Play
   appartient à l’utilisateur — c'est lui qui met le casque.
3. **Corriger sans instrumenter est indétectable.** Le reproche typique : *« tu mets des logs
   à chaque fois pour étudier l'évolution ? tu monitores les changements ? il n'y a aucun
   changement perceptible ! »*

Ce skill transforme le débogage en une boucle où **chaque run rapporte plus d'information
que le précédent**, et où chaque correction laisse une trace mesurable.

## La règle qui prime sur tout

**Le Play appartient à l’utilisateur.** Ne jamais le lancer ni l'arrêter à sa place quand il
teste au casque. Quand une mesure est finie, le dire et attendre. Si l’utilisateur dit
explicitement « fais des allers-retours », alors et seulement alors piloter le Play soi-même
via `unity-mcp` — et systématiquement `manage_editor stop` avant de lui répondre.

## La boucle

### 1. La bible avant le code

Avant de câbler, de configurer, d'inventer un composant, ou **d'affirmer un comportement
du SDK** :

```bash
grep -i "<mots>" ~/.claude/meta-doc/llms.txt     # environ 2 600 pages, instantané
```

puis `WebFetch` de l'URL `.md` trouvée, avec une question précise.

Le déclencheur n'est PAS le doute. **Se sentir sûr est justement l'état où l'on ne vérifie
pas, donc celui où l'on se trompe sans le voir.** « Meta fournit-il déjà ça ? » se tranche
par une recherche, jamais par intuition.

Quand la doc ne répond pas (c'est fréquent sur les détails d'implémentation), ne pas
inventer : passer à l'étape 2, qui est plus fiable que la doc.

### 2. Comparer au prefab de RÉFÉRENCE du SDK

**C'est l'étape la plus rentable, et la plus souvent oubliée.** Le SDK embarque des prefabs
de référence : ce sont eux la vérité d'implémentation, pas la doc.

```
Library/PackageCache/com.meta.xr.sdk.interaction.ovr@*/Runtime/Prefabs/
Library/PackageCache/com.meta.xr.sdk.interaction@*/Runtime/UnityXR/Prefabs/
```

Chargeables via `AssetDatabase.LoadAssetAtPath("Packages/com.meta.xr.sdk.interaction.ovr/...")`.

Diffe **structure + configuration sérialisée** entre le prefab du projet et celui de Meta,
sur le sous-arbre concerné. Deux issues, toutes deux utiles :

- **Divergence** → tu as ta cause, et la référence te donne la valeur à remettre.
- **Identique** → tu viens d'éliminer tout le prefab d'un coup. Le défaut est ailleurs
  (alimentation, scène, code projet). C'est un résultat, pas un échec.

Lire la configuration par `SerializedObject` + `GetIterator()`, pas à l'œil : les champs
qui comptent (`_thresold`, `_comparison`, `_checkAxis`, les `Inject*`) ne sont pas tous
visibles dans l'inspecteur.

### 3. Lire le code source du SDK quand la sémantique est en jeu

Un champ nommé `_thresold = (0.00, 0.25)` avec `_comparison = Less Than` ne se devine pas.
Le `PackageCache` contient les sources : les lire tranche en trente secondes ce qu'une
hypothèse laisse ouvert pendant trois runs.

### 4. Une sonde persistante, pas des Debug.Log

Un `Debug.Log` se perd dans la console. Une **sonde** écrit une ligne d'état par échantillon
dans `evidence/<sujet>.log`, avec des mesures nommées, et survit aux sessions.

Principes :

- **Posée à la main dans la scène.** Jamais de `RuntimeInitializeOnLoadMethod` pour un
  outil de diagnostic : l'auto-bootstrap crée exactement le genre d'effet de bord invisible
  qu'on est en train de traquer.
- **Une mesure = un nom court en français**, lisible d'un coup d'œil sur une ligne dense :
  `rayons=2 hover=1 cible=X murM2=8.29 tp=1/9 porteTP=False`.
- **Compter actifs/total**, pas seulement actifs : `tp=1/9` dit autre chose que `tp=1`.
- **Horodater et marquer les démarrages de scène** pour découper les runs.

### 5. La mesure discriminante

Avant de demander un run, écrire les hypothèses concurrentes et **ce que chacune produirait
comme ligne de journal**. Si deux hypothèses donnent la même ligne, la sonde est
insuffisante : l'enrichir AVANT de faire tourner.

Exemple réel :

| Ligne observée | Ce qu'elle élimine |
|---|---|
| `stickD=(0.33,0.94)` + `axeISDK=(0.00,0.00)` | le stick est lu par OVRInput mais pas par l'ISDK → défaut d'alimentation du controller |
| `axeISDK=(0.33,0.94)` + `porteTP=False` | l'ISDK voit le stick, la porte ne s'ouvre pas → seuil ou ActiveState |
| `porteTP=True` + `fermeTP=Interactor:True` | la porte s'ouvre puis se referme → un autre interactor engagé |

Deux chaînes d'entrée coexistent presque toujours en Meta XR (`OVRInput` d'un côté,
`IController`/`ControllerRef` de l'ISDK de l'autre). **Mesurer les deux** : leur divergence
est une cause fréquente et invisible autrement.

### 6. AVANT tout test de l’utilisateur : un PARCOURS DE LOGS sur ce qu'on teste

**Règle absolue et non négociable : on ne demande JAMAIS à l’utilisateur de tester
sans avoir d'abord posé une série de logs qui couvre, maillon par maillon, la
fonctionnalité précise qu'on est en train de déboguer.** Pas l'état général : le chemin
de CE qu'on teste, du geste jusqu'à l'effet.

Le test de sortie, avant d'écrire « teste » : *« si ça échoue, le journal me dira à quel
maillon exactement ? »* Si la réponse est non, **l'instrumentation n'est pas finie et on ne
demande pas le run**. Poser un correctif puis envoyer l’utilisateur au casque « pour voir », c'est
exactement ce qu'il refuse — et ça brûle un run pour rien.

Un état n'est pas un parcours. `porteTP=False` dit *où on en est*, pas *jusqu'où on est
allé*. Deux mesures aux extrémités (`pinceMajeur=0` … `tpMain=0/2`) laissent tout le milieu
muet : impossible de dire si c'est le seuil du geste, la condition d'angle, ou le gate.

**Écrire la chaîne causale d'abord, l'instrumenter ensuite, à chaque maillon :**

```
entrée physique → lecture SDK → condition/ActiveState → porte → interactor
    → interactable → événement émis → effet sur le joueur
```

Exemple, pour le téléport aux mains :

```
force du pincement → composant déclencheur → VirtualActiveState.Active
  → WristAngle → ActiveStateGate → interactor téléport → arc → cible
```

Chacune de ces flèches est un log. Aucune ne doit manquer.

Concrètement :
- **Une sonde persistante, pas des `Debug.Log` épars** (cf. §4) : le journal doit survivre
  au run et se relire. Un `Debug.Log` noyé dans la console ne se compare pas d'un run à
  l'autre.
- **S'abonner aux événements**, pas seulement échantillonner des booléens. Les UnityEvent
  et les `WhenStateChanged` du SDK disent *quand* et *dans quel ordre* — un échantillonnage
  à 0,5 s rate une transition de trois frames.
- **Journaliser les valeurs CONTINUES, pas seulement les seuils franchis.** `pinceMajeur=0`
  ne dit rien ; `forceMajeur=0,30` dit que le geste est fait mais n'atteint pas le seuil.
  La valeur brute distingue « pas de geste » de « geste trop faible ».
- **Un maillon muet est un maillon suspect** : si la trace s'arrête au maillon 4, on sait
  que 1-3 fonctionnent. C'est ça, gagner un run.

**Red flag** : je m'apprête à écrire « Play : teste ceci » alors que je n'ai pas ajouté de
log depuis mon dernier correctif → STOP, instrumenter d'abord.

### 7. Instrumenter le changement qu'on vient de faire

Règle non négociable. Après chaque correction, la sonde
doit exposer **la grandeur que la correction est censée modifier**, avec sa valeur
attendue avant/après.

> Retaille du collider d'un pont canvas → ajouter `murM2=` à la sonde.
> Avant : `murM2=8.29 hover=2`. Après : `hover=0`. Le journal prouve l'effet.

Sans ça, « rien n'a changé » est indiscernable de « ça a changé mais ailleurs ».

### 8. La preuve a le type du symptôme

- Symptôme **visuel** → la clôture exige une **image** (`manage_camera screenshot`, ou
  `capture_composited_image` de l'operator). Jamais un booléen, jamais un compteur.
- Symptôme **comportemental** → une ligne de journal qui montre la transition.

Verbes autorisés : **« modifié »** (j'ai écrit du code) / **« constaté »** (j'ai produit et
lu l'artefact du bon type) / **« confirmé »** (l’utilisateur l'a vu). Interdit d'écrire
« corrigé » ou « vérifié » sans artefact joint.

## Les deux outils, chacun à sa place

| Outil | Rôle | Usage |
|---|---|---|
| `unity-mcp` | **RÉPARER** | `execute_code` (C# éditeur), prefabs, scènes, `manage_editor play/stop`, `manage_camera screenshot` |
| `meta-xr-operator` | **CONSTATER** | agit en joueur dans l'app qui tourne : `set_controller_input`, `set_head_pose`, `capture_composited_image` |

L'operator n'est joignable que **pendant** un Play VR (`XR Application Server` actif) ;
hors ligne, `metavr xroperator enable` puis Play. Réparer sans constater ne vaut rien.

## Pièges XR spécifiques, déjà payés

- **`com.meta.xr.sdk.interaction` ≠ `com.meta.xr.sdk.interaction.ovr`.** Le premier est le
  backend UnityXR/Input System, le second le backend OVRPlugin. Installer le mauvais donne
  un rig d'apparence correcte et totalement inerte.
- **Les auto-câbleurs runtime écrasent le travail sur la scène.** Un composant en
  `DontDestroyOnLoad` qui re-scanne toutes les N secondes recrée ce que tu viens de
  supprimer : tes modifications de scène semblent sans effet. Chercher
  `RuntimeInitializeOnLoadMethod` et les `Update` qui recâblent **avant** d'éditer une scène.
- **Un pont Ray↔Canvas pose une surface plein rect.** Sur un HUD qui suit le joueur, c'est
  un mur invisible qui capte les rayons en permanence et verrouille en cascade la
  locomotion et le téléport. Retailler la surface sur les seuls éléments interactifs.
- **Un `ActiveStateTracker` qui éteint un GameObject au repos est le design normal**, pas
  un bug. Ne pas « réparer » en forçant l'objet actif : chercher pourquoi la porte ne
  s'ouvre pas.
- **Un raycast vers le bas touche la capsule du joueur.** Trier les hits et ignorer tout
  collider enfant de la racine du joueur.
- **Ne jamais toucher le `localScale` d'un prefab source FBX** : les FBX portent souvent
  0.01, le remettre à 1 donne des objets à l'échelle 100.
- **Lancer une scène de jeu seule ne charge pas son environnement chargé en additif** : pas de sol, donc
  chute. Un symptôme observé dans ce montage est un artefact, pas un bug.

## Ce qu'il ne faut jamais faire

- Enchaîner des corrections devinées entre deux runs.
- Demander un run sans savoir quelle ligne de journal tranchera.
- Conclure « ça marche » sur des logs d'initialisation.
- Écrire dans un commentaire un chiffre non mesuré (le commentaire devient une fausse
  source de vérité pour la session suivante).
- Répondre à l’utilisateur pendant qu'un Play lancé par soi tourne encore.

## Boucle, en une ligne

**bible → prefab de référence → source SDK → sonde enrichie → UN run discriminant →
correction instrumentée → artefact du bon type.**
