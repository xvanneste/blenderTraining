# CH06.01 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch06_01_armature_starter.blend` : le mannequin `REF_Body` (filaire, non sélectionnable) et une armature « Armature » sale (sept bones « Bone.00x », un seul côté, hanche décalée). Sauvegardez sous `ch06_01_armature_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Nettoyer (15 min)
Renommez l'objet RIG_Hero et ses données ARM_Hero. Object > Apply > All Transforms. Supprimez ou réutilisez les bones sales.

## Tutoriel 2 — L'axe (40 min)
Edit Mode : root (0,0,0 → 0,0,2 de longueur), pelvis, spine.001–003, neck, head aux hauteurs de THEORY.md §6, chaque bone parenté au précédent et **Connected** (sauf root et pelvis).

## Tutoriel 3 — Le côté gauche (60 min)
shoulder.L (parent spine.003, non connecté), upper_arm.L, forearm.L, hand.L (connectés, bras à 40° de la verticale) ; thigh.L (parent pelvis, non connecté), shin.L, foot.L, toe.L.

## Tutoriel 4 — Le côté droit (10 min)
Sélectionnez les bones .L ; Armature > Symmetrize. Vérifiez les suffixes `.R` et la position des articulations en vue de face. Le corps reste orienté selon la convention de repère du starter. Déplacez un coude en mode Édition sur une copie et contrôlez que la tête de l’os suivant suit lorsque la liaison est *Connected*.

## Tutoriel 5 — Déformation, pose (15 min)
Bone Properties : Deform désactivé pour root. Pose Mode : tout sélectionner, Pose > Clear Transform > All.

## Tutoriel 6 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch06_01_armature_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch06_01.py" -- --exercise armature --debug
```
Référence : `ch06_01_armature_reference.png` (croquis de face et de profil).

Remarque d'honnêteté : la solution est générée par script (bones créés par `edit_bones.new`) ; elle est comparée au mannequin par un croquis (les bones ne se rendent pas en EEVEE, j'ai dessiné leur projection avec numpy) : le squelette suit bien le corps. Deux erreurs de ma part ont été révélées par les contre-épreuves : un test de connexion qui lisait le mauvais nom de bone (spine.001 devenait « spine ») et un contre-exemple « asymétrique » qui passait parce qu'un bone connecté était remis en place par sa connexion. Les raccourcis et chemins de menu (Symmetrize, Clear Transform) n'ont pas été relus dans l'interface 5.3.

## Variante de contrôle

Affichez les axes locaux et vérifiez la symétrie des deux côtés avant pondération. Testez une petite rotation de pose sur un seul os. **Preuve** L’axe utilisé est identifié et le pivot de l’articulation se trouve au bon endroit lorsque le membre pivote.
