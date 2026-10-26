---
name: design-on-the-go
description: Mode de travail itératif pour concevoir une UI/visuel avec l’utilisateur en aller-retour rapide. L’utilisateur lâche un retour court ("trop d'infos", "j'aime pas", "trop technique", "plus aéré"), tu DEVINES l'intention et tu construis le changement directement — SANS poser de question. Aperçu live dans Chrome (serveur http local), il rafraîchit (F5). Se déclenche sur "/design-on-the-go", "design on the go", "on bosse le template/le design comme ça", ou quand l’utilisateur dit explicitement qu'il va donner des retours au fil de l'eau et que tu dois guess + construire.
---

# Design on the go — itération visuelle sans friction

## L'esprit (règle d'or)

L’utilisateur conçoit en **regardant**, pas en répondant à des questions. Il lâche un retour bref, tu **interprètes**, tu fais **un changement concret**, il rafraîchit et réagit. Le cycle doit être le plus court possible.

> Consigne type de l'utilisateur : « Arrête de poser des questions : je vais dire des choses, tu devines et tu construis, et on fait des retours comme ça. Si je veux que tu me poses des questions, je te le dirai. »

## Les règles

1. **NE PAS poser de question.** Devine l'intention la plus probable et exécute. Si tu hésites entre deux lectures, prends la plus probable et signale en une ligne l'alternative (« j'ai coupé X ; dis si tu voulais plutôt Y »). L’utilisateur demandera explicitement si jamais il veut que tu poses une question.
2. **Un retour = un changement ciblé.** Pas de refonte massive à chaque mot. Petit, net, réversible. Il construit le design retour après retour.
3. **Annonce en 1-2 lignes ce que tu as changé**, pour qu'il sache quoi regarder en rafraîchissant. Puis stop — laisse-le réagir.
4. **Aperçu live, jamais de renvoi de fichier à chaque tour.** Sers la page sur un http local, ouvre-la dans Chrome une fois ; ensuite il fait F5. (Renvoyer un fichier seulement s'il le demande, ou pour mobile.)
5. **Travaille sur la surface réelle** (le vrai fichier du produit), pas une maquette jetable — comme ça chaque itération validée atterrit directement dans l'outil.
6. **Ne jette rien de vérifié en silence.** Réduire la densité = déplacer/replier l'info (pied de carte, `<details>`), pas la supprimer. Si tu supprimes vraiment, dis-le.
7. **Respecte les préférences durables de l’utilisateur** (règles et mémoire du projet) ; à défaut : pas d'emojis dans les livrables (sauf 1 icône fonctionnelle par callout, cf. `format-notion`), vraies puces, signal d'abord, langage accessible (« trop simple » > « trop technique »).

## Le setup live (à faire une fois en début de session)

```bash
# Servir le dossier du fichier travaillé
cd <dossier-du-fichier>
(curl -s -o /dev/null http://localhost:8765 && echo up) || python3 -m http.server 8765 >/tmp/srv.log 2>&1 &
```
Puis ouvrir `http://localhost:8765/<fichier>.html` dans le navigateur (`xdg-open`, `open` ou `start` selon le système).
Ensuite : tu édites le fichier, l’utilisateur fait **F5**. Pas de re-spawn de Chrome à chaque tour.

Pour itérer sur **une carte / un composant** : ouvre la vue qui le rend isolément (ex. l'outil de review affiche une carte à la fois). « Ouvre au pif » = ouvre n'importe quel exemplaire réel, le template est partagé.

## Traduire les retours courts (dictionnaire d'intentions)

| Il dit | Tu fais (interprétation par défaut) |
|---|---|
| « trop d'infos » | Réduire la densité de la vue d'entrée : replier/déplacer le secondaire (pied de carte, `<details>`), garder le signal + l'action. |
| « j'aime pas » (vague) | Changer la chose la plus saillante que tu viens de toucher ; proposer un écart net, pas un micro-ajustement. |
| « trop technique » | Vulgariser : définir le jargon, mener par le so-what, raccourcir. |
| « moche / mise en page » | Travailler l'espacement, la hiérarchie typo, l'alignement, la couleur d'accent — pas le contenu. |
| « pas assez aéré / serré » | Ajuster paddings/marges/interlignes. |
| « ça fait trop IA » | Retirer emojis, formules génériques, sur-structuration ; ton plus humain. |
| « highlights / première page » | Vue d'ensemble du run en tête (digest/grille/hero/tableau), avant le détail carte par carte. |

Quand un retour est ambigu, choisis l'option qui **réduit** plutôt que celle qui ajoute (le défaut penche vers moins, signal d'abord).

## Quand le design est validé

Quand l’utilisateur dit que c'est bon (« ça marche », « DONE », « valide ») :
1. Si le design vit dans une surface réelle (outil), il y est déjà.
2. **Propager aux skills concernés** : reporter le format/CSS validé dans les skills ou gabarits de génération qui produisent ce livrable, pour que la suite produise désormais ce format (« une fois validé, mets à jour les skills correspondants »).
3. Commit/sauvegarde si pertinent.

## Anti-patterns

- Poser une question de clarification au lieu de tenter un guess. (Sauf demande explicite.)
- Tout refondre à chaque retour au lieu d'un changement ciblé.
- Renvoyer un fichier à chaque itération au lieu du live + F5.
- Supprimer de l'info vérifiée en silence pour « faire plus propre ».
- Maquette jetable déconnectée du vrai produit → le travail validé n'atterrit nulle part.
