---
name: format-notion
description: Use when the user asks for "format Notion", "style Notion", "mets ça en format Notion/joli", or when producing a polished structured deliverable (compte-rendu de réunion, briefing, doc de cours, rapport) that must be scannable and pleasant to read. Defines a writing+layout standard inspired by Notion docs.
---

# format-notion — standard de mise en forme « style Notion »

## Principe
**La structure porte le sens.** Un bon document se scanne : on sait la nature de chaque bloc avant de le lire, grâce à un **système de callouts à couleur sémantique** + une hiérarchie typo forte.

## Système de couleurs sémantiques (le cœur — la couleur = un SENS, jamais déco)
| Couleur | Sens | Exemples d'usage |
|---|---|---|
| **bleu** | objectif / cadrage | objectif d'une section, ce qu'on vise |
| **vert** | message-clé / décision / « pourquoi ça marche » | take-away, décision actée |
| **brun** | théorie / concept à comprendre | explication d'un mécanisme |
| **jaune** | attention / point ouvert / à surveiller | risque, question en suspens |
| **rouge** | urgence / blocage / fallback | danger, action critique |
| **violet** | intro / section majeure / transition | ouverture d'un gros bloc |
| **gris** | méta / liens / ressources secondaires | crédentials, références |

## Règles de forme
- **En-têtes à statut** quand pertinent : 🟢🟡🔴 (facile/moyen/dur) + durée en *italique* `*(~10 min)*`.
- **Hiérarchie** : titres `#`/`##` préfixés d'une icône **fonctionnelle**, étapes **numérotées**, séparateurs `---` entre blocs majeurs.
- **Le bon conteneur** : texte à copier → bloc de code ; comparaison/données → **tableau** ; idée-clé → **gras** dans un callout coloré ; aparté/citation → *italique* ; actions → liste numérotée.
- **Signal d'abord** : une idée par bloc, gras sur les termes-clés, pas de remplissage.

## Icônes : fonctionnelles, pas décoratives
Les emojis décoratifs font vite « généré par IA ». **Exception assumée ici** : dans le style Notion, icônes + couleurs servent au **repérage/sémantique** (une par section/callout, qui a un sens). Jamais d'emoji gratuit dans le corps du texte.

## Le fond compte autant que la forme
Ne JAMAIS dumper du brut (transcript, logs). **Rédiger** : intro/résumé exécutif court, puis sections structurées. Le lecteur doit suivre sans effort.

## Implémentation HTML (cible par défaut des livrables auto-contenus)
Callouts = encadré `bordure-gauche colorée + fond teinté + icône`. CSS réutilisable :

```html
<style>
:root{ --ink:#1a1a1a; --mut:#6b6b6b; --line:#e6e4df; }
body{ font:16px/1.6 -apple-system,Segoe UI,Roboto,sans-serif; color:var(--ink); max-width:780px; margin:40px auto; padding:0 20px; background:#fff; }
h1{ font-size:30px; letter-spacing:-.02em; margin:.2em 0 } h2{ font-size:21px; margin:1.6em 0 .4em; border-bottom:1px solid var(--line); padding-bottom:.2em }
hr{ border:0; border-top:1px solid var(--line); margin:2em 0 }
.cal{ display:flex; gap:10px; padding:12px 14px; border-radius:8px; margin:12px 0; border-left:4px solid }
.cal .i{ font-size:18px; line-height:1.4 } .cal .b{ flex:1 }
.cal.blue{ background:#eef4fd; border-color:#3b82f6 } .cal.green{ background:#ecfdf3; border-color:#16a34a }
.cal.brown{ background:#f6f1ea; border-color:#a16207 } .cal.yellow{ background:#fef9ec; border-color:#eab308 }
.cal.red{ background:#fdecec; border-color:#ef4444 } .cal.purple{ background:#f4eefe; border-color:#8b5cf6 }
.cal.gray{ background:#f4f4f2; border-color:#9ca3af }
table{ border-collapse:collapse; width:100%; margin:12px 0 } th,td{ border:1px solid var(--line); padding:7px 10px; text-align:left } th{ background:#faf9f7 }
code{ background:#f4f4f2; padding:1px 5px; border-radius:4px; font-size:.9em }
.meta{ color:var(--mut); font-size:14px }
</style>

<h1>Compte-rendu — Réunion X</h1>
<div class="meta">12 juin 2026 · Participants : …</div>

<div class="cal purple"><div class="i">📌</div><div class="b"><b>Résumé.</b> En 2-3 phrases, le so-what de la réunion.</div></div>

<h2>Décisions</h2>
<div class="cal green"><div class="i">✅</div><div class="b"><b>Décision actée.</b> Formulation claire.</div></div>

<h2>Actions</h2>
<div class="cal blue"><div class="i">🎯</div><div class="b"><b>Qui</b> — quoi, pour quand.</div></div>

<h2>Points ouverts</h2>
<div class="cal yellow"><div class="i">💬</div><div class="b">Sujet non tranché.</div></div>

<h2>Questions</h2>
<div class="cal gray"><div class="i">❓</div><div class="b">Question en suspens.</div></div>
```

## Cibles possibles selon le besoin
- **HTML auto-contenu** (défaut) : un fichier, partageable par lien, téléchargeable. Utiliser le CSS ci-dessus.
- **Page Notion native** : si le livrable doit vivre dans Notion → callouts via l'API (`color: blue_bg`, etc.) avec la même grille sémantique.
- **Markdown enrichi Notion** : `<callout icon="…" color="green_bg">` quand on écrit dans Notion via MCP.

## Quand NE PAS l'utiliser
- Données purement tabulaires/CSV, code brut, sortie machine → garder simple.
- Quand l'utilisateur demande explicitement « brut » / texte nu.

## Mapping catégories réunion → couleur (compte rendu de réunion)
Résumé = **violet** · Décisions = **vert** · Actions = **bleu** · Points ouverts = **jaune** · Questions = **gris** · Risques/urgences = **rouge**.
