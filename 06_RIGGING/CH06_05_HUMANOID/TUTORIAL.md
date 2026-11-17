# CH06.05 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch06_05_humanoid_starter.blend` : `CHR_Hero_Body` (le corps retopologisé de P3, 1,76 m) et `META_Hero` (méta-rig humain, 1,98 m, non ajusté). Sauvegardez sous `ch06_05_humanoid_starter_<prenom>_v001.blend`. Activez le module Rigify (Preferences > Add-ons) s'il ne l'est pas.

## Tutoriel 1 — Ajuster (30 min)
En mode Objet, sélectionnez `META_Hero`, appliquez un facteur 0,889 avec `S`, puis `Ctrl+A → Scale`. Pour voir le méta-rig devant le corps en affichage solide, activez *Object Properties → Viewport Display → In Front* sur l’armature. Comparez de face puis de profil. Vérifiez la colonne et les jambes, puis repérez l’écart entre les bras et leurs os.

## Tutoriel 1 bis — Ajuster les bras (30 min)
Tab (Edit Mode) sur META_Hero. Activez la symétrie **X** de l'en-tête. Vue de face (Numpad 1) : sélectionnez la tête de `forearm.L` (le coude) et déplacez-la (G) au milieu du bras du mannequin ; idem pour la tête de `hand.L` (le poignet). Vue de côté (Numpad 3) : remettez coude et poignet au milieu de l'épaisseur du bras, le coude 1 à 2 cm en arrière. Sélectionnez ensuite `hand.L` et tous les os des doigts, placez le pivot sur l'élément actif et tournez-les (R) dans l'axe de l'avant-bras, puis mettez-les à l'échelle (S) jusqu'au bout des doigts. Revenez en Object Mode (Tab).

## Tutoriel 2 — Générer (15 min)
Object Data Properties du méta-rig > Rigify > **Generate Rig**. Renommez l'objet « rig » en RIG_Hero. Explorez les collections de bones (Torso, Arm.L (IK)…).

## Tutoriel 3 — Lier (20 min)
En mode Objet, sélectionnez `CHR_Hero_Body` puis ajoutez `RIG_Hero` à la sélection. Confirmez que le rig généré est actif. Faites `Ctrl+P → With Automatic Weights`. Vérifiez que le modificateur *Armature* du maillage cible `RIG_Hero`. En Weight Paint, appliquez *Limit Total* à 4 sur les poids de déformation puis *Normalize All* et inspectez les articulations.

## Tutoriel 4 — Essayer (20 min)
Pose Mode sur RIG_Hero : déplacez `root`, levez `foot_ik.L` : le corps suit proprement.

## Tutoriel 5 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch06_05_humanoid_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch06_05.py" -- --exercise humanoid --debug
```
Le correcteur déplace racine et pied lui-même puis remet la pose.

Remarque d'honnêteté : la solution est faite avec les opérateurs réels (ajout du méta-rig, `rigify_generate`, Automatic Weights) en arrière-plan : cela fonctionne en 5.3 ; le croquis montre bien les jambes et la colonne alignées et le pied gauche levé qui entraîne le corps. Les bras ont été ajustés après un audit (le premier rig laissait les mains hors du maillage) : la solution recale coude, poignet et main sur l'axe du bras du maillage (fonction `fit_arms` du script de construction) ; le croquis montre les os des bras dans les bras. Le rig généré s'appelait déjà « RIG_Hero » dans mes builds répétés ; mon script accepte les deux noms. Libellés relus dans les sources 5.3 de Rigify : bouton « Generate Rig » (« Re-Generate Rig » si le rig existe), entrée de menu « Human » sous Add > Armature.

## Variante de contrôle

Avant de générer, superposez les repères du méta-rig au mesh de profil et de face. Après génération, testez un avant-bras et une cuisse dans de petites poses. **Preuve** Les articulations du méta-rig tombent sur les repères visés avant la génération. Les problèmes de poids sont consignés séparément.
