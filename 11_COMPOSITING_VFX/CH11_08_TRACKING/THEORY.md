# CH11.08 — Cours théorique : Tracking et matchmoving

## 1. Le tracking
Suivre des motifs (patterns) de l'image d'une image à l'autre : une piste = une suite de marqueurs.

## 2. La caméra du clip
Movie Clip Editor > Tracking > Camera : Focal Length (mm), Sensor Width, distorsion. API : `clip.tracking.camera`. Attention : changer la largeur du capteur recalcule la focale en mm ; réglez le capteur d'abord, puis la focale.

## 3. Detect Features et Track Markers
Detect Features crée des pistes sur les points contrastés de l'image courante ; Track Markers suit les pistes sélectionnées (vers l'avant sur toute la séquence).

## 4. Le solveur
Solve Camera Motion calcule la caméra et la position 3D des points. Il faut au moins 8 pistes communes entre deux images clés et du mouvement de translation.

## 5. L'erreur
Erreur de reprojection moyenne en pixels : ≤ 1 est acceptable ; la solution fait 0,75.

## 6. L'exercice
Clip de 40 images ; focale 35 mm ; ≥ 12 pistes de ≥ 30 marqueurs ; erreur ≤ 1,0 pixel.

## 7. Pièges
- Une rotation pure sans translation : pas de profondeur.
- Trop peu de pistes ou des pistes trop courtes.
- Mauvaise focale (la reconstruction peut quand même « réussir »).
- Un chemin de clip relatif cassé (le clip passe à 256 × 256 : constaté).

## 8. Limites
Plan synthétique parfait ; pas de nettoyage de pistes ; pas de setup de scène (Set Floor, Set Origin) ; pas de caméra solved appliquée à une scène.
