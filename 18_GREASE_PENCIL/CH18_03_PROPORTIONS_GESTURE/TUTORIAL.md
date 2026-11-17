# CH18.03 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch18_03_gesture_starter.blend`, sélectionnez `GP_Practice`,
`Ctrl+Tab` → Draw Mode, `Num 0`. Le calque GUIDE (verrouillé) montre l'échelle en têtes, un
mannequin de face et quatre lignes d'action types.

## Tutoriel 1 — Construire un mannequin debout (USER_Mannequins)
1. Calque **USER_Mannequins** (`Y`).
2. En vous aidant de l'échelle graduée : marquez légèrement le sommet (7,5 têtes) et le sol.
3. Tracez la **ligne d'action** (droite pour une pose debout neutre).
4. Tête (ovale, 1 tête de haut), cage thoracique (ovale, de 6,4 à 4,4 têtes), bassin (ovale
   aplati vers 3,8 têtes).
5. Épaules (un trait de 2 têtes de large), puis bras en 2 segments jusqu'à mi-cuisse ; jambes en
   2 segments, genoux à 2 têtes. Petits cercles aux articulations.
   ✅ Comparez avec le mannequin du GUIDE.

## Tutoriel 2 — Huit poses
1. Pour chaque pose (debout, marche, course, saut, assis, accroupi, porter, montrer du doigt) :
   **ligne d'action d'abord** (C, S, inversée…), puis tête, cage, bassin, puis membres.
2. Vérifiez la **longueur des membres** : un bras plié reste aussi long qu'un bras tendu.
3. Vérifiez l'**équilibre** : verticale depuis le cou → pied d'appui.
4. Contrapposto pour la pose debout détendue : hanche haute côté jambe d'appui, épaule basse
   du même côté.

## Tutoriel 3 — Croquis gestuels chronométrés (USER_Gesture)
1. Calque **USER_Gesture**. Ouvrez une série de photos de poses (sport, danse) dans votre
   navigateur ou en image de référence (CH18.09).
2. Chronomètre 30 s par croquis : ligne d'action → ovale tête → ovale cage → ovale bassin →
   2–4 traits de membres. Arrêtez-vous à la sonnerie, même inachevé.
3. Enchaînez 20 croquis sans vous corriger.

## Tutoriel 4 — Silhouettes (USER_Silhouettes)
1. Calque **USER_Silhouettes**, `U` → **MAT_GP_Black** (remplissage noir).
2. Dessinez le contour fermé d'un personnage en pose, ou utilisez l'outil **Fill** à l'intérieur
   d'un contour fermé.
3. Variante rapide : une très grosse brosse noire (`F` pour agrandir) et dessinez la pose
   directement en « feutre » épais.
4. Test : la pose se comprend-elle sans détail ? Sinon, écartez les membres.

## Tutoriel 5 — Vérifier
Enregistrez `ch18_03_gesture_<prenom>_v001.blend` (Object Mode), puis :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_03_gesture_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch18_03.py" -- --exercise gesture --render
```
Référence : `COMPLETED_EXAMPLES/ch18_03_gesture_reference.png`.

## Variante de contrôle

Simplifiez la silhouette du mannequin à des masses et des axes. Tirez une autre pose avec le même personnage en changeant l’appui. **Preuve** La silhouette identifie la pose et l’appui sans détails de vêtement ou de visage.
