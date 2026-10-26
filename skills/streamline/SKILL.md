---
name: streamline
description: Use when the user says "streamline", "/streamline", "streamline ça", "streamline interface", "streamline interactions", "fais du streamline", "trop verbeux", "tu répètes", "enlève le bruit", "va à l'essentiel", "trop de clics" about a page, dashboard, document, UI section or message — or when building any deliverable the user will read on their phone. "streamline" alone = interface AND interactions; "streamline interface" or "streamline interactions" = that one only. Always TWO goals: a pleasant, accessible, intuitive interface AND a professional, stylish visual result (frontend-design, mockups shown before coding) — cutting text alone never counts. Interface = Notion visual style (format-notion) + hard cut to essential content. Interactions = fewest gestures (no intermediate step, click the object itself, never lose the current view, only offer choices that work).
---

# Streamline — le signal, sans le bruit

## Vérification indépendante (choix avant application)

Avant d'appliquer le skill, demander : **« Veux-tu le faire avec une vérification indépendante ? »** — A : oui ; B : non ; C : autre, précise-moi. Attendre la réponse avant de modifier le livrable. Si l’utilisateur a déjà donné ce choix pour le travail en cours, ne pas le redemander ; ne pas réutiliser le choix d'un autre travail.

• **Non** : appliquer le skill et effectuer les contrôles ordinaires de l'agent principal, sans agent vérificateur.
• **Oui** : terminer la modification, puis envoyer le résultat à **un seul agent indépendant pour une seule passe complète**. Ce choix autorise cette délégation et la correction des problèmes constatés dans le périmètre demandé.
• Le vérificateur découvre d'abord le rendu à froid, sans les conclusions du principal. Il cherche à le critiquer : compréhension au premier regard, propreté visuelle, contenu essentiel, interactions, cohérence, états d'erreur, accessibilité et respect de la demande. Il utilise réellement les parcours, teste sur bureau et mobile 390 px, prend et regarde des captures ; pour un livrable statique, adapter ces contrôles au format.
• Il **ne corrige pas le livrable**. Il rend un rapport priorisé : chaque bug ou problème doit porter une localisation précise, sa gravité, son impact, des étapes de reproduction et une preuve (capture, mesure ou ligne de code). Distinguer défaut démontré et préférence ; indiquer aussi la couverture, les limites et les points non testés.
• Tester les actions qui changent des données sur des fichiers/comptes jetables ou une instance isolée, sauf autorisation explicite sur les données réelles. Propager les règles de l’utilisateur aux sous-agents ; ils ne modifient que leurs artefacts de test et de rapport.
• Le principal examine le rapport et **corrige automatiquement les problèmes établis**, puis vérifie les correctifs et les non-régressions utiles. Signaler tout problème réellement bloqué ou hors périmètre, avec sa raison.
• **Arrêt après cette passe et ses corrections.** Les contrôles ciblés du principal après correction ne sont pas une nouvelle passe d'audit. Ne pas relancer le vérificateur, ni un autre agent, ni une boucle d'amélioration, sauf nouvelle demande explicite.
• Livrer un bilan bref avec le rapport, les corrections et les limites restantes. Un « oui » active cette vérification pour ce travail ; il n'autorise pas d'actions externes ou de changements hors périmètre.

## Portée (selon ce que l’utilisateur dit)

| l’utilisateur dit | On traite |
|---|---|
| « streamline » seul | **interface ET interactions** |
| « streamline interface » (ou « visuel », « texte ») | l'interface seulement |
| « streamline interactions » (ou « parcours », « clics ») | les interactions seulement |

## Ce que demande « streamline » : toujours les deux

« streamline » ne veut jamais dire seulement « couper ». Il demande **deux choses** :
1. **Une interface agréable, accessible, intuitive** : on comprend au premier regard quoi faire, chaque action est là où on l'attend, contrastes et tailles lisibles, clavier et mobile OK.
2. **Un rendu visuel pro et stylé** : la page doit avoir l'air d'un produit soigné, pas d'un formulaire d'admin. Couper le texte ne suffit pas : une page courte peut rester moche.

Leçon : une refonte « streamline » qui a coupé le texte sans refaire le design a reçu ce verdict : « ça reste moche ».

## Rendu visuel pro (exigence 2, jamais sautée)

• Charger le skill `frontend-design` et choisir une **direction visuelle** assumée (typographie, palette, rythme des espacements, composants), cohérente avec le produit hôte.
• Pour une page d'application : **2 à 3 maquettes rendues** (captures), montrées à l’utilisateur avant de coder ; il choisit (A/B/C + D ouverte).
• Hiérarchie visuelle nette : un titre fort, des cartes ou blocs qui respirent, des états (vide, chargement, erreur) dessinés, des icônes cohérentes, aucune boîte grise empilée sans relief.
• Juger sur **une capture regardée** (bureau et 390 px), jamais sur le code ; passe `harmony` avant de livrer.
• Test final : « est-ce qu'un client trouverait ça beau et professionnel ? » Si la réponse honnête est non, ce n'est pas fini.

