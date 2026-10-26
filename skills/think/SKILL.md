---
name: think
description: Use quand l’utilisateur invoque "/think", ou dit "réfléchis bien", "prends le temps", "cherche vraiment", "je veux que tu creuses", "trouve-moi une solution", "on est bloqués sur X", "comment on fait ça". Force un cycle de réflexion LONG sur un problème dont la solution n'est pas évidente : cadrer le vrai problème, produire plusieurs pistes concurrentes, aller chercher sur le web ce que d'autres ont déjà résolu, éliminer par preuve et pas par intuition, et ne rendre qu'une recommandation défendable. Distinct de self-reflect (débloquer un agent qui boucle) et de mission (boucle d'exécution goal-driven).
---

# Think — creuser avant de répondre

Le réflexe par défaut est de répondre avec la première solution plausible. Sur un problème
difficile, cette première solution est presque toujours la solution du problème **voisin** —
celle qui ressemble à ce qu'on a déjà vu, pas celle qui traite le cas présent.

**La règle qui commande tout : aucune recommandation ne sort tant qu'elle n'a pas survécu à une
alternative sérieuse et à ce que le web sait déjà du problème.**

Ce mode coûte du temps et des tokens. C'est le but. L’utilisateur l'invoque quand la mauvaise réponse
coûte plus cher que l'attente.

---

## Les cinq passes

### Passe 1 — Cadrer le vrai problème

Avant de chercher une solution, s'assurer qu'on cherche la bonne chose.

- **Reformuler le problème en une phrase**, sans le vocabulaire de l’utilisateur. Si la reformulation
  est impossible, le problème n'est pas compris — c'est ça qu'il faut dire.
- **Séparer le symptôme de la cause.** « Le build est lent » est un symptôme. « On recompile
  toute la lib à chaque changement de test » est un problème.
- **Nommer la contrainte dure.** Budget, délai, infra existante, compétence disponible, ce qui
  ne peut PAS bouger. Une solution qui viole une contrainte dure n'est pas une solution.
- **Nommer le critère de succès.** À quoi on saura que c'est résolu. S'il n'existe pas, le
  demander — une seule question, la plus bloquante.
- **Lire l'état réel** : code, logs, fichiers, dossiers du sujet s'il en existe. Ne jamais raisonner sur une description quand l'artefact est lisible.

### Passe 2 — Produire des pistes concurrentes

**Au moins trois pistes, réellement différentes.** Trois variantes de la même idée n'en font
qu'une.

Angles à couvrir systématiquement, parce que chacun cache une famille de solutions :
- **La solution évidente** — celle qui vient en premier. À écrire, pour pouvoir la battre.
- **La solution qui ne construit rien** — configuration, outil existant, changement d'usage.
  Souvent la bonne, presque jamais la première pensée.
- **La solution qui attaque la cause** et pas le symptôme — plus chère, souvent définitive.
- **La solution du domaine voisin** — comment ce problème est résolu ailleurs (autre stack,
  autre métier, autre échelle).
- **La solution qui supprime le problème** — changer la contrainte au lieu de la satisfaire.

Chaque piste s'écrit avec : ce qu'elle coûte, ce qu'elle suppose vrai, et **ce qui la tuerait**.

### Passe 3 — Aller chercher dehors (obligatoire)

**Ce mode n'est pas complet sans recherche web.** La mémoire d'entraînement est datée et ce
problème a probablement déjà été résolu par quelqu'un.

Ce qu'on cherche, dans cet ordre :
1. **Le problème tel qu'il se nomme dans son domaine** — trouver le terme de l'art. Un problème
   qui a un nom a une littérature.
2. **Les post-mortems et les retours d'échec** — « X doesn't scale », « why we moved off Y »,
   les issues GitHub fermées, les threads HN. Ce qui a raté est plus informatif que ce qui a
   marché.
3. **La doc officielle à jour** de tout outil cité — versions, limites, dépréciations. Ne jamais
   recommander une API de mémoire.
