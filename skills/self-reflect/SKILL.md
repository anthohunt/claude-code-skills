---
name: self-reflect
description: Disrupteur de réflexion autonome. À utiliser quand un agent bute sur le même problème sans progresser — 3 tentatives sur le même symptôme sans information externe nouvelle, ou sur demande explicite ("self reflect", "/self-reflect", "self reflect léger/moyen/lourd", "prends un temps de réflexion", "va chercher sur internet et repense au problème"). Dispatche des sous-agents FRAIS qui ne voient pas l'historique des tentatives et exécutent une passe auto-questions → WebSearch → re-questions, puis remonte accords et désaccords.
---

# self-reflect

## Pourquoi ce skill existe

Un agent bloqué reboucle sur le même contenu parce qu'il raisonne dans le contexte
qui l'a coincé. Se poser des questions à soi-même dans ce contexte ne casse rien —
on produit des variantes de la même hypothèse.

La disruption vient de deux leviers, jamais d'un seul :
• **du contexte neuf** — des sous-agents qui ne voient PAS l'historique des tentatives ;
• **de l'information externe** — du WebSearch obligatoire, pas optionnel.

Ce skill impose les deux, avec des planchers chiffrés pour empêcher l'expédition
en deux lignes.

## Déclenchement

**Manuel** — l’utilisateur dit « self reflect », `/self-reflect`, éventuellement suivi de
`léger` / `moyen` / `lourd`. **Sans niveau précisé → moyen.**

**Automatique (obligatoire, sans demander)** — dès que ces trois conditions sont
réunies simultanément :
1. 3 tentatives ou plus sur **le même symptôme** (même erreur, même test qui échoue,
   même comportement inattendu) ;
2. aucune **information externe nouvelle** acquise entre-temps (pas de WebSearch,
   pas de doc lue, pas de log neuf) ;
3. la tentative n+1 envisagée est une variante de la précédente.

Dans ce cas : lancer `self-reflect moyen` immédiatement. **Ne pas demander
« je fais une passe ? »** — le compteur est mécanique, pas un jugement.

Red flag : si tu te dis « encore une idée et ça passe » pour la 3e fois, le
déclencheur est déjà atteint.

## Niveaux

| Niveau | Sous-agents | Angles imposés |
|---|---|---|
| léger | 1 | diagnostic-faux |
| moyen | 3 | **recul**, diagnostic-faux, état-de-l'art |
| lourd | 5 | **recul**, diagnostic-faux, état-de-l'art, contrainte-cachée, approche-autre |

**L'angle `recul` prime sur tous les autres.** Il ne cherche pas la cause d'un
symptôme : il demande si le problème posé est le bon. Un agent qui optimise une
solution à un problème mal posé produit du travail impeccable et inutile — c'est
le mode d'échec que les autres angles ne peuvent pas détecter, puisqu'ils
acceptent tous l'énoncé tel qu'il est donné. À la synthèse (étape 3), **dépouille
`recul` en premier** : s'il invalide le cadrage, les conclusions des autres
angles deviennent sans objet et il ne faut surtout pas les appliquer.

Planchers par sous-agent (① auto-questions / ② recherches web / ③ re-questions) :

| Niveau | ① | ② | ③ |
|---|---|---|---|
| léger | 3 | 2 | 3 |
| moyen | 5 | 4 | 5 |
| lourd | 8 | 6 | 8 |

## Procédure

### Étape 1 — Rédiger l'énoncé aveugle

