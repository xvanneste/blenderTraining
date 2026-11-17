# CH06.01 — Cours théorique : armatures et bones

## 1. Anatomie d'un bone
Un **bone** (os) a une **tête** (head), une **queue** (tail) et un **roll** (rotation autour de son axe). En **Edit Mode** on place tête et queue (`armature.edit_bones`, `.head`, `.tail`, `.roll`) ; en **Pose Mode** on pose les bones (`object.pose.bones`, `.location`, `.rotation_*`, `.scale`) sans toucher à la position de repos ; en Object Mode on lit `armature.bones` (`head_local`, `tail_local`).
Options clés : `parent`, `use_connect`, `use_deform`.

## 2. Hiérarchie et connexions
Le **parent** transmet ses mouvements à ses enfants. **Connected** (`use_connect`) colle la tête de l'enfant à la queue du parent : c'est le cas de la colonne, du cou, de la tête, des chaînes de bras (forearm, hand) et de jambe (shin, foot, toe). Les **épaules** et les **cuisses** ne sont pas connectées : elles partent du côté de la colonne ou du bassin.
```
root ─ pelvis ─┬─ spine.001 ─ spine.002 ─ spine.003 ─┬─ neck ─ head
               │                                     └─ shoulder.L/.R ─ upper_arm ─ forearm ─ hand
               └─ thigh.L/.R ─ shin ─ foot ─ toe
```

## 3. Nommage
- Côtés : suffixes **.L** (gauche, +X) et **.R** (droite, −X) ; Blender s'en sert pour les miroirs.
- Numérotation : spine.001, spine.002… ; minuscules, pas d'espaces.
- Jamais de « Bone », « Bone.001 » : ils cachent le rôle.
- `root` : racine au sol.

## 4. Symétrie
**Armature > Symmetrize** (Edit Mode) recopie un côté sur l'autre (X → −X) ; roll opposé pour des images miroirs (ici roll nul des deux côtés). Les bones du centre restent sur x = 0.

## 5. Pose de repos et déformation
La pose de repos est neutre : tous les bones en identité en Pose Mode (Pose > Clear Transform). `root` ne déforme pas ; les autres bones ont **Deform** actif (ils influenceront le maillage au skinning, CH06.03).

## 6. Dimensions de la solution (A-pose, 1,76 m)
pelvis 0,95 → 1,05 ; spine 1,05 → 1,45 (3 bones) ; neck 1,45 → 1,58 ; head 1,58 → 1,76 ; shoulder 0,03 → 0,17 en x à z = 1,42 ; bras de 0,30 + 0,27 + 0,10 m à 40° de la verticale ; cuisse 0,95 → 0,52, tibia 0,52 → 0,09, pied jusqu'à y = −0,18, orteils jusqu'à −0,26 (z = 0).

## 7. Pièges
- Noms par défaut « Bone.001 » : plus rien n'est reconnu.
- Un seul côté construit : le miroir ne marche pas.
- Chaîne déconnectée : un trou apparaît quand le parent bouge.
- Pose de repos sale : l'animation « tire » au départ.
- Échelle de l'objet ≠ 1 : tout l'ensemble du rig déraille.

## 8. Limites
Le squelette est volontairement simple (pas de doigts, de bones de visage ni de contrôleurs) : il est la base de CH06.02 à CH06.05. Le correcteur contrôle la structure et les positions, pas la qualité de la déformation.