4. **Le contre-exemple** — chercher activement « pourquoi la piste que je préfère est mauvaise ».

Règles de recherche :
- **Plusieurs formulations**, pas une. Le vocabulaire de l’utilisateur n'est pas forcément celui du
  domaine.
- **Dater les sources.** Un billet de 2021 sur un outil qui bouge vaut peu.
- **Ouvrir les pages**, ne pas se contenter des extraits de résultats.
- Pour une recherche large et indépendante, dispatcher des sous-agents `Explore` ou
  `general-purpose` en parallèle — un par piste ou par angle — et ne garder que leurs conclusions.
- **Dire ce qu'on n'a pas trouvé.** Une absence de résultat est une information.

### Passe 4 — Éliminer par preuve

Les pistes ne se départagent pas au feeling.

- **Pour chaque piste, chercher son point de rupture** : la condition précise qui la fait
  échouer, et vérifier si cette condition est vraie ici.
- **Tester quand c'est testable.** Un script de 10 lignes, un `curl`, un prototype jetable dans
  le scratchpad tranche mieux que trois paragraphes d'argumentation. Si un test est possible et
  pas cher, il n'est pas optionnel.
- **Chiffrer.** Ordre de grandeur de temps, de coût, de complexité. Un chiffre grossier bat une
  intuition.
- **Écarter explicitement.** Chaque piste rejetée l'est pour une raison nommée, pas par silence.

### Passe 5 — La passe adversariale

Avant de rendre, attaquer sa propre conclusion.

- **Qu'est-ce qui doit être vrai** pour que la recommandation tienne ? Est-ce vérifié ou supposé ?
- **Quel est le scénario où l’utilisateur revient dans trois semaines** en disant que ça a cassé ?
- **Qu'est-ce que je n'ai pas regardé** — une modalité de recherche non faite, un fichier non
  ouvert, une source non lue ?
- Si le problème est important ou la conclusion fragile : dispatcher un sous-agent **frais**
  (qui ne voit pas le raisonnement) avec pour consigne de **réfuter** la recommandation. Ce qu'il
  trouve devient la passe suivante.
- En cas de blocage persistant malgré tout ça, enchaîner sur `self-reflect`.

---

## Les garde-fous

- **Ne pas s'arrêter à la première piste qui marche.** Une solution qui marche n'est pas une
  solution choisie. Le mode exige au moins une comparaison.
- **Ne pas confondre longueur et profondeur.** Cinq paragraphes de délibération qui n'ouvrent
  aucun fichier et ne lancent aucune recherche ne sont pas de la réflexion.
- **Ne pas laisser le mode devenir un blocage.** Si la réflexion tourne sans converger, rendre
  l'état : ce qui est établi, ce qui bloque, et la question unique qui débloquerait.
- **Pas d'implémentation pendant ce mode.** `/think` produit une recommandation défendue. Le
  code vient après, quand l’utilisateur a tranché — sauf prototype jetable pour départager.
- **Une seule question à la fois** si une clarification est nécessaire.
- Si la recommandation contredit ce que l’utilisateur pensait, l'assumer — enchaîner avec `honest`.

---

## Le format de sortie

Le style concis reste actif : **3 phrases / 3 puces max** sauf si l’utilisateur écrit « détaille ».

Après tout ce travail, ce qui sort tient en :

1. **La recommandation** — une phrase, tranchée.
2. **Le motif décisif** — le fait vérifié qui l'emporte (avec la source si elle vient du web).
3. **Le principal concurrent écarté et pourquoi** — ou la condition à vérifier avant de lancer.

Exemple :
> Passe par un cache de compilation partagé (`sccache`), pas par la parallélisation : le profil
> montre que 80 % du temps part en recompilation de dépendances inchangées, pas en calcul.
> J'ai écarté le découpage en workspaces — même gain, trois jours de refonte au lieu d'une heure.

Le raisonnement complet, les pistes écartées et les sources ne s'affichent que si l’utilisateur écrit
« détaille ». Ils existent, mais ils ne s'imposent pas.
