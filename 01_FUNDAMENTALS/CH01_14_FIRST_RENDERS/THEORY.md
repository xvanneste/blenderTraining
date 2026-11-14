# CH01.14 — Cours théorique : vos premiers rendus

## 1. Rendre, c'est calculer l'image finale
Le viewport montre une approximation interactive ; le **rendu** calcule l'image définitive à
la résolution et à la qualité choisies. `F12` rend l'image courante (*Render → Render
Image*), `Ctrl+F12` l'animation (*Render Animation*). La fenêtre de rendu (un *Image Editor*)
affiche le résultat, le temps (*Time*) et la mémoire (*Mem*, *Peak*).

## 2. EEVEE ou Cycles ?
| | **EEVEE** | **Cycles** |
|---|---|---|
| Principe | Rastérisation temps réel + ray tracing écran/matériel optionnel | *Path tracing* : simulation des trajets de la lumière |
| Vitesse | Secondes ou moins par image | Secondes à minutes (GPU), plus en CPU |
| Réalisme | Très bon pour la stylisation, plus approximatif pour le verre, les caustiques, la lumière indirecte complexe | Physiquement fondé : rebonds, ombres douces, réfractions |
| Bruit | Peu (anti-crénelage temporel) | Du bruit, réduit par plus d'échantillons + débruitage |
| Usage | Previz, animation stylisée, look dev rapide, motion design | Rendus réalistes, finaux de film, images fixes |
Règle : **régler en EEVEE, valider en Cycles** quand le réalisme compte. Les deux utilisent
les mêmes matériaux (le Principled BSDF) et les mêmes lumières.

## 3. Les réglages de Cycles à connaître
*Properties → Render* :
- **Device** : *GPU Compute* (CH00.01).
- **Sampling → Render** : *Noise Threshold* (échantillonnage adaptatif : Cycles s'arrête
  quand un pixel est assez propre ; 0,01 = très propre, 0,05 = plus rapide), *Max Samples*
  (plafond, ex. 128–1024), *Time Limit*.
- **Denoise** : supprime le bruit restant (*OpenImageDenoise* par défaut, CPU ou GPU ;
  *OptiX* sur NVIDIA). Permet de rendre avec moins d'échantillons.
- **Light Paths** (phase 10) : nombre de rebonds.
Pour EEVEE : *Sampling → Render → Samples* (anti-crénelage, ombres douces), options de ray
tracing et d'ombres (phase 10).

## 4. Résolution et format de sortie
*Output → Format* : résolution, %, cadence (CH01.09).
*Output → Output* :
- **Chemin** : `//renders/nom_` (relatif ; pour une animation, Blender ajoute `0001`, `0002`…).
- **File Format** : *PNG* (sans perte, 8 ou 16 bits, transparence possible avec *RGBA* et
  *Film → Transparent*), *JPEG* (aperçus seulement), *OpenEXR* (production, phase 10),
  *FFmpeg Video* (vidéo directe — déconseillé pour un rendu long : en cas de plantage tout
  est perdu ; rendez des images puis montez).
- **Color** : BW / RGB / RGBA ; **Color Depth** : 8 bits (diffusion), 16 bits (retouche).

## 5. Gestion des couleurs (Color Management)
*Render → Color Management* : comment les valeurs physiques de lumière deviennent des
couleurs d'écran.
| View Transform (5.3) | Usage |
|---|---|
| **AgX** (défaut) | Rendu « filmique » moderne : les fortes lumières passent doucement au blanc, les couleurs saturées se comportent naturellement |
| Standard | Correspondance directe : couleurs d'interface, motion design, images techniques |
| Filmic | Ancien défaut (avant 4.0) |
| ACES 1.3 / ACES 2.0 | Pipelines ACES (échanges avec étalonnage pro) |
| Khronos PBR Neutral | Rendu fidèle des couleurs de produits (e-commerce) |
| False Color | Diagnostic de l'exposition (zones sous/surexposées) |
| Raw | Données brutes (non visuelles) |
Le **Look** ajuste le contraste (*AgX - Punchy*, *AgX - Medium High Contrast*, *AgX - Base
Contrast*…). *Exposure* et *Gamma* corrigent globalement. Ces réglages sont enregistrés dans
la scène et appliqués aux images 8/16 bits (pas aux EXR, qui gardent les valeurs linéaires).

## 6. Enregistrer l'image
`F12` **n'enregistre rien** : dans la fenêtre de rendu, *Image → Save As* (`Shift+Alt+S`).
Les **slots** (menu *Slot* de la fenêtre de rendu, ou touches `1`…`8` au survol) gardent
plusieurs rendus pour les comparer (`J` alterne entre les deux derniers).
En ligne de commande (CH00.01) : `blender -b fichier.blend -f 1` enregistre directement dans
le chemin de sortie.

## 7. En production
On ne rend jamais « à la main » les images d'un film : les plans partent en **file de rendu**
(ligne de commande, render farm, phase 10) avec des réglages validés par séquence. Mais
chaque artiste fait des **rendus de test** fréquents, à basse résolution et peu d'échantillons,
pour décider vite.
