# CH06.03 — Cours théorique : skinning

## 1. Principe
Le **skinning** déforme un maillage par une armature. Chaque sommet porte, dans des **groupes de sommets** (`object.vertex_groups`), des **poids** (0–1) ; le groupe porte le nom d'un bone. Le **modificateur Armature** (`ARMATURE`, `object` = l'armature) transforme chaque sommet par la moyenne pondérée des transformations des bones.

## 2. Lier
Maillage sélectionné, armature active : **Ctrl+P > With Automatic Weights** (`bpy.ops.object.parent_set(type='ARMATURE_AUTO')`) : parente le maillage à l'armature, crée les groupes (un par bone déformant) et le modificateur, calcule des poids par diffusion de chaleur. Autres options : *With Empty Groups* (groupes vides), *With Envelope Weights*.
Ici : tube de 496 sommets, bones `upper` (0–0,30 m) et `fore` (0,30–0,60 m) → deux groupes.

## 3. Qualité des poids
- **Tous les sommets pesés** (un sommet sans poids reste immobile).
- **Somme = 1** : Weights > **Normalize All** (`vertex_group_normalize_all`) ; Automatic Weights a laissé 0,978 par endroits.
- **≤ 4 influences** par sommet (Limit Total).
- **Noms = bones** : un groupe sans bone ne sert à rien.
- **Transition progressive** aux articulations.

## 4. Le test de pliage
`pose_bone.rotation_euler = (0, 0, 90°)` sur `fore`, puis évaluation du maillage. Le correcteur mesure : racine (x < 0,10 m) déplacée de ≤ 5 mm ; bout (x > 0,55 m) à ≤ 2 cm de la position d'un solide tournant de 90° autour du coude (0,30 ; 0 ; 0) ; arête la plus étirée ≤ 2,2 × sa longueur au repos.
Solution : racine 0,0 mm, bout 0,0 mm, étirement ×1,71. Poids binaires : ×4,30. Sommets non pesés : ×16,8.

## 5. Pièges
- Sommets non pesés : trous qui restent derrière.
- Poids binaires : coude cassé.
- Groupes mal nommés : le mauvais bone déforme.
- Trop d'influences : tronquées à l'export.
- Oublier de normaliser après une retouche.
- Rotation d'un bone en Edit Mode : change la pose de repos, pas la pose.

## 6. Limites
Un tube à deux bones : le skinning d'un personnage (épaules, hanches, doigts) demande de la peinture de poids par zone (CH06.05). Le correcteur teste un seul pliage de 90° autour de Z ; il ne mesure pas la conservation du volume.
