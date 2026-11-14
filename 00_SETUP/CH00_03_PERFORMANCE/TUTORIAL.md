# CH00.03 — Tutoriels pas à pas

## Tutoriel 1 — Lire le coût d'une scène
1. Ouvrez `STARTER_FILES/ch00_03_heavy_scene_starter.blend`.
2. Barre d'état : notez *Objects*, *Faces*, *Memory*, *VRAM* (activez-les en CH00.02 si besoin).
3. Vue 3D → menu **Overlays** (icône deux cercles en haut à droite) → cochez
   **Statistics** : les mêmes chiffres apparaissent en haut à gauche de la vue.
4. Workspace **Scripting** → *Text → Open* → `SCRIPTS/bcma_scene_cost.py` → **Run Script**
   (`Alt+P`). Ouvrez la console (*Window → Toggle System Console*).
   ✅ Vous lisez `Maillages distincts : 202` et `Faces estimées au rendu : 16 384 002`.
   Comparez au nombre de faces de la barre d'état : c'est l'écart viewport / rendu.

## Tutoriel 2 — Partager les données (duplication liée)
1. Cliquez un galet : panneau *Object Data* (triangle vert) → le nom du maillage en haut
   (`GEO_Pebble_000`, `GEO_Pebble_000.001`…) : chaque galet a **sa propre copie**.
2. Sélectionnez tous les galets : dans l'Outliner, clic droit sur la collection `PROPS`
   → **Select Objects**.
3. Rendez actif le galet de référence : `Ctrl`+clic sur `GEO_Pebble_000` dans l'Outliner
   (il devient l'objet **actif**, surligné plus clair).
4. Vue 3D : **Object → Link/Transfer Data → Link Object Data** (`Ctrl+L`).
   ✅ Le nom du maillage de n'importe quel galet est `GEO_Pebble_000` avec un nombre
   d'utilisateurs **200** à côté du nom.
5. Les anciens maillages, désormais sans utilisateur, seront purgés à l'enregistrement
   (ou *File → Clean Up → Purge Unused Data*).

## Tutoriel 3 — Réduire la subdivision… sur 200 objets d'un coup
1. Galets toujours sélectionnés, galet actif = `GEO_Pebble_000`.
2. Panneau *Modifiers* (clé à molette bleue) → modificateur **Subdivision** :
   **Levels Viewport = 1**, **Render = 2**.
3. Pour appliquer à toute la sélection : clic droit sur le champ *Render* → **Copy to
   Selected**. Faites de même pour *Levels Viewport*.
   (Alternative : maintenir `Alt` en modifiant la valeur l'applique à tous les objets
   sélectionnés.)
4. Relancez `bcma_scene_cost.py`.
   ✅ `Faces estimées au rendu : 256 002`.

## Tutoriel 4 — Simplify, le garde-fou global
1. *Properties → Render* → panneau **Simplify** : cochez la case du titre.
2. Sous-panneau *Viewport* : **Max Subdivision = 1** ; sous-panneau *Render* :
   **Max Subdivision = 2**.
3. Testez : remettez un galet à Render = 5 → l'estimation ne bouge pas : Simplify plafonne.
   ✅ Simplify agit sur toute la scène sans modifier les objets : idéal pour une
   prévisualisation rapide, ou comme filet de sécurité avant un rendu de nuit.

## Tutoriel 5 — Comparer les temps de rendu
1. *Render → Device : GPU Compute*, *Sampling → Render → Max Samples = 32*,
   *Output → Resolution % = 50*.
2. `F12` sur la scène lourde (avant optimisation : rouvrez le starter) : notez le temps
   (en haut de la fenêtre de rendu, *Time*) et la mémoire (*Mem*, *Peak*).
3. Même chose sur votre version optimisée.
   ✅ Temps et pic mémoire plus bas, image identique à l'œil.

## Tutoriel 6 — Changer de backend (seulement en cas de problème)
1. *Preferences → System → Display Graphics → Backend* : notez la valeur (Vulkan).
2. Pour **tester** OpenGL sans changer vos préférences : fermez Blender, lancez
   `blender_startup_opengl.cmd` dans `C:\Program Files\Blender Foundation\Blender 5.3\`.
3. Si un problème d'affichage disparaît en OpenGL, choisissez-le dans les préférences et
   redémarrez. Sinon, restez en Vulkan.
