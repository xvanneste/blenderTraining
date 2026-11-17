# CH18.02 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch18_02_perspective_starter.blend`, sélectionnez `GP_Practice`,
`Ctrl+Tab` → Draw Mode, `Num 0`.

## Tutoriel 1 — Le couloir à 1 point (USER_OnePoint)
1. Calque **USER_OnePoint** actif (`Y` → USER_OnePoint).
2. Outil **Line** (barre `T`). Tracez un petit rectangle autour du PF : le **mur du fond**.
3. Reliez ses 4 coins aux 4 coins du cadre : murs, sol, plafond.
4. Portes du mur gauche : deux verticales (plus rapprochées pour la porte la plus lointaine),
   reliées en haut et en bas par des lignes **qui visent le PF**.
5. Une fenêtre sur le mur droit, plus haute que les portes, même méthode.
6. Carrelage : 4 lignes du bord inférieur vers le PF.

## Tutoriel 2 — La rue à 2 points (USER_TwoPoint)
1. Calque **USER_TwoPoint**. Les deux PF sont **hors cadre** sur la ligne d'horizon : suivez
   les fuyantes bleues.
2. Pour chaque bâtiment : arête verticale avant, puis bas et haut vers chaque PF, puis
   verticales arrière (méthode des boîtes de CH18.01).
3. Fenêtres : lignes parallèles aux fuyantes du côté concerné.
4. Variez hauteurs et largeurs ; un bâtiment doit en cacher partiellement un autre.

## Tutoriel 3 — La tour à 3 points (USER_ThreePoint)
1. Calque **USER_ThreePoint**. L'horizon est bas : la caméra regarde vers le haut.
2. Les verticales de la tour suivent les fuyantes bleues qui convergent vers le haut.
3. Étages : lignes à peu près horizontales qui se resserrent en montant.

## Tutoriel 4 — Comparer avec une caméra Blender (5 min)
1. Object Mode, nouvel onglet de scène ou nouveau fichier : `Shift+A` → *Mesh → Cube*,
   étirez-le en tour (`S Z 5`).
2. Caméra au pied de la tour, tournée vers le haut, focale 18 mm : `Num 0`.
   Les arêtes verticales convergent : c'est votre 3e point de fuite.

## Tutoriel 5 — Vérifier
Enregistrez `ch18_02_perspective_<prenom>_v001.blend` puis :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_02_perspective_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch18_02.py" -- --exercise perspective --render
```
Référence : `COMPLETED_EXAMPLES/ch18_02_perspective_reference.png`.

## Variante de contrôle

Sur une copie du couloir, déplacez l’horizon et reconstruisez les fuyantes. Comparez avec une variante qui garde la hauteur et change le point de fuite horizontal. **Preuve** Vous distinguez changement de hauteur du regard et changement de direction.
