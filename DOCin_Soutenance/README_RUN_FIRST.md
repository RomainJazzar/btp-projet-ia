# Guide de démarrage – DOCin Soutenance

Ce dépôt contient tous les éléments nécessaires à la soutenance du projet **DOCin**. Suivez ces instructions pour présenter efficacement le matin et l’après‑midi.

## 1. Présentation du matin (sans slides)

1. Ouvrez le fichier `MORNING_TABLE_PACK.md` : il regroupe tout le contenu textuel demandé (nom, promesse, persona, OMFR, positionnement, 7 étapes, stratégie RS, posts complets). Il est conçu pour être lu à voix haute en 3–4 minutes.
2. Rendez‑vous dans le dossier `MEDIA/` et ouvrez chaque image en plein écran :
   - `moodboard.png` : moodboard illustrant l’univers visuel de DOCin.
   - `logo_light.png`, `logo_dark.png` et `logo_mono.png` : déclinaisons du logo.
   - `palette_typography.png` : feuille de palette de couleurs et de typographies.
   - `post_linkedin_carousel.png`, `post_short_cover.png`, `post_x_card.png` : maquettes des posts pour LinkedIn, TikTok/Shorts et X.
3. (Optionnel) Si vous avez généré l’audio :
   - Lisez `jingle.wav` dans un lecteur audio pour faire entendre le jingle de confirmation (2 s). Si ce fichier n’existe pas, voir section 4 pour le générer.
4. (Optionnel) Si vous avez une vidéo de démonstration :
   - Lisez `docin_preview.gif` ou `docin_preview.mp4` pour montrer le flux Upload → Renommage → Classement → Recherche → Q/R.

## 2. Présentation de l’après‑midi (pitch + slides)

1. Ouvrez le fichier PPTX `SLIDES/DOCin_S1_Deck.pptx` avec PowerPoint ou LibreOffice. Chaque slide est numérotée et comprend des notes orateur (affichables en mode Présentateur) résumant ce qu’il faut dire en 30–60 secondes.
2. Si vous ne disposez pas de PowerPoint, ouvrez `SLIDES/DOCin_S1_Deck.pdf` : il contient les mêmes diapositives sans animations.
3. En cas de fallback (si le PPTX n’a pas pu être généré), rendez‑vous dans `SLIDES/PNG_EXPORT/` : les fichiers `slide_01.png`, `slide_02.png`, etc. représentent chaque diapositive dans l’ordre, et `slides_manifest.md` décrit le contenu et les notes orateur.

## 3. Contenu additionnel

- `SOCIAL_COPY/` contient les textes bruts des posts LinkedIn, TikTok/Shorts et X.
- `PROMPTING_LOG.md` documente tous les prompts et itérations ayant mené aux médias – utile pour justifier la maîtrise du prompting.

## 4. Générer le jingle et la vidéo (facultatif)

### Générer un jingle localement

Si vous souhaitez créer un jingle audio, copiez le script ci‑dessous dans un fichier Python (ex. `render_jingle.py`) et exécutez‑le. Ce script utilise le module `wave` et `struct` (batterie standard) pour générer deux notes de Do majeur (C5 et E5) sans dépendance externe :

```python
import wave, struct, math

def generate_tone(frequency, duration, volume=0.5, sample_rate=44100):
    num_samples = int(sample_rate * duration)
    samples = [volume * math.sin(2 * math.pi * frequency * t / sample_rate) for t in range(num_samples)]
    return samples

def write_wav(filename, samples, sample_rate=44100):
    with wave.open(filename, 'w') as wav_file:
        wav_file.setparams((1, 2, sample_rate, 0, 'NONE', 'not compressed'))
        for s in samples:
            wav_file.writeframes(struct.pack('<h', int(s * 32767.0)))

C5 = 523.25  # Hz
E5 = 659.25  # Hz

samples = []
samples += generate_tone(C5, 0.12)
samples += generate_tone(E5, 0.20)

write_wav('jingle.wav', samples)
print("Jingle généré dans jingle.wav")
```

### Générer une vidéo simple

Nous avons fourni un storyboard dans `PROMPTING_LOG.md`. Pour réaliser une vidéo, vous pouvez utiliser un éditeur vidéo comme OpenShot ou un script Python (moviepy) en associant des captures d’écran de l’application. Si cela n’est pas possible, utilisez `docin_preview.gif` comme démonstration animée.

## 5. Créer l’archive finale

Pour regrouper tous les fichiers dans une archive ZIP prête à être envoyée, placez‑vous dans le répertoire parent de `DOCin_Soutenance/` et exécutez :

```bash
zip -r PACK.zip DOCin_Soutenance
```

L’archive `PACK.zip` contiendra toute l’arborescence (MORNING_TABLE_PACK.md, PROMPTING_LOG.md, SLIDES, MEDIA, SOCIAL_COPY). Vous pouvez la partager facilement avec vos évaluateurs.
