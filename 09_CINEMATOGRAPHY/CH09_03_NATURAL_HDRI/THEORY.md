# CH09.03 — Cours théorique : Naturel et HDRI

## 1. Le monde comme source
Le monde (World) éclaire toute la scène. Un fond uni donne une lumière douce sans direction ; une image d'environnement apporte la direction et la couleur.

## 2. HDRI
Une image équirectangulaire en virgule flottante (ici 256 × 128, EXR) : ciel de 0,1 à 1, soleil à 1 500. Elle est générée par `build_ch09_03_files.py` (pas une photo : dégradé de ciel + disque de soleil de 2,5° à 20° au-dessus de l'horizon). Une vraie HDRI se télécharge (vérifier la licence) ; la méthode est identique.

## 3. Les nœuds
Texture Coordinate (Generated) → Mapping → Environment Texture → Background → World Output. La rotation Z du Mapping fait tourner l'environnement autour de la verticale.

## 4. L'exercice
Sol de 10 × 10 m (gris 50 %), poteau de 1 m, caméra orthographique au zénith. Sans rotation l'ombre part vers −X (le soleil est à +X) ; avec 180° elle part vers +X.

## 5. Exposition
Strength multiplie l'environnement : 1 → sol à 0,59 ; l'exposition est linéaire en Strength. Le correcteur demande 0,35 à 0,8.

## 6. Ombre
Ombre nette (soleil petit et intense) et bleutée (fond de ciel). Mesures : 73 pixels d'ombre, angle 0°, bleu / rouge 1,68.

## 7. Pièges
- Image 8 bits : pas de soleil réel.
- Rotation oubliée : le soleil est du mauvais côté.
- Strength confondu avec la rotation.
- Bruit : un soleil minuscule demande des échantillons (64 suffisent ici pour la mesure).

## 8. Limites
HDRI synthétique ; une seule heure de la journée ; pas de Sky Texture (ciel Nishita) ; pas de réflexions sur un sujet brillant ; l'exposition est mesurée sur un sol mat.
