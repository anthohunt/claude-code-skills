---
name: continue-conversation
description: Reprendre une conversation Claude Code qui a crashé (ou été coupée par quota) ET le travail qu'elle pilotait. Déclencheurs — "/continue-conversation", "la conversation a crashé", "reprends la conversation", "récupère le contexte de l'ancienne conversation", souvent avec une capture d'écran ou un extrait de la fin. Retrouve la transcription sur cet ordinateur ou sur une autre machine déclarée, relit la fin, vérifie l'état réel du travail, puis répond au dernier message de l'utilisateur comme si rien n'avait coupé.
---

# Continuer une conversation crashée

But : l'utilisateur ne doit rien réexpliquer. On retrouve, on relit, on vérifie, on reprend.

## 1. Extraire des indices du contexte donné
Capture ou texte collé → noter 2-3 **phrases exactes et rares** (pas de nombres seuls : les espaces fines des milliers ne matchent pas), le titre de session, l'heure, et **le dernier message de l'utilisateur** (souvent dans la zone de saisie, pas encore envoyé).

## 2. Retrouver la transcription
```bash
python3 -I <dossier du skill>/trouver.py chercher "phrase rare 1" "phrase rare 2" --heures 48
```
Cherche dans tous les `~/.claude*/projects` de cet ordinateur, puis sur les machines déclarées dans la variable `CONTINUE_MACHINES` (`alias_ssh:linux` ou `alias_ssh:windows`, séparés par des virgules ; voir l'en-tête de `trouver.py`). Rien trouvé :
- raccourcir/changer les phrases (une seule, sans accents ni ponctuation typographique) ;
- vérifier une éventuelle sauvegarde des sessions ;
- machine injoignable → le dire en une phrase à l'utilisateur (« c'était sur le portable, éteint ») et proposer de reprendre depuis l'état du chantier (étape 4) ; ne PAS boucler sur des recherches.

Ne jamais confondre avec la session courante (elle contient la capture et les phrases cherchées).

## 3. Relire la fin
```bash
python3 -I <dossier du skill>/trouver.py relire CHEMIN --machine local|<alias> --n 60
```
Lire jusqu'à comprendre : chantier, décisions déjà prises par l'utilisateur, travail lancé (agents, tâches planifiées, surveillances), question en suspens. Si besoin, `--n 200`.

## 4. Vérifier l'état réel avant de parler
La transcription date ; le monde a bougé. Pour chaque travail en cours : un fait réel (processus, journal, fichier de suivi du chantier, tableau de bord). Réarmer ce que la session morte portait (contrôle périodique, réveil programmé) — un réveil appartient à la session et est mort avec elle.

## 5. Reprendre
- Répondre directement au dernier message de l'utilisateur (ou à la question qu'on lui avait posée), au format de la conversation d'origine.
- Une ligne max sur la reprise elle-même (« Repris depuis la session X, 02:04 »), pas de récap.
- Ne refaire aucune décision déjà prise ; ne relancer aucun agent déjà vivant ; respecter une pause en cours.
