# CH03.07 — Cours théorique : mains et pieds

## 1. Pourquoi ces deux zones
Elles sont petites mais très regardées ; une erreur de structure (cinq doigts ? pouce au bon endroit ?) se voit tout de suite.
On sculpte d'abord la **structure** (nombre, longueurs, articulations), puis les détails (plis, ongles, veines).

## 2. La main : repères moyens
| Élément | Repère | Solution mesurée |
|---|---|---|
| Longueur poignet → bout du majeur | ≈ 19–22 cm (adulte) | 21,9 cm (avec 4 cm de poignet) |
| Largeur, pouce écarté | ≈ 16–19 cm | 18,2 cm |
| Doigts | 4 doigts de **3 phalanges** (≈ 45 / 30 / 25 % de la longueur) | 3 segments |
| Longueurs | majeur > annulaire ≈ index > auriculaire | index 95 %, annulaire 96 % du majeur |
| Pouce | 2 phalanges + métacarpien qui part du poignet ; ≈ 60 % du majeur | 61 % |
| Épaisseur de la paume | ≈ 3–4 cm | 4,0 cm |
Les doigts **s'effilent** (base plus large que le bout) : majeur 19,4 mm à la base, 16,9 mm près du bout.
Les articulations sont des endroits un peu plus larges, séparés par des segments plus fins ; les creux de flexion (plis
de la paume) sont sur la face de la paume.

## 3. Le pied : repères moyens
| Élément | Repère | Solution mesurée |
|---|---|---|
| Longueur talon → gros orteil | ≈ 25–28 cm | 27,7 cm |
| Largeur de l'avant-pied (« balle ») | ≈ 9–11 cm | 11,1 cm |
| Talon / avant-pied | talon nettement plus étroit | 59 % |
| Voûte plantaire | le milieu ne touche pas le sol | 1,2 cm de dégagement |
| Appui | talon et balle | semelle plane de 112 cm² |
| Orteils | 5, le gros orteil le plus long et le plus épais, puis décroissance | 5 pics, ordre respecté |

## 4. Orientation et pose
Convention de ce chapitre : bout des doigts / orteils vers **+Y** ; main à plat (paume vers −Z), pouce vers +X ; pied posé sur
**z = 0**. Les **doigts légèrement écartés** : on peut les rapprocher au rig, jamais l'inverse (une moufle ne se sépare pas).

## 5. Garder les parties séparées
Voxel Remesh referme les petits écarts (entre orteils de 2–4 mm, par exemple) : choisir un Voxel Size inférieur à la moitié de
l'écart, ou garder les orteils écartés de ≥ 5 mm dans la pose de sculpture. Un lissage trop fort fusionne aussi.

## 6. Mesurer sur la silhouette
Vue de dessus, chaque doigt (ou orteil) séparé donne un **pic** dans le profil ; le correcteur compte les pics dont la
proéminence dépasse un seuil (≥ 2 cm pour les doigts, ≥ 6 mm pour les orteils). Une moufle de test : 2 pics ; quatre doigts :
4 pics. Avantage : ça ne dépend ni de l'ordre des sommets ni de la densité du maillage.

## 7. Limites
Le correcteur juge la structure, pas la beauté ni la finesse des détails. Les solutions fournies sont **simplifiées** (ellipsoïdes
lissés) : un mannequin de main, un pied stylisé ; à vous d'y ajouter l'anatomie (tendons, veines, ongles, plis).
