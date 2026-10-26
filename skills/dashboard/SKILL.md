---
name: dashboard
description: Construire un tableau de bord web personnel — "fais-moi un dashboard", "un dashboard web pour X", "un tableau de bord". Page privée, d'un seul fichier, au look Notion (assets/notion.css), servie localement ou sur un réseau privé, jamais exposée sur Internet. Pattern « matrice → panneau de détail » pour le suivi à deux dimensions.
---

# Dashboard web (style Notion, servi en privé)

Quand l'utilisateur demande **un dashboard**, il veut : une **page web privée**, servie sur sa machine ou son réseau privé (VPN, réseau local), au **look Notion** clair. Jamais un artifact public, jamais exposé sur Internet.

« Beau et propre » n'est pas optionnel : c'est le critère d'acceptation. Le style est **imposé** par `assets/notion.css` — ne pas réinventer une palette à chaque fois.

## 1. Le style Notion — règles dures

- **Source de vérité** : `assets/notion.css` (dans ce skill). On le **copie** dans le dossier servi et on le lie (`<link rel="stylesheet" href="notion.css">`). On ne réécrit pas les couleurs à la main.
- Fond **blanc** (`--bg:#fff`), texte `#37352f`, police système sans-serif, beaucoup d'air.
- **Tags = select Notion** : petit rectangle arrondi (3-4px), fond pastel + texte foncé. Classes : `.tag.g` gris, `.bl` bleu, `.gr` vert, `.yl` jaune, `.rd` rouge, `.pu` violet, `.or` orange.
- **Tables = database Notion** : header discret (`.db`), lignes cliquables au survol `#f1f1ef`, bordures fines `#ecebe9`.
- **Cartes de synthèse** : `.card` avec `.k` (libellé), `.v` (grand chiffre), `.d` (détail), accent optionnel `.accent-gr/-yl/-rd/-g`.
- **Entête de page** : `.ico` (une icône ~44px) + `h1` gros et gras + `.sub` + `.callout` (encart d'avertissement/contexte).
- Statuts standard (mapper les données dessus) : `done` → vert « Validé », `partiel` → jaune, bloqué → rouge, `todo` → gris. Garder ces 4 partout pour la cohérence entre dashboards.

## 2. Le pattern « matrice → panneau de détail »

Le format le plus lisible pour un suivi à deux dimensions :

- **Vue principale = une table database** : lignes = éléments (histoires d'utilisateur, tâches…), colonnes = axes (agents, machines…). Chaque **ligne est cliquable**.
- **Clic → panneau** : un panneau `.peek` qui **glisse depuis la droite** (comme l'ouverture d'une page Notion), voile `.scrim` derrière, fermeture par ✕ / clic sur le voile / Échap.
- Le panneau montre le **détail** : titre, état (tag), note, propriétés (`.prop` = dt/dd), sous-listes (`.eclist`) et **captures** (`.shots` en grille, miniatures `.thumb`).
- Tout en **une seule page** : données en JSON embarqué + petit JS de rendu. Pas de framework, pas de CDN (la page doit marcher hors ligne).

## 3. Servir en privé

Un dashboard = **un dossier** contenant `index.html`, `notion.css` et les assets (ex. `preuves/`).

```bash
# choisir un port libre
for p in 7900 7901 7902; do ss -tln | grep -q ":$p " && echo "$p occupé" || { echo "$p LIBRE"; break; }; done

# servir UNIQUEMENT sur l'adresse privée voulue (par défaut cette machine seule ; jamais 0.0.0.0)
BIND=127.0.0.1        # ou l'adresse de ton réseau privé / VPN
nohup python3 -m http.server <port> --bind "$BIND" --directory <dossier-du-dashboard> \
  >"<dossier-du-dashboard>/serveur.log" 2>&1 &

# vérifier
curl -s -o /dev/null -w "%{http_code}\n" "http://$BIND:<port>/"
```

**Persistance** : un serveur lancé à la main tombe au redémarrage de la machine. Proposer (sans l'imposer) un service : `systemd` (`Restart=always`, `systemctl enable --now`) ou une tâche planifiée au démarrage, lançant la même commande `http.server`.

**Règles** : bind sur l'adresse privée uniquement ; contenu privé ; pas de secret en clair dans la page ; `<meta http-equiv="refresh" content="180">` pour rafraîchir des données relevées régulièrement.

## 4. Recette d'un nouveau dashboard

1. Créer le dossier du dashboard (+ sous-dossiers d'assets).
2. Copier `notion.css` depuis ce skill dans le dossier.
3. Écrire `generer.py` : **données en tête** (structures Python éditables), génération d'`index.html` (JSON embarqué + JS).
4. Lancer le serveur sur un port libre, vérifier un HTTP 200 (page **et** un asset), regarder une capture d'écran.
5. Donner l'URL. Mise à jour ultérieure = éditer les données dans `generer.py` puis régénérer.
