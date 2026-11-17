# CH07.02 — Cours théorique : Keyframes et timeline

## 1. Clés, courbes, interpolation
Une **clé** associe une valeur à une image pour une propriété (ex. la position en X). Les clés d'une propriété forment une **courbe d'animation** (F-curve) ; l'**interpolation** décide du trajet entre deux clés : Bezier (par défaut : accélère puis freine), Linear (vitesse constante), Constant (marche d'escalier). Les poignées Auto Clamped évitent les dépassements.

## 2. Timeline
Plage (début, fin), cadence (24 i/s ici), image courante. Les **marqueurs** nomment des images (M ajoute, F2 ouvre le nom ; touches de la keymap par défaut, vérifiées dans `blender_default.py`).

## 3. Insérer des clés
Touche **I** en vue 3D (keymap par défaut : `anim.keyframe_insert`) ; K ouvre le menu des Keying Sets. En Python : `obj.keyframe_insert("location", frame=24)`. Dope Sheet et Graph Editor : touche **T** (type d'interpolation).

## 4. L'exercice
GEO_Crate, 72 images à 24 i/s. Position X : 0 (image 1), 4 (24), 4 (48), 0 (72). Rotation Z : 0° (24), 90° (48), 90° (72), interpolation linéaire. Marqueurs « arrive » (24) et « turn_end » (48).

## 5. Mesures
Solution : 34/34. Maintien X entre 28 et 44 : 4,000. Rotation à l'image 30 : 22,5° (linéaire) contre 14,1° (Bezier, contre-exemple). Intervalle de X : 0 à 4,00. Contre-exemples : plage 1–60 ; clé de l'image 48 à 3,5 (X dérive à 3,71) ; clés décalées d'une image (25, 49) ; pas de marqueurs ; pas de rotation.

## 6. Pièges
- Clés décalées d'une image par erreur de curseur.
- Oublier la plage de fin (le rendu produit 250 images).
- Rotation par défaut en Bezier : la caisse accélère au lieu de tourner à vitesse constante.
- Maintien manquant : la valeur dérive.
- Clé insérée sur un autre canal sans le vouloir.

## 7. Limites
Une seule caisse, deux canaux ; pas de Keying Sets personnalisés ni d'auto-key testés ; l'esthétique du mouvement n'est pas jugée (CH07.04 et CH07.05 l'approfondissent).