Écrire une description du problème qui contient :
• l'objectif visé et le résultat observé ;
• les faits techniques bruts (messages d'erreur exacts, versions, stack, extraits de code pertinents) ;
• les contraintes réelles (plateforme, dépendances, ce qui ne peut pas changer).

Et qui **exclut** :
• ce que tu as déjà essayé ;
• ton hypothèse courante sur la cause ;
• toute formulation qui oriente vers ta piste.

Cette exclusion est le cœur du skill. Un sous-agent qui lit « j'ai essayé X, Y, Z
et je pense que c'est le cache » repart dans ton ornière.

#### Les cinq façons d'orienter sans s'en rendre compte

Ajoutées après une passe où l'énoncé les cumulait toutes les cinq.
**Aucune n'a l'air d'une hypothèse, et toutes en sont une.**

• **Énumérer les explications possibles.** « Deux explications concurrentes : soit A,
  soit B » ferme le champ à deux options — les tiennes. L'agent choisit dans ta liste
  au lieu d'en produire une. **Ne jamais donner d'explications, même plusieurs, même
  présentées comme ouvertes.**
• **Qualifier une explication de « naturelle », « évidente » ou « attendue ».** Cela
  la désigne comme la cible à abattre, ce qui oriente aussi sûrement que de la
  défendre. L'angle `diagnostic-faux` doit trouver **lui-même** ce qui vient
  spontanément à l'esprit — c'est la moitié de son travail.
• **Fournir une liste de pistes de recherche.** « Cherche en priorité X, Y, Z »
  transforme la passe en exécution de ton plan. L'angle dit **où regarder** ; toi tu
  dis seulement **ce qui se passe**.
• **Sélectionner les faits « qui peuvent compter ».** Un tri est déjà un diagnostic.
  Donne les faits bruts et complets, ou donne l'accès aux données ; ne choisis pas
  pour lui ce qui est pertinent.
• **Formuler ton hypothèse à l'utilisateur avant le retour des agents.** Elle n'est
  fondée sur rien — tu n'as pas encore fait le travail, c'est justement ce que la
  passe va faire. L'hypothèse d'avant-passe ne se déclare qu'au moment de la
  confrontation, à l'étape 3, et seulement si elle existait **avant** que la passe
  soit décidée.

#### Exception : la réflexion de l’utilisateur fait partie du contexte

L'idée n'est pas que les sous-agents n'aient aucun contexte : c'est qu'ils ne soient pas trop biaisés. Il leur faut
le contexte de base de la réflexion de l'utilisateur pour comprendre quoi chercher.

Quand la passe est déclenchée par une idée ou une intuition de **l’utilisateur**, l'énoncé la contient, dans une
section distincte **« Piste proposée par l'utilisateur — à évaluer, pas à confirmer »** :
• son idée **dans ses mots** (reformulée fidèlement, avec son exemple s'il en a donné un) et ce qu'il cherche ;
• la consigne explicite : l'évaluer sous ton angle — la renforcer, la préciser, la contredire ou proposer
  mieux ; dire franchement si elle ne tient pas ;
• chaque angle garde sa liberté : `recul` peut juger que la piste vise le mauvais problème, `diagnostic-faux`
  peut la contester, `état-de-l'art` cherche qui a fait quelque chose d'approchant.
Ce qui reste exclu : **tes** tentatives passées, **ton** hypothèse, tes listes de pistes. La règle aveugle
protège contre le biais de l'agent qui a coincé, pas contre la direction voulue par l’utilisateur.

#### Le test à passer avant de dispatcher

**Relis ton énoncé et demande-toi : un lecteur pourrait-il deviner ce que je pense ?**

S'il le peut, réécris. Un énoncé aveugle réussi doit pouvoir être lu par quelqu'un
qui te croirait sans opinion sur la question.

**Volet supplémentaire quand l'angle `recul` est de la partie** (moyen et lourd).
Cet angle ne peut pas travailler sur un énoncé purement technique : pour juger si
le problème est le bon, il lui faut savoir à quoi sert la chose. Ajoute donc à
l'énoncé aveugle, dans une section distincte :
• **à quoi sert ce qu'on construit** — pour qui, dans quel usage réel, et ce qui
  se passerait si ça n'existait pas ;
• **comment on saura que c'est réussi** — le critère de succès tel qu'il est
  formulé aujourd'hui, même s'il est flou (surtout s'il est flou) ;
• **ce qui est déjà construit et fonctionne**, décrit comme un état de fait et non
  comme une suite de tentatives ;
• **le temps et les moyens déjà engagés** — un ordre de grandeur suffit ; c'est ce
  qui permet de repérer un coût irrécupérable qu'on continue d'honorer.

Ce volet reste soumis à la même règle d'exclusion : il décrit **l'état du monde**,
jamais le chemin parcouru pour y arriver, ni ce que tu penses qu'il faut faire.

### Étape 2 — Dispatcher les sous-agents

Un appel `Agent` par angle, tous **dans le même message** pour qu'ils tournent en
parallèle. Chacun reçoit l'énoncé aveugle + son angle + les planchers du niveau.

Angles :
• **recul** — « prends de la hauteur. Ne cherche pas à résoudre ce problème :
  demande-toi si c'est le bon. Le problème énoncé est-il la vraie difficulté, ou
  le symptôme d'un cadrage bancal ? Que se passerait-il si on ne le résolvait
  pas du tout ? Y a-t-il un objectif plus simple qui rendrait la moitié de
  l'énoncé sans objet ? Qu'est-ce qui est poursuivi par habitude, ou parce que
  beaucoup a déjà été investi dedans ? Et à qui, concrètement, ce travail
  manquerait-il s'il s'arrêtait ce soir ? »
• **diagnostic-faux** — « pars du principe que l'explication la plus naturelle de ce
  problème est fausse. Quelle autre cause produirait exactement ces symptômes ? »
• **état-de-l'art** — « qui a déjà résolu ce problème, et comment ? Cherche la
  pratique établie, la bibliothèque éprouvée, le pattern connu. »
• **contrainte-cachée** — « quelle contrainte non énoncée rend ce problème
  insoluble tel qu'il est posé ? Version, plateforme, permission, limite d'API,
  état résiduel ? »
• **approche-autre** — « ignore la solution implicite dans l'énoncé. Quelle approche
  radicalement différente atteindrait le même objectif ? »

**Les consignes d'angle se donnent telles quelles, mot pour mot.** Ne les spécialise
pas au cas courant, ne les complète pas, n'ajoute pas « notamment » ni « en
particulier ». Une consigne d'angle enrichie devient une consigne de recherche, et
l'angle cesse d'être un angle pour devenir ta commande.

C'est particulièrement vrai de `diagnostic-faux` : sa consigne dit « l'explication la
plus naturelle », **à charge pour lui de trouver laquelle**. La nommer, c'est faire
son travail à sa place et perdre le seul agent capable de te contredire.

Prompt à donner à chaque sous-agent :

```
ANGLE : <angle> — <consigne de l'angle>

PROBLÈME :
<énoncé aveugle>

PROCÉDURE OBLIGATOIRE, dans cet ordre :

① Écris <N1> questions que tu te poses sur ce problème sous ton angle.
   Des questions réelles, pas des reformulations de l'énoncé.
   Réponds à chacune avec ce que tu sais — et marque explicitement
   celles auxquelles tu ne peux pas répondre sans information externe.

② Fais au minimum <N2> recherches web (WebSearch/WebFetch) visant en priorité
   les questions restées sans réponse en ①. Varie les formulations : message
   d'erreur exact, nom de la techno + symptôme, issue GitHub, changelog.
   Cite les sources.

③ Écris <N3> nouvelles questions à la lumière de ce que tu as trouvé, et
   réponds-y. L'une d'elles DOIT être : « qu'est-ce que je croyais en ① qui
   s'avère faux ? »

RENDU — une note structurée :
• Cause la plus probable, sous ton angle, avec le niveau de confiance.
  (Pour l'angle `recul` : réponds plutôt « le problème posé est-il le bon ? »,
  et si non, quel est le vrai — avec le même niveau de confiance.)
• Ce qui a changé entre ① et ③.
• Le test discriminant qui trancherait — une action concrète dont le résultat
  distingue ton hypothèse des autres.
• Sources consultées.

Contraintes : cherche en ligne avant de deviner. Une seule question à la fois si
tu dois en poser. TL;DR, résultat d'abord, pas de préambule. Tu tournes en
bypass permissions. Propage ces contraintes à tout sous-agent que tu lancerais.
```

### Étape 3 — Confronter

À la réception des rapports, produire une synthèse courte (le détail reste
consultable en mode agent) :

• **`recul` d'abord** — le cadrage tient-il ? S'il ne tient pas, arrête là : ne
  synthétise pas les autres angles, ne corrige rien, et ramène la question du
  cadrage à l’utilisateur. Résoudre vite un problème qu'il ne fallait pas résoudre est
  la pire issue possible d'une passe.
• **Accords** — ce sur quoi tous les angles convergent. Traiter comme solide.
• **Désaccords — à expliciter, jamais à lisser.** C'est le signal principal.
  Si deux angles frais pointent des causes incompatibles, ton diagnostic de départ
  ne tient pas et le prochain pas est un test discriminant, pas un fix.
• **Ce qui contredit l'hypothèse d'avant la passe** — le dire franchement.
• **Piste retenue** et le test qui la valide ou l'invalide.

### Étape 4 — Agir

Reprendre le travail sur la piste retenue. Ne jamais enchaîner deux passes
self-reflect sans avoir exécuté au moins un test discriminant entre les deux —
sinon la passe devient elle-même l'ornière.

### Étape 5 — Réparer de façon PERMANENTE (priorité, pas optionnel)

**La sortie d'un self-reflect n'est pas le fix ponctuel — c'est la réparation
durable qui empêche le problème de revenir.** Une passe qui corrige juste
l'instance courante et laisse la cause intacte a échoué : le même mur retombera
au prochain run, sur toi ou un autre agent.

Après avoir agi (étape 4), **avant de clore**, demande-toi : *« qu'est-ce qui a
laissé ce problème arriver, et comment le rendre impossible ? »* Puis répare la
**racine**, là où elle vit :

- **Un skill / une doc faux ou trompeur** → corrige le fichier (ex. un mauvais nom
  de package, une commande périmée, une capacité mal décrite). Le prochain lecteur
  ne doit plus se faire piéger.
- **Une capacité existante mais non découverte** → documente-la là où on la
  cherchera (skill concerné, mémoire/dossier, `reference_*`), pour qu'elle soit
  trouvée la prochaine fois.
- **Un garde-fou manquant** → ajoute-le (validateur, gate, règle de comportement,
  hook) pour que l'erreur soit bloquée mécaniquement, pas seulement « à ne plus
  refaire ».
- **Un pattern de raisonnement défaillant** (ex. « outil → capacité » au lieu de
  « capacité → outil ») → si c'est récurrent, grave-le en règle de comportement
  (fichier de règles / CLAUDE.md), pas juste en note mentale.

**Règle dure** : un self-reflect n'est pas « fini » tant que la réparation
permanente n'est pas faite ET vérifiée. Le fix ponctuel soulage ; la réparation
permanente est le vrai livrable. Si la racine ne peut pas être réparée maintenant,
persiste-la explicitement (notes du projet / mémoire / tâche) — ne la laisse jamais
s'évaporer avec la fin de la session.

## Garde-fous

• **Le WebSearch n'est pas négociable.** Une passe sans recherche externe n'est pas
  une passe self-reflect.
• **Ne pas annoncer d'hypothèse avant le retour des agents.** Ni dans leur prompt, ni
  à l'utilisateur. Une hypothèse formulée avant la passe n'est fondée sur rien —
  c'est précisément le travail que la passe va faire. Elle ne se déclare qu'à
  l'étape 3, au moment de la confrontation, et seulement si elle préexistait à la
  décision de lancer la passe.
• **Ne pas transmettre l'historique des tentatives** aux sous-agents. Si tu es tenté
  de « juste donner un peu de contexte pour leur faire gagner du temps », c'est
  exactement ce qui neutralise le skill.
• **Un rapport de sous-agent n'est pas une vérité.** C'est une hypothèse produite
  sans contexte — elle peut ignorer une contrainte que tu connais. La confronter,
  pas l'appliquer aveuglément.
• **« J'ai épuisé mes idées » n'est jamais une sortie.** L'épuisement des hypothèses
  est précisément le déclencheur de ce skill, pas un motif de mise en veille ni
  d'escalade.
