# CH06.05 — Cours théorique : rig humanoïde avec Rigify

## 1. Rigify
**Rigify** est un module fourni avec Blender (activé par `bpy.ops.preferences.addon_enable(module='rigify')`). Il part d'un **méta-rig** (un squelette de description, `bpy.ops.object.armature_human_metarig_add()` : 159 bones) que l'on ajuste au personnage, et **génère** le rig (`bpy.ops.pose.rigify_generate()`) : ici 706 bones.
Rig généré : os déformants `DEF-*`, os d'origine `ORG-*`, mécanismes `MCH-*`, contrôleurs (`root`, `torso`, `hips`, `chest`, `hand_ik.L`, `foot_ik.L`, `head`…), et des **collections de bones** (Face, Torso, Fingers, Arm.L (IK), Arm.L (FK), Leg.L (IK)…) pour masquer ou afficher des groupes de contrôleurs.

## 2. Procédure du chapitre
1. Add > Armature > Human (entrée ajoutée par Rigify ; opérateur « Add Human (metarig) ») ; hauteur du méta-rig : 1,98 m (x de −0,79 à +0,79 m).
2. Mise à l'échelle sur le corps (1,759 / 1,98 = 0,889), puis Ctrl+A > Scale : échelle de l'objet 1.
3. **Ajuster les bras** en Edit Mode (obligatoire ici, voir §4) : le méta-rig a les bras à ≈ 29° sous l'horizontale et une chaîne trop courte ; le mannequin les a à ≈ 51° (pose en A) jusqu'au bout des doigts (≈ 0,66 m du centre). Placer le **coude** et le **poignet** au milieu du bras, vus de face ET de profil, garder le coude très légèrement en arrière (1–2 cm) pour donner à l'IK son sens de pliage, puis tourner/allonger la main et les doigts dans l'axe. Avec le bouton de symétrie **X** de l'en-tête (Edit Mode d'armature), le côté droit suit.
4. Generate Rig : un objet « rig » ; ici renommé RIG_Hero.
5. Corps : sélectionné, puis RIG_Hero actif : Ctrl+P > With Automatic Weights (bones DEF- seulement : 160 groupes) ; Normalize All ; Limit Total 4 ; Normalize All.

## 3. Mesures de la solution
706 bones ; bras : coudes et poignets à 1,7 cm au plus du centre de la section du bras (avant ajustement : poignets HORS du bras) ; sommet des bones DEF à 1,759 m ; pieds à z = +0,015 m ; rig centré (écart 0 cm) ; 100 % des sommets pesés, somme 1, ≤ 4 influences. Racine +0,5 m : déplacement moyen 0,500 m. Pied gauche levé de 0,25 m : le pied du corps monte de 0,243 m ; pied droit et tête : 0,0 mm.

## 4. Limites du chapitre
- Sans ajustement, les bras du méta-rig passent au-dessus des bras du mannequin et la main du rig tombe hors du maillage : les sommets des bras pèsent alors sur les os les plus proches, mal placés. La solution est ajustée (étape 3) ; le correcteur mesure la position des coudes et poignets.
- Le correcteur teste le corps, la tête, les jambes et la position des bras ; il ne teste ni les doigts ni le visage, ni la déformation des bras en pose.
- Rigify génère un rig lourd ; une scène avec plusieurs personnages demande de le masquer ou de le simplifier (CH06.11).

## 5. Pièges
- Générer avant d'avoir appliqué l'échelle du méta-rig.
- Parenter le corps au méta-rig au lieu du rig généré.
- Décaler le méta-rig en X (la génération ignore l'emplacement : seul le rig généré compte, ici placé à l'origine).
- Oublier de normaliser après Automatic Weights.
- Oublier que seules les collections visibles montrent les contrôleurs.

## 6. Contrôle
Le correcteur règle des poses (racine, pied IK) ; ne modifiez pas la pose de repos de votre fichier.
