# Fiche de révision — CH00.03 Performances

- **Budget** : temps de rendu/image, VRAM, RAM, triangles, Go de textures.
- **CPU** : modificateurs, animation, simulations, Cycles CPU. **GPU** : affichage, EEVEE, Cycles GPU.
- **VRAM** : la scène entière doit y tenir pour Cycles GPU.
- **Backend** (affichage) : Vulkan par défaut en 5.3 · `blender_startup_opengl.cmd` pour tester OpenGL.
- **Subdivision** : faces × 4^niveau. Niveau 5 = ×1 024.
- **Statistiques** = viewport ; coût rendu → `bcma_scene_cost.py`.

| Action | Raccourci / menu |
|---|---|
| Partager les données | `Ctrl+L` → Link Object Data (actif = référence) |
| Duplication liée | `Alt+D` |
| Copie indépendante | `Shift+D` |
| Appliquer une valeur à la sélection | clic droit → Copy to Selected (ou `Alt` + modification) |
| Plafond global | Render → Simplify → Max Subdivision |
| Statistiques dans la vue | Overlays → Statistics |
| Purger les données orphelines | File → Clean Up → Purge Unused Data |
| Détacher une donnée partagée | Object Data → nombre d'utilisateurs → Make Single User |
