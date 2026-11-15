# CH02.12 — Cours théorique : modéliser pour l'animation

## 1. Un maillage déformable n'est pas un maillage figé
Un décor reste immobile ; un personnage, un câble, un tissu **plient**. Lors d'une déformation par
armature (phase 6), chaque sommet suit les os selon des **poids** ; entre deux os, il est
**interpolé**. S'il y a trop peu de géométrie au pli, l'interpolation écrase la forme : le coude
« s'effondre », se vrille, perd du volume.

## 2. Mesure du chapitre
Bras de 60 cm (Ø 10 cm), plié à 90° au coude, poids lissés sur ±3 cm :
| Topologie | Volume conservé |
|---|---|
| 4 segments réguliers (1 boucle au coude) | **87,5 %** — coude écrasé (`ch02_12_arm_bent_starter.png`) |
| + 4 boucles serrées autour du coude | **97,5 %** (`ch02_12_arm_bent_solution.png`) |
| 40 segments réguliers (lourd) | 98,4 % |
Leçon : il ne faut pas **plus** de géométrie partout, il en faut **là où ça plie**.

## 3. Règles de topologie pour la déformation
- **Boucles d'articulation** : 3 boucles minimum autour de chaque articulation (coude, genou,
  doigts, cou, poignet), resserrées vers le pli ; plus pour les grandes amplitudes (épaule, hanche).
- **Anneaux continus** : les boucles font le tour complet du membre (pas de triangle ni de n-gon qui
  interrompt l'anneau).
- **Pôles hors des zones de pli** (CH02.01).
- **Densité régulière** ailleurs : des quads de taille proche facilitent les poids et la subdivision.
- **Visage** : boucles concentriques autour des yeux et de la bouche (phase 3).
- Pose de modélisation : **A-pose** ou **T-pose**, bras légèrement fléchis, mains ouvertes : les poids
  se peignent mieux sur des membres écartés.

## 4. Échelle et transformations
- **Échelle réelle** : un personnage de 1,75 m mesure 1,75 m (physique, profondeur de champ,
  simulations, cohérence entre plans).
- **Transformations appliquées** (`Ctrl+A` → *All Transforms*) avant le rig : échelle 1, rotation 0,
  origine aux pieds.
- Avant (Y négatif) et symétrie sur l'axe X (Mirror, phase 6 : noms .L/.R).

## 5. Tester tôt
Ajoutez une armature simple dès la modélisation et pliez (Pose Mode, `R`) : un problème vu à cette
étape coûte dix fois moins qu'en animation. Les **Loop Cuts** interpolent automatiquement les poids
existants : on peut ajouter des boucles même après le skinning.
