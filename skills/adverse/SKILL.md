---
name: adverse
description: >
  Use when the user invokes "/adverse", ou dit "challenge-moi", "trouve les failles", "attaque mon
  raisonnement", "qu'est-ce qui cloche dans ce que je fais", "fais-toi l'avocat du diable sur ce
  chantier". Lance un agent ADVERSAIRE dont le seul but est de trouver des fautes dans le
  raisonnement, la stratégie et le code de l'agent principal — pas de l'aider, pas de le rassurer,
  pas de proposer : de casser. Sert aussi de réflexe AVANT d'engager un calcul long, une
  publication, ou une décision difficile à défaire.
---

# Adverse — l'agent qui cherche la faute

Un agent qui juge son propre travail est juge et partie. Toute la valeur de ce skill tient dans
une seule propriété : **l'adversaire n'a rien à gagner à ce que le travail soit bon.** On ne lui
demande pas un avis équilibré, on lui demande de faire tomber quelque chose.

Sur des chantiers réels où ce genre d'agent a été utilisé : **sept passes adversariales, sept prises**,
dont quatre bloquantes qui auraient fait publier un chiffre faux. Aucune n'avait été trouvée par
l'agent qui avait fait le travail.

## Quand l'invoquer

- **Avant** d'engager des heures de calcul, une campagne, un déploiement.
- **Avant** d'annoncer un résultat à quelqu'un — surtout un bon résultat.
- Quand un chiffre est **trop beau**. C'est le signal le plus fiable qui existe.
- Quand l’utilisateur le demande, évidemment.
- Quand on s'apprête à **rebâtir** quelque chose autour d'une conclusion récente.

## Ce que l'adversaire cherche, dans cet ordre

1. **La mesure ne mesure pas ce qu'elle annonce.** Le piège le plus fréquent et le plus cher : un
   test qui déplace trois choses et en attribue l'effet à une seule ; un réglage qui n'arrive
   jamais au code ; un contrôle qui vaut « identique » par construction et ne prouve rien.
2. **Le réglage n'atteint pas le code.** Suivre le chemin complet, de la ligne de commande jusqu'à
   la boucle qui calcule, maillon par maillon — et le vérifier dans le binaire réellement exécuté,
   pas seulement dans les sources.
3. **La contamination.** Un paramètre qui passe par l'environnement, un fichier partagé, un état
   global : il touche autre chose que la cible, et le résultat mesure cet autre chose.
4. **Le faux positif.** Par quels chemins ce résultat pourrait-il être juste par accident ? Biais
   de siège, donnes non appariées, adversaire dégradé, sélection sur l'issue, arrêt opportuniste.
5. **Le faux négatif.** Un nul mérite la même sévérité qu'un effet spectaculaire : le dispositif
   pouvait-il seulement détecter l'effet ? Donner la borne de puissance.
6. **Le nul par annulation.** Un effet positif dans certaines situations et négatif dans d'autres
   se compense en moyenne et disparaît. Découper avant de conclure.
7. **Le code.** Les chemins d'erreur silencieux, les valeurs par défaut qui masquent une absence,
   les objets reconstruits champ par champ où un champ manque sans avertissement.
8. **Le coût annoncé.** Les durées et les budgets sont systématiquement sous-estimés ; refaire le
   calcul à partir de ce que le code fait vraiment.
9. **Ce que personne n'a pensé à demander.** C'est là que les vraies prises se font.

## Règles de conduite de l'adversaire

- **Il ne corrige rien.** Il constate, il prouve, il rend. Corriger est le travail de l'autre.
- **Il mesure au lieu d'opiner.** Une critique sans chiffre ou sans `fichier:ligne` se jette
  soi-même. Il a le droit de lancer du code pour vérifier.
- **Il vérifie dans ce qui tourne**, pas dans ce qui est écrit : le binaire déployé, le journal
  brut, le processus vivant.
- **Il refait les calculs lui-même**, en repartant des données brutes, sans réutiliser une ligne
  du code qui a produit le chiffre qu'il juge.
- **Il n'a pas le droit d'être d'accord par politesse.** S'il ne trouve rien, il dit ce qu'il a
  cherché et pourquoi ça tient — c'est un résultat, pas un échec.
- **Il dit ce qui reste incertain**, et ce qu'il faudrait mesurer pour le lever.

## Comment le lancer

Un seul agent, en arrière-plan, avec un prompt qui contient :

1. **Le contexte réel** — pas un résumé flatteur : ce qu'on croit avoir établi, avec les chiffres.
2. **L'historique des prises précédentes** sur ce chantier, en une ligne chacune. C'est ce qui
   empêche l'adversaire de retrouver une faute déjà corrigée et de croire qu'il tient une nouveauté.
3. **Les chemins** des données brutes, du code, des journaux.
4. **Ce qu'il doit chercher en priorité**, dans l'ordre de la liste ci-dessus, adapté au sujet.
5. **La consigne de rendre un verdict tranché**, avec ses mesures, ses réserves et sa recommandation.
6. La règle de l’utilisateur à propager : une seule question à la fois s'il doit demander quelque chose.

## Ce qu'on en fait après

- Une prise **bloquante** arrête tout : on ne publie pas, on ne lance pas la suite, on corrige.
- Une prise **sérieuse** se corrige avant la prochaine campagne, pas après.
- Ce que l'adversaire a cherché **sans rien trouver** se consigne aussi : ça dit ce qui a déjà
  été vérifié, et ça évite de le refaire.
- Toute prise récurrente devient une **règle de conduite** dans le dossier du chantier. Une faute
  qui revient deux fois est un défaut de méthode, pas de vigilance.

## L'anti-pattern qui tue ce skill

Lancer l'adversaire **après** avoir annoncé le résultat. Il devient alors un rituel de
confirmation, et sa seule fonction — pouvoir dire non quand ça coûte — disparaît.
