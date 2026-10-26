---
name: doc
description: Consulter la documentation officielle Meta Horizon (developers.meta.com) — l'index complet des ~2 600 pages est en cache local, la recherche est un grep instantané, la lecture un WebFetch du markdown brut. À utiliser AVANT de câbler, configurer ou affirmer quoi que ce soit sur Unity XR / Meta XR SDK / Quest / OpenXR — y compris quand on se croit sûr. Déclencheurs — "/doc", "cherche dans la doc", "qu'est-ce que dit la doc sur X", "vérifie dans la doc", ou toute question Meta/Quest/XR à laquelle on s'apprête à répondre de mémoire.
---

# doc — la documentation Meta Horizon comme réflexe

> Première utilisation : créer l'index avec la commande de la section « Rafraîchir l'index » (une seule fois).

## Pourquoi ce skill existe

Le mode d'échec qu'il corrige, constaté : travailler des heures sur le
suivi de mains en lisant le **code source** du SDK et en sondant des composants, sans
ouvrir une seule fois la documentation. Résultat — un composant inventé à la main
(`ControllersEnabler`) qui a verrouillé les manettes éteintes, alors que la doc
donnait la réponse supportée (le rig de remplacement et son `HandsMerger`). Puis un
diagnostic affirmé et commité (« le périphérique MetaAimHand est absent ») que la
première mesure réelle a démenti.

Le code source dit **comment c'est fait**. La doc dit **comment c'est censé
s'assembler**. Prendre le premier pour le second, c'est avancer à l'aveugle.

## La règle

**Consulter la doc AVANT d'agir, pas après avoir échoué.** Le doute n'est pas le
déclencheur — l'absence de doute non plus n'est pas une dispense. Se sentir sûr est
précisément l'état dans lequel on ne vérifie pas, et donc celui où l'on se trompe
sans le voir.

Déclencheurs, non négociables :
- avant de **câbler** un rig, un interactor, un prefab, une feature OpenXR ;
- avant d'**affirmer** un comportement du SDK à l’utilisateur ;
- avant d'**inventer** un composant : la question « Meta fournit-il déjà ça ? » se
  tranche par une recherche, jamais par intuition ;
- dès qu'un nom de prefab, d'API, de réglage ou de menu Unity est en jeu — ces noms
  changent à chaque version et la mémoire du modèle est périmée.

Red flag : « je sais déjà comment ça marche » → c'est exactement là qu'il faut
chercher, ça coûte dix secondes.

## Comment s'en servir

### 1. Chercher — instantané, local, gratuit

L'index complet est en cache : `~/.claude/meta-doc/llms.txt` (environ 2 600 pages, chacune
avec titre, URL markdown et description d'une ligne).

```bash
# par mots-clés, insensible à la casse
grep -i "hand tracking" ~/.claude/meta-doc/llms.txt | head -20

# croiser deux termes (l'ordre n'importe pas)
grep -iE "unity" ~/.claude/meta-doc/llms.txt | grep -i "teleport"

# ne rendre que les URLs
grep -i "openxr" ~/.claude/meta-doc/llms.txt | grep -oE "https://[^)]+\.md"
```

Chercher **large puis affiner** : le catalogue entier est sous la main, relancer un
grep ne coûte rien. Mieux vaut dix recherches qu'une hypothèse.

### 2. Lire — la page en markdown brut

L'URL trouvée est directement lisible, sans HTML :

```
WebFetch("https://developers.meta.com/horizon/llmstxt/documentation/unity/<page>.md", "<ta question précise>")
```

Poser à `WebFetch` une **question précise**, pas « résume » : la page fait souvent
plusieurs milliers de mots et la réponse utile tient en trois lignes.

### 3. Rafraîchir l'index — quand il a vieilli

Date du cache dans `~/.claude/meta-doc/fetched-at.txt`. Au-delà d'un mois, ou si une
recherche ne trouve rien d'attendu :

```bash
mkdir -p ~/.claude/meta-doc && curl -s -m 60 -A "Mozilla/5.0" https://developers.meta.com/horizon/llmstxt/llms.txt \
  -o ~/.claude/meta-doc/llms.txt && date -Iseconds > ~/.claude/meta-doc/fetched-at.txt
grep -c "^- \[" ~/.claude/meta-doc/llms.txt   # doit rendre ~2600+
```

## Ce que couvre l'index

`Unity` · `Unreal` · `Spatial SDK` · `Native & OpenXR` · `Immersive Web SDK` · `Web`
· `Android Apps` · `Essentials` · `Distribute & Grow` · `Policy` · `Design`.

Au-delà des pages `documentation/`, le site sert aussi la **référence d'API**
(`/horizon/reference/unity/latest/…` — `OVRManager`, `OVRInput`, `OVRCameraRig`), les
pages de **permissions**, et les **téléchargements** (dont le Meta XR Simulator).

## Pourquoi un index local

On voit le **catalogue entier** au lieu d'un top-5 opaque, la recherche est locale donc
gratuite et répétable à volonté, et il n'y a aucune dépendance à un plugin tiers.

## Anti-patterns

- **Répondre de mémoire sur un nom de prefab, d'API ou de menu Unity.** Ils changent
  de version en version ; la mémoire du modèle a des mois de retard.
- **Lire le code du package au lieu de la doc pour savoir comment assembler.** Le
  code montre une implémentation, pas la façon supportée de s'en servir.
- **Chercher seulement après l'échec.** Le coût d'une recherche est de dix secondes,
  celui d'un composant inventé se compte en heures et en régressions.
- **Se contenter du premier résultat.** Le grep est gratuit : croiser deux ou trois
  formulations avant de conclure qu'une page n'existe pas.
