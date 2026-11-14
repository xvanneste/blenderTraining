# CH01.08 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — M | M (Shift+M : lier à une collection supplémentaire). |
| Q2 | — | Oui (Shift+M ou Ctrl+glisser dans l'Outliner), à utiliser avec parcimonie. |
| Q3 | — | Ils échappent à l'organisation : impossible de les masquer, exclure ou lier par groupe ; les outils de pipeline s'appuient sur les collections. |
| Q4 | **b** — L'appareil photo | Disable in Renders. |
| Q5 | — | Non : il masque seulement dans le viewport (temporaire, par view layer). |
| Q6 | — | Rendre un objet/une collection non sélectionnable (visible mais protégé des clics). |
| Q7 | — | Filtre (entonnoir) de l'Outliner > Restriction Toggles. |
| Q8 | **b** — A puis B (B actif), Ctrl+P | Le parent est l'objet actif (sélectionné en dernier). |
| Q9 | — | La collection organise (dossier) ; le parentage crée une relation de mouvement (l'enfant suit le parent). |
| Q10 | — | Unused Data (appelé Orphan Data dans d'anciennes versions). |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
- Canapé visible mais absent du rendu → icône **appareil photo** (*Disable in Renders*) de
  l'objet ou de sa collection.
- Table invisible dans la vue mais rendue → **œil** (*Hide in Viewport*, `H`) — temporaire,
  sans effet au rendu. (`Alt+H` révèle tout.)
- Vase non sélectionnable → **flèche** (*Disable Selection*).

## Exercice 3
Fichier : `COMPLETED_EXAMPLES/ch01_08_living_room_solution.blend`.
| Collection | Objets |
|---|---|
| SET | GEO_Floor, GEO_Wall_Back, GEO_Wall_Left |
| PROPS | GEO_Sofa, GEO_Table, GEO_Vase, GEO_Rug, GEO_LampBase, GEO_LampShade, GEO_Shelf |
| LIGHTS | LGT_Key, LGT_Window |
| CAMERAS | CAM_Main, EMP_CamTarget |
| HELPERS (📷 désactivé) | EMP_Guide_1..3, GEO_Debug_Box |
Parent : GEO_LampShade → GEO_LampBase (`Ctrl+P` → *Object*).
