# CH01.12 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch01_12_portrait_starter.blend`.

## Tutoriel 1 — Activer et regarder par la caméra
1. Outliner → `CAMERAS` → `CAM_Shot`, souris dans la vue, `Ctrl+Numpad 0` : vue caméra.
2. *Object Data* (caméra verte) → *Viewport Display* → *Composition Guides* → **Thirds** ;
   *Passepartout* à 0,8.

## Tutoriel 2 — Choisir la focale
1. *Lens → Focal Length* : essayez 24, 50, 85, 135 en restant en vue caméra.
   Observez la taille du gardien et la taille apparente du phare.
2. Réglez **50 mm**.

## Tutoriel 3 — Placer la caméra à hauteur d'œil
1. Quittez la vue caméra avec `Numpad 0`. Placez-vous en vue de dessus (`Numpad 7`).
2. Sélectionnez `CAM_Shot`, `N` → *Item* : *Location* = (0,55 ; −4,2 ; 1,6) (≈ 4 m devant le
   gardien, légèrement à sa droite, à 1,60 m).
3. *Rotation* : X = 90°, Y = 0, Z = 0 pour commencer (regarde vers +Y).

## Tutoriel 4 — Composer avec les tiers
1. `Numpad 0`. Sidebar `N` → onglet *View* → cochez **Lock Camera to View**.
2. Orbitez/glissez légèrement (`Shift+MMB`) jusqu'à placer la **tête** du gardien sur
   l'intersection du **tiers supérieur gauche** (ou droit), avec le phare visible dans la
   partie opposée.
3. **Décochez Lock Camera to View**.
   ✅ Les yeux sont sur la ligne haute des tiers ; espace libre du côté du phare.

## Tutoriel 5 — Profondeur de champ
1. *Object Data → Depth of Field* : cochez la case du panneau.
2. *Focus on Object* → `EMP_Head`.
3. *Aperture → F-Stop* = **2.8**.
4. Dans *Rendered*, comparez f/2,8 et f/16 avec le même point de mise au point. À f/16,
   la zone de netteté s’étend. Lisez le bord du phare pour comparer les deux images.
   Remettez f/2,8 et vérifiez que la tête du gardien reste nette.

## Tutoriel 6 — Vérifier
Enregistrez `ch01_12_portrait_<prenom>_v001.blend` puis :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch01_12_portrait_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch01_12.py" -- --exercise portrait --render
```
[Image de référence du portrait](COMPLETED_EXAMPLES/ch01_12_portrait_reference.png)

## Contrôle de transfert

Gardez la caméra à la même position et comparez 24 mm et 50 mm. Ensuite cadrez le personnage à une taille proche en déplaçant la caméra, puis comparez sa relation au phare. Une focale change le cadre depuis la position donnée. Un déplacement de caméra change les rapports de perspective. Désactivez **Lock Camera to View** avant de revenir à la navigation libre. **Réussite** Trois cadres portant position, focale et effet observé.
