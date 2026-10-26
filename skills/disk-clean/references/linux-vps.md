# Linux, VPS et macOS

## Identifier la cible et limiter la charge

Sur un serveur distant, retrouver l'hôte dans les configurations autorisées, vérifier le nom de machine et les montages par SSH. Ne jamais supposer qu'un ancien hôte est encore le bon : vérifier le nom de machine avant d'agir. Utiliser l'authentification SSH déjà configurée ; ne pas rechercher un mot de passe humain.

Sur Linux, commencer par `df -hT`, `df -i`, les montages et une vue des disques. Utiliser `du -x` sur le système de fichiers voulu : `/proc`, `/sys`, `/dev`, les montages réseau et les couches Docker peuvent sinon fausser les mesures ou surcharger l'audit. Vérifier les options disponibles sur la machine. Inventorier les gros sous-dossiers avant d'approfondir ; utiliser des limites de durée et, sur une production chargée, une priorité réduite adaptée aux outils disponibles.

Sur macOS, identifier les volumes APFS et utiliser les outils locaux (`df`, `diskutil`, `du`). Distinguer taille des fichiers, clones/APFS, snapshots et espace purgeable. Ne pas compter les blocs partagés comme autant de gains indépendants. Un système APFS plein peut nécessiter un examen des snapshots Time Machine, pas une purge générale du dossier utilisateur. Vérifier les commandes sur cette version de macOS avant mutation.

## Nettoyer avec le gestionnaire propriétaire

• Paquets système : proposer d'abord les caches de téléchargement identifiés. Utiliser le gestionnaire de la distribution installée. Examiner une simulation avant un autoremove : d'anciens paquets, noyaux ou SDK peuvent encore servir au boot, aux builds ou aux services. Ne jamais effacer les bases des gestionnaires à la main.

• Logs : mesurer les journaux système et ceux des applications, identifier la politique de rétention, puis utiliser journalctl/logrotate ou l'outil de l'application. Conserver les diagnostics encore nécessaires. L'espace d'un fichier supprimé mais ouvert peut rester occupé ; repérer le PID exact et l'application concernée avant de décider d'un rechargement ou redémarrage autorisé. Ne pas tronquer arbitrairement un log actif ni redémarrer toute la production.

• Temporaires : utiliser les politiques existantes de nettoyage quand elles correspondent au lot autorisé. Vérifier âge, propriétaires, verrous et tâches actives. `/tmp` peut contenir sockets, sessions et travaux en cours ; aucun effacement récursif global.

• Caches de développement : distinguer cache de téléchargement, venv, SDK et dépendances de projet. Préserver les environnements utilisés, sources, outils déployés, workers et chemins mentionnés dans les unités systemd, tâches cron et commandes des processus. Les caches Hugging Face/Ollama peuvent être les seuls modèles disponibles pour un service ; les classer à part.

• Docker/Podman : mesurer avec le moteur présent si son interrogation ne démarre pas de travaux. Distinguer images utilisées, caches de build, conteneurs arrêtés, volumes et bind mounts. Ne pas utiliser un prune global avec volumes sur la base d'un total occupé. Identifier les projets et données concernés, proposer l'opération précise, puis vérifier ce que le gestionnaire a réellement retiré.

## Sources, sauvegardes et production

Les répertoires de releases, entraînements, exports, médias, sauvegardes et dumps SQL sont des données, même anciens ou hors Git. Vérifier les consommateurs, les références de déploiement et la destination de sauvegarde. Une sauvegarde datée dans un dossier mémoire ne prouve pas que ces données y figurent encore.

Préparer une liste de chemins absolus normalisés sur l'hôte, avec leurs parents autorisés, puis employer des opérations natives et des arguments correctement quotés. Vérifier le système de fichiers et les liens avant toute suppression récursive ; ne pas franchir un montage ou une racine protégée. Ne pas construire une commande de suppression à partir de lignes de texte non échappées.

Vérifier après nettoyage : espace libre/inodes, processus ou services concernés, état des montages et présence des projets protégés. Un audit ou nettoyage local n'autorise aucune intervention distante, et un nettoyage de VPS n'autorise pas une suppression de bases de données ni une interruption de services en dehors des lots choisis.

## Sources à vérifier selon l'opération

• [Prune Docker](https://docs.docker.com/engine/manage-resources/pruning/).

• Documentation officielle du gestionnaire installé et manuels locaux pour `du`, `find`, `journalctl`, `systemd-tmpfiles` ou `logrotate`. Lire les options et simulations utiles avant une purge.

• [APFS et utilitaire de disque](https://support.apple.com/guide/disk-utility/welcome/mac). Ne pas transposer les options GNU de Linux aux outils BSD de macOS.
