---
name: note-agenda
description: Use ONLY when the user explicitly asks for a note in their agenda — « mets une note dans mon agenda », « note dans l'agenda pour demain », « /note-agenda ». Adds ONE short line to the all-day « À faire » event of that day in Google Calendar (created if absent). Never used by another skill on its own initiative, and not for appointments (→ calendar event with a time) or alarms.
---

# Note dans l'agenda

Pour qui trouve qu'une liste de tâches séparée devient vite un fouillis : la note va dans **un seul événement par jour**, journée entière, titré **« À faire »**, une puce par chose à faire.

Seulement sur demande explicite de l'utilisateur. Aucun autre skill ne l'appelle de lui-même.

## Prérequis

[`gws`](https://github.com/googleworkspace/cli) (CLI Google Workspace) installé, dans le PATH (ou `GWS=<chemin>`) et connecté au compte (`gws auth login`). Fuseau : celui de l'ordinateur, ou `NOTE_AGENDA_TZ=Europe/Paris`.

## Une commande

```bash
node <dossier du skill>/note-agenda.mjs YYYY-MM-DD "ligne"
```

• Date omise = aujourd'hui (fuseau configuré). « Demain » = calculer la date dans ce fuseau.
• L'événement du jour existe déjà → la ligne s'ajoute à la fin de sa description. Sinon il est créé (agenda principal, journée entière, « disponible », propriété privée `noteAgenda=1` qui sert à le retrouver).

## La ligne

**Une seule ligne, courte, un verbe et l'objet.** Exemple : « Envoyer la facture n° 12 au client Durand ». Pas de contexte, pas de lien, pas de sous-puces.

## Vérifier

Le script affiche l'événement renvoyé par Google (id, date, description) : c'est la preuve. Répondre à l'utilisateur en une ligne : la date et la ligne ajoutée.
