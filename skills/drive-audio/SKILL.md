---
name: drive-audio
description: Use when the user veut récupérer le ou les derniers enregistrements audio déposés sur Google Drive et les transcrire dans la foulée — déclencheurs « /drive-audio », « drive audio », « récupère le dernier audio sur Drive », « transcris le dernier audio du Drive », « les 3 derniers audios du Drive ». Sans nombre précisé = UN seul fichier (le plus récent) ; un nombre précisé = les N plus récents. Enchaîne téléchargement Drive puis skill `transcribe-audio`.
---

# /drive-audio — dernier(s) audio(s) du Drive → transcription

Combine deux gestes : aller chercher le ou les derniers fichiers audio sur Google Drive, puis les transcrire. La transcription elle-même reste décrite dans `transcribe-audio` (source unique : backend, modèle, synthèse) — ce skill ne la duplique pas.

## Arguments

| L'utilisateur dit… | Comportement |
|--------------|--------------|
| rien (« /drive-audio ») | **1** fichier, le plus récent |
| un nombre (« /drive-audio 3 », « les 3 derniers ») | les **N** plus récents |
| « synthèse », « résume » | transcript brut + synthèse (cf. `transcribe-audio`) |

Sans mention de synthèse : transcript brut uniquement.

## Étapes

1. **Lister** les N derniers audios (tri par date de création, corbeille exclue) :

```bash
gws drive files list --params '{"q":"mimeType contains '\''audio/'\'' and trashed = false","orderBy":"createdTime desc","pageSize":<N>,"fields":"files(id,name,mimeType,createdTime,size)"}'
```

2. **Télécharger** chaque fichier dans un dossier de travail (`$TMPDIR`) :

```bash
gws drive files get --params '{"fileId":"<FILE_ID>","alt":"media"}' --output "$TMPDIR/<name>"
```

3. **Transcrire** chaque fichier en suivant `transcribe-audio` (Groq par défaut si réseau ; au-delà de ~25 Mo, recompresser en mono 40k d'abord). Plusieurs fichiers = un transcript par fichier, traités du plus ancien au plus récent.

4. **Écrire** chaque transcript dans `~/Downloads/<nom-du-fichier-audio>.txt`.

5. **Nettoyer** : supprimer l'audio téléchargé et les `.json` intermédiaires du dossier de travail. Ne jamais supprimer ni modifier le fichier sur Drive.

## Restitution

Par fichier : nom, date, durée, chemin du `.txt`, et le contenu en deux ou trois lignes. Aucune tâche, note ou e-mail créé automatiquement — proposer seulement si le contenu l'appelle.

## Cas limites

- Aucun audio trouvé : élargir aux vidéos (`mimeType contains 'video/'`) avant de conclure, et le dire.
- Le plus récent a déjà un `.txt` du même nom dans Downloads : le signaler plutôt que retranscrire en silence.
