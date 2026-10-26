---
name: disk-clean
description: "Auditer l'espace disque et nettoyer les lots autorisés sur un ordi, un VPS ou un disque externe. Utiliser pour /disk-clean, les demandes de nettoyage de stockage et la recherche des plus gros gains récupérables, en préservant les projets actifs et les services utiles."
---

# Disk Clean

Reprendre la méthode : mesurer, proposer des lots précis, nettoyer ceux autorisés, vérifier le résultat, puis chercher les prochains gains. Adapter les outils à la machine ; ne pas imposer de logiciel d'analyse ni installer un agent permanent.

## Cadrer la cible et préserver le travail

Par défaut, auditer la machine locale. Si l'utilisateur nomme un VPS, un autre hôte ou un disque externe, retrouver sa configuration puis vérifier l'identité de la machine, du volume et des chemins avant toute suppression. Utiliser CLI/API/SSH avant une interface graphique. Ne pas modifier un autre hôte dans cette demande.

Retrouver d'abord le dossier ou l'audit existant dans le contexte, le workspace et les notes du projet. Vérifier les tailles actuelles ; un ancien rapport n'est pas un inventaire vivant. Continuer dans le même dossier et garder les décisions « conserver », les dépendances actives et les autorisations de la demande en cours. Si une information indispensable reste introuvable, poser une seule question.

Identifier les projets en développement, caches nécessaires à leur chargement, outils utilisés, services en production et données personnelles. Ajouter leurs chemins exacts à la liste de protection. Une demande de garder un projet rapide inclut ses caches d'importation, de compilation et de shaders. Ne retirer une protection qu'avec une décision explicite de l'utilisateur.

Lire [references/windows.md](references/windows.md) pour Windows ; [references/linux-vps.md](references/linux-vps.md) pour Linux, macOS ou un VPS. Ne charger que la référence utile. Sur un serveur distant, reprendre l'hôte indiqué par les règles du projet et passer par le canal sécurisé prévu (SSH par clé, VPN).

## Audit en lecture seule

## Mesurer

Mesurer espace libre, capacité, partitions, systèmes de fichiers, dossiers dominants et gros fichiers. Distinguer disque plein, partition trop petite, espace non alloué et saturation des inodes. La modification des partitions est un travail distinct, à autoriser explicitement.

Commencer par les gros postes et approfondir les candidats. Éviter de rescanner tout le disque à chaque échange. Annoncer les répertoires inaccessibles et les limites de l'audit. Sur un serveur, limiter la charge et rester sur le système de fichiers ciblé.

Le script portable [scripts/inventory.py](scripts/inventory.py) fournit un inventaire de métadonnées en JSON, sans lire le contenu des fichiers ni supprimer quoi que ce soit :

```text
python <skill>/scripts/inventory.py <racine> --output <workspace>/work/inventaire.json
```

Par défaut : 60 secondes maximum, 250 000 fichiers, aucun suivi de liens ni passage sur un autre système de fichiers. `--depth` règle la profondeur du rapport, pas celle du scan. Lire le champ `complete` ; étendre les limites ou auditer des sous-dossiers si nécessaire. Le rapport écrit est son seul effet de bord.

Pour chaque candidat, déterminer le propriétaire et les dépendances avant de choisir l'opération : cache de téléchargement, runtime installé, source de projet, sauvegarde, modèle IA, résultat de simulation, média ou disque virtuel. « Cache », « ancien » et « doublon de nom » ne suffisent pas à établir que le fichier est supprimable. Ne charger aucun modèle IA et ne démarrer aucun service susceptible de lancer des modèles ou des travaux pour les mesurer.

Compter les liens physiques et les fichiers partagés. La somme de dossiers imbriqués se recoupe. La longueur logique d'un fichier sparse, d'un disque virtuel ou d'un fichier lié n'est pas son gain récupérable. Une copie liée ailleurs peut empêcher de récupérer ses blocs après suppression.

Pour une archive ou une sauvegarde, examiner le sommaire et comparer aux sources conservées, y compris les versions différentes. Vérifier une sauvegarde à sa destination avant d'affirmer qu'elle existe. Ne pas rechercher ni afficher des credentials dans cet examen.

## Présenter un choix concret

Présenter un tableau court, numéroté, avec : candidat, espace occupé, gain estimé ou inconnu, action proposée et conséquence utile. Distinguer explicitement les lots « supprimer », « auditer » et « conserver ». Exemple : « Docker : 30 Go occupés, gain inconnu, auditer les images et les volumes » ne signifie pas « supprimer 30 Go ».

Préparer l'inventaire exact des cibles et les vérifications nécessaires avant de demander une décision. Si les suppressions sont déjà autorisées dans la conversation, exécuter les lots correspondants sans redemander. Sinon, demander quels lots supprimer, une seule fois. Un « ok nettoie » porte sur les suppressions proposées ; il ne transforme pas les lots « auditer » en autorisation d'effacer leurs données.

Si une condition échoue, conserver ce lot et poursuivre les autres lots autorisés. Signaler le fait concret : par exemple, une archive contient des sources absentes du projet actif. Éviter de créer un blocage global pour un seul lot.

## Exécuter et journaliser

Préférer le gestionnaire propriétaire : purge de cache, désinstalleur officiel, CLI de modèles ou de paquets. Vérifier son emplacement de stockage et sa version ; plusieurs versions d'un gestionnaire peuvent avoir des magasins distincts. Une commande de prune peut ne retirer qu'une petite partie du magasin.

Pour une suppression directe : utiliser une liste de chemins littéraux et absolus, vérifier leur résolution et leurs parents, exclure les chemins protégés et les liens/jonctions. Sur Windows, garder les opérations de fichiers dans PowerShell avec `-LiteralPath`. Ne jamais supprimer à partir d'une chaîne shell construite avec des noms trouvés sur le disque. Pour une cible partagée ou récemment modifiée, réévaluer avant d'effacer.

Conserver les fichiers verrouillés. Fermer proprement une application seulement lorsque cela ne perd pas le travail ouvert et relève du lot autorisé. Ne jamais tuer tous les processus d'un nom. Un éventuel arrêt doit viser un PID ou une instance exactement identifiée et autorisée ; sur un VPS, maintenir la continuité des services requis.

Journaliser par lot : cible/hôte, chemins, espace libre avant, tailles, commande exécutée, cibles retirées, ignorées et erreurs. En cas d'échec partiel, reprendre les opérations restantes depuis le journal ; ne pas réinitialiser les preuves ni répéter les opérations réussies. Chercher la documentation officielle face à une API inconnue ou une erreur avant un correctif ciblé.

## Vérifier et poursuivre

Vérifier les fichiers réellement absents, les outils/projets conservés et les références des gestionnaires. Pour un projet actif, comparer ses fichiers importants et caches avant/après quand pertinent. Tester un service si l'opération a pu l'affecter ; ne pas lancer un modèle ou une réimportation coûteuse pour vérifier un simple nettoyage de fichiers.

Mesurer l'espace libre après. Rapporter séparément les tailles retirées et l'évolution de l'espace libre : d'autres processus peuvent écrire pendant le nettoyage. Ne pas affirmer que le chargement d'un projet est rapide sans l'avoir chronométré.

Conserver audit, décisions et journal dans le workspace ; livrables utiles dans son dossier de sortie. Réponse courte : gain constaté, espace libre actuel, protections vérifiées et lots conservés avec leur raison. Si l'utilisateur demande « ensuite ? », actualiser les prochains candidats et recommencer à partir de l'audit.
