# CH04.04 — Cours théorique : Shader Editor et nœuds

## 1. Principe
Un matériau est un graphe : des **nœuds** (boîtes) reliés par des **liens**. Chaque nœud a des **entrées** (à gauche) et des **sorties** (à droite). Le flux va des textures vers le shader (Principled BSDF) puis vers le **Material Output** (entrée *Surface*).

## 2. Les nœuds du chapitre (types de l'API 5.3)
| Nœud (interface) | Type API | Rôle |
|---|---|---|
| Texture Coordinate | TEX_COORD | Fournit des coordonnées (Object, Generated, UV, Camera, Window…) |
| Mapping | MAPPING | Location / Rotation / Scale du vecteur |
| Noise Texture | TEX_NOISE | Bruit fractal (Scale, Detail, Roughness) |
| Color Ramp | VALTORGB | Valeur 0–1 → couleur, par stops |
| Mix | MIX | Mélange A/B selon un facteur (type de données Color ici) |
| Map Range | MAP_RANGE | Change de plage : (From Min/Max) → (To Min/Max) |
| Principled BSDF | BSDF_PRINCIPLED | Shader de CH04.03 |
| Material Output | OUTPUT_MATERIAL | Résultat du matériau |

## 3. Le graphe de la solution
```
Texture Coordinate [Object] → Mapping → Noise Texture [Fac] ┬→ Color Ramp ┬→ Mix [Factor] (A rouille, B acier) → Base Color
                                                            │             └→ Metallic
                                                            └→ Map Range → Roughness
Principled BSDF → Material Output [Surface]
```
Un seul masque (la rampe) pilote la couleur ET le caractère métallique : l'acier propre est métallique, la rouille ne l'est pas. La rugosité vient directement du bruit, remis à l'échelle par Map Range (0,25–0,85).
Valeurs : Noise Scale 6, Detail 8, Roughness 0,6 ; rampe : stop 0 en position 0,45 (blanc), stop 1 en 0,62 (noir) ; acier (0,50 ; 0,52 ; 0,55), rouille (0,45 ; 0,15 ; 0,05).

## 4. Bonnes pratiques
- Lire de gauche à droite ; garder des liens courts ; pas de nœud orphelin.
- Un masque unique pour des paramètres cohérents (couleur, métal, rugosité).
- Régler Mapping avant de régler la texture.
- Frames et labels pour les graphes plus grands.

## 5. Pièges
- Mix en type Float au lieu de Color : le résultat ne se branche plus proprement sur Base Color.
- Metallic constant : la rouille reste brillante comme le métal.
- Échelle excessive du bruit : aspect de sable.
- Pas de Mapping : impossible de décaler ou d'orienter la texture.

## 6. Limites
Le correcteur lit la structure du graphe et quelques valeurs ; il ne juge pas l'apparence : toujours regarder le rendu. Il n'évalue que le premier Noise relié à Base Color.
