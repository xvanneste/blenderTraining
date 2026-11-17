# CH07.14 — Cours théorique : Motion capture

## 1. Le BVH
Fichier texte : une section HIERARCHY (joints, décalages, canaux) puis une section MOTION (nombre d'images, durée d'une image, une ligne de valeurs par image). L'import (`bpy.ops.import_anim.bvh`) crée une armature et une action avec une clé par image et par canal.

## 2. Le fichier de l'exercice
`ch07_14_mocap_noisy.bvh` : quatre joints (Hips avec position et rotation, Spine, Head, Arm_L), 96 images à 24 i/s ; une oscillation de période 24 images par joint ; bruit de 1° (3 mm) et trois glitches de 9° (et 4 cm sur la hauteur des hanches à l'image 48). Importé : 15 courbes de 96 clés.

## 3. Diagnostic
Rugosité : écart quadratique moyen de la différence seconde (le bruit la gonfle). Glitches : valeurs à plus de 15 % de l'amplitude de la courbe lissée. Courbes de pur bruit : amplitude utile inférieure à 0,05 rad (rotations) ou 0,02 m.

## 4. Nettoyage
1. **Retirer les glitches** (médiane glissante sur 5 images) ; 2. **Lisser** (gaussien de σ = 1,2 image : atténuation de l'amplitude d'environ 5 % pour une période de 24 images) ; 3. **Décimer** (Ramer-Douglas-Peucker : tolérance de 3 % de l'amplitude, au moins un quart du plancher d'amplitude) ; 4. **Bezier** sur les clés restantes. Opérateurs du Graph Editor correspondants : Smooth (Gaussian), Decimate (Allowed Change), Clean Keyframes, interpolation Bezier.

## 5. Contrôles du correcteur
Rugosité ≤ 50 % du brut ; fidélité (écart quadratique à la référence : médiane 5 puis gaussien σ = 1,5) ≤ 8 % de l'amplitude ; amplitude conservée ≥ 90 % ; glitches (écart maximal) ≤ 15 % ; ≤ 38 clés par courbe ; clés Bezier ; MOCAP_RAW intacte.

## 6. Mesures
Solution : 38/38 ; rugosité 29 % ; fidélité 6,6 % ; amplitude 100 % ; écart maximal 12,7 % ; 32 clés au plus ; Spine Z : 28 clés ; total 211 clés (1 440 au départ). Contre-exemples : brute (rugosité 100 %) ; σ = 6 (amplitude 28 %) ; glitches conservés (écart 50 %) ; 96 clés ; clés linéaires ; copie brute nettoyée.

## 7. Pièges
- Lisser sans retirer les glitches.
- Lisser trop (le mouvement s'écrase).
- Décimer avant de nettoyer.
- Modifier la copie brute.
- Clés linéaires après décimation.

## 8. Limites
BVH synthétique de quatre joints ; pas de retargeting sur un rig de personnage (autre rig, autre hiérarchie) ; pas de pieds au sol (foot locking) ni de mocap faciale ; le correcteur compare à une référence calculée, pas à une vérité artistique.
