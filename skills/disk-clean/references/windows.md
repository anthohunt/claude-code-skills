# Windows : points à contrôler

## Mesurer

Utiliser PowerShell pour les volumes, partitions, processus et registres de désinstallation. Les scans de métadonnées doivent ignorer jonctions, liens et placeholders cloud pour éviter les cycles, le double comptage ou le téléchargement de fichiers OneDrive. Une erreur d'accès signifie « zone non mesurée », pas « dossier vide ».

Éviter les sommes cumulées des parents et sous-dossiers. Pour les gros fichiers liés, vérifier les liens physiques avant d'estimer un gain. Ne pas fabriquer des liens physiques entre des fichiers seulement similaires : comparer le contenu et expliquer que modifier un alias peut modifier les autres. Préférer supprimer les copies autorisées plutôt que changer implicitement leur sémantique.

## Projets et outils

• Unity : identifier un projet par `Assets` et `ProjectSettings/ProjectVersion.txt`, pas uniquement par son nom. Inventorier aussi les projets imbriqués. Garder le projet actif, sa `Library`, les caches Unity partagés, Gradle et shaders lorsque l'utilisateur veut conserver son démarrage et ses builds rapides. Examiner jonctions, packages locaux et références avant de supprimer un ancien projet parent. Désinstaller les versions d'éditeur par leur désinstalleur, puis contrôler les résidus et Unity Hub. Ne pas ouvrir un projet conservé avec une autre version implicitement.

• Python/Conda/CUDA : regarder les environnements, `pyvenv.cfg`, interpréteurs réellement utilisés, profils, tâches planifiées et dépendances. Plusieurs versions CUDA peuvent servir des runtimes différents : comparer les DLL requises, pas uniquement « la plus récente ». Une purge de téléchargement pip n'est pas la suppression d'un environnement. Ne pas charger Whisper ni un autre modèle pour ce contrôle.

• npm/pnpm/uv/Playwright : utiliser la version installée du gestionnaire et interroger son magasin. Vérifier les magasins de plusieurs versions. Ne pas supprimer globalement `node_modules` ou les venvs des projets actifs. Les anciennes révisions Playwright peuvent encore être requises par d'autres paquets ; contrôler les références `.links` et `browsers.json`. Un magasin uv verrouillé reste préservé ; ne pas arrêter les serveurs MCP pour forcer une purge.

• Modèles IA : inventorier Ollama et les fichiers hors Ollama séparément. Une autorisation portant sur les modèles Ollama ne couvre pas les modèles utiles de transcription, de voix ou d'autres applications. Vérifier la suppression via le gestionnaire, sans lancer de modèle.

## Caches, temporaires, corbeille

Purger uniquement les feuilles `Cache`, `Code Cache` ou autres caches identifiés. Conserver profils, cookies, sessions, extensions, données utilisateur et modèles. Les applications ouvertes peuvent conserver des fichiers verrouillés ou recréer des fichiers ; journaliser ce résultat sans les tuer largement.

Un dossier temporaire d'extraction d'installateur peut être supprimable une fois l'installation terminée. Vérifier les installateurs actifs et le contenu ; ne pas appliquer cela au cache permanent de Windows Installer ou de Visual Studio. Ne pas supprimer manuellement `WinSxS`, `Installer`, le driver store ou les dossiers système de paquets.

Pour la corbeille, examiner celle du SID courant. Les autres comptes ont leurs propres corbeilles et données : leur taille n'est pas une autorisation de les vider.

## Docker et WSL

La taille de `docker_data.vhdx` ou `ext4.vhdx` n'est pas entièrement récupérable. Distinguer contenu utile, caches internes et espace libéré non rendu au disque hôte. Inventorier images, conteneurs, volumes, montages et projets avant prune. Les volumes peuvent contenir bases, résultats et modèles ; une absence de conteneur actif ne prouve pas leur inutilité.

Avant de démarrer un moteur arrêté, regarder ce qui pourrait se lancer automatiquement. Préférer un audit hors ligne en lecture seule si le démarrage peut déclencher un modèle ou des travaux. Une bibliothèque de lecture VHDX/ExtFS comme Dissect peut servir cet audit, avec des dépendances isolées dans le workspace ; elle ne justifie pas une écriture directe dans le système de fichiers Linux.

La compaction est une opération distincte de la suppression de fichiers internes. La proposer seulement sur un disque précisément identifié, dynamique et détaché ou monté en lecture seule, après vérification de la documentation et des autorisations. Ne jamais supprimer le VHDX, désenregistrer une distribution, ni repartitionner sous couvert de « vider les caches ». Vérifier et rétablir l'état initial des services lancés pour l'opération.

## Sources à vérifier selon l'opération

• [Caches pip](https://pip.pypa.io/en/stable/cli/pip_cache/), [magasin pnpm](https://pnpm.io/cli/store), [navigateurs Playwright](https://playwright.dev/docs/browsers#stale-browser-removal).

• [Espace WSL](https://learn.microsoft.com/en-us/windows/wsl/disk-space), [compaction VHD](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/compact-vdisk), [Optimize-VHD](https://learn.microsoft.com/en-us/powershell/module/hyper-v/optimize-vhd).

• [Prune Docker](https://docs.docker.com/engine/manage-resources/pruning/). Vérifier aussi l'aide de la CLI réellement installée avant exécution.
