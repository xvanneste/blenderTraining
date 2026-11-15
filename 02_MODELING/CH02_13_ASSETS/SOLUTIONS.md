# CH02.13 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | — | Une donnée (objet, matériau, collection, node group…) marquée pour être retrouvée dans l'Asset Browser et réutilisée dans d'autres scènes. |
| Q2 | **a** — Object → Asset | Object → Asset → Mark as Asset, ou clic droit dans l'Outliner. |
| Q3 | — | Dans le fichier blender_assets.cats.txt situé à côté du .blend (dans le dossier de la bibliothèque). |
| Q4 | — | Description, auteur, licence (et copyright), tags, catalogue, aperçu. |
| Q5 | **b** — Icône ⟳ sous l'aperçu dans le panneau N de l'Asset Browser (Generate Preview) | Generate Preview. |
| Q6 | — | Edit → Preferences → Asset Libraries → + et choisir le dossier contenant les .blend de bibliothèque. |
| Q7 | **b** — Link | Link : une correction de la source se propage. |
| Q8 | — | Pour copier un asset sans dupliquer les données déjà présentes (matériaux, textures). |
| Q9 | — | Il appartient au fichier source (une seule source de vérité) ; on modifie la source, ou on crée une Library Override. |
| Q10 | — | Nom clair, origine au sol, échelle 1 et transformations appliquées, topologie et UV validées, métadonnées complètes. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
Le tabouret **lié** reflète la modification de la bibliothèque à la réouverture ; la caisse **ajoutée**
(Append) est une copie indépendante, inchangée. Un objet lié n'est pas modifiable localement : c'est
voulu (une seule source de vérité) ; pour l'animer ou l'ajuster, on crée une *Library Override*.

## Exercice 3
Référence : `COMPLETED_EXAMPLES/ch02_13_library_solution.blend` + `blender_assets.cats.txt`
(catalogues *Props/Mobilier*, *Props/Accessoires*, *Props/Nature*), rendu
`ch02_13_library_reference.png`. Les 6 props sont repris (append) des solutions de CH02.02, 02.03,
02.05, 02.08 et 02.11 ; chacun a une description, l'auteur « Blender Cinema Master Academy », une
licence, 2 à 3 tags et un aperçu généré. Le correcteur lit le fichier de catalogues situé à côté du
`.blend`.
