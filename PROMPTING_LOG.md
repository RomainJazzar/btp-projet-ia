# Journal de prompting — DOCin

Ce document retrace notre processus de génération des médias. Pour chaque ressource, nous avons formulé un premier prompt (**v1**), analysé la sortie, puis ajusté le prompt (**v2**) afin d’obtenir un résultat conforme à notre territoire de marque. La **rationale** explique pourquoi l’itération sélectionnée a été retenue.

## Moodboard

- **Prompt v1** : « Crée un moodboard de marque pour DOCin (assistant local de documents). Thèmes : ordre calme, dossiers étiquetés, tampons, bureau propre, palette teal/navy, lumière douce, contraste élevé. 9 tuiles : 3 textures (papier/étiquette/tampon), 3 photos bureau, 3 fragments UI minimalistes. Sortie : PNG 1920×1080, grille régulière, légendes 1 mot par tuile, sans watermark. »
- **Sortie v1** : le générateur a produit un collage agréable mais certaines tuiles étaient très chargées (macros de papiers froissés) et la palette tirait vers le beige au lieu du teal/navy.
- **Critique** : bruit visuel trop important et couleurs éloignées de notre palette (#2EC4B6, #0B132B). L’étiquetage manquait de lisibilité.
- **Prompt v2** : « Crée un moodboard DOCin avec 9 tuiles : 3 textures calmes (papier lisse, étiquette typographique, tampon encreur), 3 photos de bureaux organisés, 3 fragments d’interface épurée. Palette dominée par les teintes teal et navy (#2EC4B6, #0B132B). Suppression de toute teinte beige. Réduis le bruit visuel et ajoute une lumière douce. »
- **Sortie v2** : un collage harmonieux, contrasté, avec des nuances teal/navy et des textures subtilement présentes. Les légendes sont lisibles.
- **Rationale** : la version v2 retranscrit l’ordre et la sérénité recherchés et s’accorde parfaitement avec nos couleurs de marque. Nous l’avons retenue (fichier `moodboard.png`).

## Logo (déclinaisons)

- **Prompt v1** : « Conçois un logo flat minimal pour “DOCin” : dossier + coche, géométrique, lisible à 24 px. 3 variantes (clair/sombre/mono), export SVG + PNG 1024 px. Traits équilibrés, pas de dégradés/ombres, coins légèrement arrondis. »
- **Sortie v1** : le générateur a proposé un pictogramme dossier/coche mais la coche n’était pas assez visible sur le fond clair. Sur fond sombre, les contrastes étaient inégaux. La variante mono manquait de force.
- **Critique** : la coche doit être plus marquée pour évoquer la validation. La version sombre doit avoir un trait clair constant. La version mono doit pouvoir s’imprimer en noir ou blanc sans perte.
- **Prompt v2** : « Refais le logo DOCin : accentue la coche (épaisseur +20 %), garde des coins légèrement arrondis. Prévois 3 versions : (1) fond clair avec logo teal/navy, (2) fond navy (#0B132B) avec logo clair (#E6E8F0/#2EC4B6), (3) version monochrome noire sur fond blanc. Pas de dégradés, trait uniforme. »
- **Sortie v2** : les logos sont nets, la coche ressort nettement sur les deux fonds. La version mono est simple et lisible.
- **Rationale** : la v2 répond à nos critères de lisibilité et de versatilité. Nous avons conservé trois PNG (`logo_light.png`, `logo_dark.png`, `logo_mono.png`) ainsi qu’un fichier `logo.svg` (vectorisation approximative) pour l’intégration.

## Palette & typographies

- **Prompt v1** : « Propose une palette AA pour UI sombre : #0B132B (fond), #1C2541 (surface), #2EC4B6 (accent), #5BC0BE (info), #EF476F (danger), texte #E6E8F0 / #A9B1C7. Génère un PNG “palette_typography.png” : chips + hex + “use for” + note AA ; type scale Inter (600–800), IBM Plex Sans (400–500), IBM Plex Mono. »
- **Sortie v1** : l’image contenait toutes les couleurs avec leurs hex, mais la police du type‑scale n’était pas reconnaissable et la note AA manquait.
- **Critique** : besoin d’indiquer explicitement l’usage (fond, surface, accent, etc.) et de vérifier le contraste du texte gris sur fond navy.
- **Prompt v2** : « Refais le spec sheet DOCin : chips de couleurs avec légendes – Primaire (fond), Surface, Accent, Info, Danger, Texte primaire, Texte secondaire – et mention “AA contrast OK”. Ajoute un encadré présentant les polices recommandées (Inter, IBM Plex Sans, IBM Plex Mono) et deux grilles de tailles (desktop : H1 36, H2 28, H3 22, body 16 pt; mobile : H1 28, H2 22, H3 18, body 15). Assure la lisibilité du texte sur fond sombre. »
- **Sortie v2** : document clair montrant chaque couleur avec son code, son usage et la mention AA, ainsi qu’un tableau de la hiérarchie typographique.
- **Rationale** : la v2 fournit un guide complet conforme aux standards d’accessibilité AA. Nous l’avons adopté sous le nom `palette_typography.png`.

## Carrousel LinkedIn

- **Prompt v1** : « Crée une image composite pour un carrousel LinkedIn (6 panneaux) de DOCin. Thème : palette teal/navy. Panneau 1 : “Vos PDF s’appellent Facture‑finale(12).pdf ?”. P2 : “Upload → renommage auto” avec icône d’upload. P3 : “Classement clair” avec icône de dossiers. P4 : “Recherche FTS instantanée” avec icône de recherche. P5 : “Local & Q/R avec source” avec icône d’un fichier et d’une chaîne. P6 : “Commentez BETA pour tester”. Minimal, typographie Inter, sépare les panneaux. »
- **Sortie v1** : l’image était joliment colorée, mais les panneaux manquaient de séparation et certaines phrases débordaient sur d’autres panneaux. Les icônes étaient surdimensionnées.
- **Critique** : améliorer la lisibilité en ajoutant des lignes de séparation, réduire les icônes et limiter le texte sur chaque panneau à l’essentiel.
- **Prompt v2** : « Recompose le carrousel DOCin en 6 cadres bien séparés par des lignes fines blanches. Utilise la palette (#0B132B, #2EC4B6) et réduis les icônes pour les aligner avec le texte. Chaque panneau doit avoir un titre court (voir v1) et un petit symbole. »
- **Sortie v2** : les six panneaux sont alignés, avec des marges claires et des icônes harmonieuses. Chaque message est facile à lire.
- **Rationale** : la v2 assure une meilleure hiérarchisation et respecte la charte graphique. Elle est retenue (`post_linkedin_carousel.png`).

## Couverture Shorts / TikTok

- **Prompt v1** : « Poster vertical 1080×1920 pour DOCin. Texte : “Classe, retrouve, répond.” en gros, centré. Palette teal/navy. Ajoute un petit logo DOCin. »
- **Sortie v1** : la couverture était lisible mais le contraste du texte sur fond bleu nuit manquait et le logo était trop petit.
- **Critique** : il faut un fond sombre uniforme avec un rectangle d’accent derrière la tagline et un logo plus visible.
- **Prompt v2** : « Refais l’affiche verticale pour DOCin. Utilise un fond navy (#0B132B). Place la tagline “Classe, retrouve, répond.” en blanc sur une pastille teal (#2EC4B6) légèrement transparente au centre. Affiche un logo DOCin plus grand en bas. »
- **Sortie v2** : design épuré avec une zone d’accent très lisible et un logo bien proportionné.
- **Rationale** : la v2 présente la tagline de façon percutante et respecte notre palette. Elle est adoptée (`post_short_cover.png`).

## Visuel X (Twitter)

- **Prompt v1** : « Crée une bannière 1600×900 pour un tweet : texte ‘Renommez. Classez. Retrouvez. Local.’ avec couleurs DOCin et un petit logo. »
- **Sortie v1** : l’image était sombre mais le texte était trop petit et les phrases trop espacées.
- **Critique** : augmenter la taille du texte et aligner les mots verticalement pour créer un rythme visuel. Assurer un contraste fort entre texte et fond.
- **Prompt v2** : « Recompose la bannière Twitter : affiche la phrase en quatre lignes (“Renommez.” “Classez.” “Retrouvez.” “Local.”) avec une police large blanc/teal sur fond navy. Dispose le logo DOCin en bas à droite. »
- **Sortie v2** : le texte est imposant et bien lisible, et l’ensemble respire.
- **Rationale** : la v2 maximise la lisibilité et véhicule le message en un coup d’œil (`post_x_card.png`).

## Storyboard de la vidéo 20–30 s

- **Prompt v1** : « Storyboard 5 plans (25 s) pour une démo de DOCin : 1) Logo 1,5 s, 2) Upload→Renommer/Classer 6 s (“1 clic”), 3) Recherche “facture EDF 2024” 5 s, 4) Q/R “Montant TTC mai 2024 ?” 7 s, 5) Tagline + CTA “Écris BETA” 4 s. Donne les textes à l’écran (≤ 5 mots) et la phrase de voix‑off. »
- **Sortie v1** : le storyboard décrivait les scènes mais manquait d’indications sur l’emplacement des textes et la synchronisation audio/vidéo.
- **Critique** : il est utile de préciser l’alignement des overlays (haut/bas), de proposer des transitions douces et d’harmoniser la durée de chaque plan.
- **Prompt v2** : « Affinons le storyboard : pour chaque plan, indique : (a) la durée, (b) l’action visuelle, (c) la position du texte à l’écran (haut/gauche/droite/bas), (d) le texte (≤ 5 mots), (e) la phrase de voix‑off. Plans : [Logo 1,5 s], [Upload→Renommage 6 s], [Recherche “facture EDF 2024” 5 s], [Q/R “Montant TTC mai 2024 ?” 7 s], [Tagline+CTA 4 s]. Utilise un ton calme et précis. »
- **Sortie v2** : le storyboard final décrit précisément chaque plan avec la disposition du texte (« 1 clic » en haut à droite, etc.), ce qui facilitera le montage.
- **Rationale** : même si nous ne produisons pas la vidéo dans cette livraison, ce storyboard documente notre intention et démontre notre maîtrise du prompting.
