# CH06.06 — Cours théorique : rig quadrupède

## 1. Méta-rigs de créatures
Rigify propose, en plus du Human : **Basic Human**, **Basic Quadruped**, **Cat**, **Horse**, **Wolf**, **Bird**, **Shark** (opérateurs `bpy.ops.object.armature_*_metarig_add`). Le méta-rig **Basic Quadruped** compte 34 bones : colonne et queue en 12 segments (`spine`, `spine.001` à `spine.011`, tête incluse), épaules (`shoulder.L/.R`), pattes avant (`front_thigh`, `front_shin`, `front_foot`, `front_toe`), pattes arrière (`thigh`, `shin`, `foot`, `toe`), bassin (`pelvis.L/.R`), poitrine (`breast.L/.R`). Étendue d'origine : y de −0,66 (museau) à +1,10 (bout de queue), z de 0 à 0,98.

## 2. Générer et lier
Même procédure que le rig humain : `bpy.ops.pose.rigify_generate()` donne 283 bones (collections : Spine, Leg.L/R (IK/FK/Tweak), Arm.L/R… pour les pattes avant, Tail, Root, ORG, MCH, DEF). `parent_set(type='ARMATURE_AUTO')` ne pèse que sur les `DEF-*` (47 bones). Contrôleurs IK : `foot_ik.L/.R` (arrière), `front_foot_ik.L/.R` (avant), `root`, `torso`.

## 3. La créature de l'exercice
Maillage de capsules (cônes à 10 côtés) construites le long des os du méta-rig : colonne (rayon 0,035–0,15), cou, tête, quatre pattes (0,06 → 0,03). Elle n'a aucun détail : elle sert à tester le rig, pas à être belle.

## 4. Mesures de la solution
283 bones ; écarts rig/créature : 3,9 et 0,5 cm en Y, 6,6 cm en hauteur ; pattes au sol ; centrage 0 cm ; 100 % des sommets pesés, somme 1, ≤ 4 influences. Racine +0,5 m : moyenne 0,500 m. Patte avant gauche levée de 0,15 m : la patte monte de 0,150 m ; les trois autres pattes : 0,0 mm.
Contre-exemples : méta-rig à l'échelle 1,4 : écarts de 22, 44 et 33 cm ; rig décalé de 0,5 m : pied qui ne monte pas ; poids supprimés aux pattes avant : 77 % de sommets pesés.

## 5. Pièges
- Méta-rig déplacé ou mis à l'échelle sans ajuster la créature (ou l'inverse).
- Parenter la créature au méta-rig.
- Pattes arrière : l'articulation « genou » est un jarret ; ne pas la remplacer par un genou humain.
- Poids entre pattes avant très proches : peindre ou séparer les groupes.
- Rig de 283 bones : masquer les collections inutiles.

## 6. Limites
Un quadrupède de base, sans oreilles, mâchoire ni doigts ; le correcteur teste la peau globale, la racine et une patte avant. Le méta-rig Cat (174 bones) ou Wolf (190) est plus riche mais demande un maillage soigné.