## Interface

Deux exigences, toujours ensemble :

1. **La forme : le style Notion** — skill `format-notion` (hiérarchie forte, couleur = sens, tableaux pour les chiffres, gras sur le terme-clé). La lire si elle n'est pas chargée.
2. **Le fond : uniquement l'essentiel.** Chaque mot doit porter une information que l’utilisateur utilise. Tout le reste part.

## La passe de coupe (à faire sur chaque bloc, avant de livrer)

Pour chaque ligne, titre, sous-titre, légende, note : **« si je l'enlève, l’utilisateur perd-il une information dont il a besoin ? »** Non → on enlève.

À supprimer systématiquement :

| Bruit | Exemple (page de budget fictive) | Remplacer par |
|---|---|---|
| **Un chiffre affiché deux fois** | le net dans les chiffres-clés ET en bas de la carte ; le total des taxes dans la légende ET dans « À payer » | un seul endroit, celui où il sert |
| **Une phrase qui explique la page** | « abonnements logiciels professionnels, remboursés par l'employeur » | rien : le titre suffit |
| **La formule de calcul** | « au barème : 60 % du montant × tranche 10 % » | le résultat seul ; la formule vit dans le code |
| **Une note de fonctionnement** | « mis de côté sur le compte courant, déjà retiré du reste disponible » | rien |
| **Un montant d'entrée mêlé aux sorties** | 1 500 € encaissés listés parmi les sommes « à reverser » | l'entrée dans le haut, les sorties dans leur liste |
| **Un paragraphe conditionnel** | « Si elle l'est, la taxe tombe à X au lieu de Y, payée avec… et il reste Z » | 5 mots en sous-ligne : « 30 € si l'option passe » |
| **Des références sans usage** | n° de facture, devise d'origine, période facturée | seulement si elles servent à agir |

## Règles de construction

• **Haut de section = la réponse** : 2 à 3 chiffres-clés (ex. Gagné · Taxes · Il reste). Tout ce qui suit précise, ne répète pas.
• **Une ligne = libellé court + montant + au plus 5 mots de contexte** (date, échéance).
• **Pas de sous-titre sous un titre** sauf s'il ajoute une donnée.
• **Titres de 1 à 3 mots.**
• **Mobile d'abord** : on lit souvent sur téléphone. Vérifier en largeur 390 px (iframe 390 px ou fenêtre réduite) : aucune ligne qui passe sur 3 lignes, pas de défilement horizontal.

## Interactions : le moins de gestes possible

Pour chaque parcours (charger, choisir, supprimer, changer de vue) : **compter les clics** et se demander « lequel peut disparaître ? ».

| Bruit d'interaction | Exemple (outil de simulation fictif) | Remplacer par |
|---|---|---|
| **Un bouton pour agir sur un objet déjà cliquable** | carte d'un jeu + bouton « Afficher » | cliquer la carte suffit |
| **Une étape intermédiaire** | « Choisir un jeu » puis « Choisir une partie… » avant la liste | un clic ouvre directement la liste |
| **Une action qui fait perdre la vue** | afficher un jeu de données refermait le panneau où l'on travaillait | l'utilisateur reste où il était |
| **Une édition non voulue** | nom d'un jeu modifiable en ligne dans un tableau de résultats | texte simple, éditer ailleurs si besoin |
| **Une confirmation alors qu'on peut annuler** | « Êtes-vous sûr ? » avant une suppression annulable par Ctrl+Z | supprimer + message « Ctrl+Z pour annuler » |
| **Des choix hors sujet proposés** | parties de tous les scénarios, dont certaines incompatibles avec le modèle chargé | ne proposer que ce qui marche |
| **Plusieurs chemins pour la même action** | bouton icône + bouton libellé qui ouvrent le même panneau | un seul, à l'endroit attendu |

Règles :
• **Un objet = une action principale au clic** ; les actions rares vont dans un menu « ⋯ » ou un clic droit.
• **Les entrées (charger, importer) en premier, à gauche** ; la sortie (ce qu'on regarde) au centre.
• **Rien ne se ferme ni ne change de vue sans que l'utilisateur l'ait demandé.**
• **Liste de choix : regrouper et rendre chaque entrée distinguable** (jamais 10 lignes identiques).

## Vérifier avant de livrer

1. Relire la page en texte (sans le HTML) : lister chaque nombre → **aucun ne doit apparaître deux fois** dans la même section.
2. Compter les phrases complètes dans le rendu : chacune doit se justifier ; en cible, zéro.
3. Capture en largeur mobile, regardée, avant de dire que c'est fait.
4. Sur la capture bureau : la page fait-elle pro et stylé ? Sinon, retour à « Rendu visuel pro ».

## En chat

Mêmes règles que les réponses courtes de tes règles globales : réponse d'abord, pas de reformulation, pas de redite de ce qui est à l'écran.
