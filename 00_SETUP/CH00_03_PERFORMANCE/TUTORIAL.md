# CH00.03 — Tutoriels pas à pas

## Tutoriel 1 — Lire le coût d'une scène
1. Ouvrez `STARTER_FILES/ch00_03_heavy_scene_starter.blend`.
2. Barre d'état : notez *Objects*, *Faces*, *Memory*, *VRAM* (activez-les en CH00.02 si besoin).
3. Vue 3D → menu **Overlays** (icône deux cercles en haut à droite) → cochez
   **Statistics** : les mêmes chiffres apparaissent en haut à gauche de la vue.
4. Workspace **Scripting** → *Text → Open* → `SCRIPTS/bcma_scene_cost.py` → **Run Script**
   (`Alt+P`). Ouvrez la console (*Window → Toggle System Console*).
   Le starter compte 202 maillages distincts et 16 384 002 faces estimées. Les statistiques de la vue et l’estimation du rendu décrivent deux états différents. Notez les deux colonnes avant d’optimiser.

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
5. Relancez l’estimateur. Le nombre de maillages distincts descend à 3 si les 200 galets partagent un maillage. L’estimation des faces reste à 16 384 002. Conservez la scène sous une nouvelle version. Après sauvegarde et réouverture, l’Outliner en mode Orphan Data permet d’inspecter les données non utilisées.

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

## Tutoriel 5 — Comparer les temps et la qualité

1. Enregistrez sur deux copies les mêmes réglages Cycles, 32 échantillons et 50 % de résolution. Utilisez le même périphérique sur les deux versions. Restez en CPU si c’est votre configuration. Conservez la caméra, la transformation de vue et la même image.
2. Rendez d’abord la scène optimisée. Si le coût du starter complet dépasse votre budget, réglez un plafond Render Simplify commun aux deux versions et indiquez-le dans vos notes. Le nombre de faces estimées du starter conserve une indication du coût sans imposer le rendu le plus lourd.
3. Au second essai de chaque version, notez le temps du rendu et la mémoire quand Blender l’affiche. Reprenez les images au même grossissement. Comparez bord des galets, ombres et reflets sous un éclairage identique.
4. Décidez quel gain est utile. Un résultat plus rapide doit préserver les informations visibles voulues dans le plan. En cas de différence, haussez un seul niveau et documentez le seuil acceptable.

**À refaire sans aide** Sur une copie de la scène optimisée, faites passer un galet à Render Levels 5. Prédisez l’estimation et observez si Simplify plafonne son niveau au rendu.

## Tutoriel 6 — Changer de backend (seulement en cas de problème)
1. *Preferences → System → Display Graphics → Backend* : notez la valeur (Vulkan).
2. Pour **tester** OpenGL sans changer vos préférences : fermez Blender, lancez
   `blender_startup_opengl.cmd` dans `C:\Program Files\Blender Foundation\Blender 5.3\`.
3. Si un problème d'affichage disparaît en OpenGL, choisissez-le dans les préférences et
   redémarrez. Sinon, restez en Vulkan.
