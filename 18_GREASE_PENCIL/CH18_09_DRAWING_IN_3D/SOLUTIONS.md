# CH18.09 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | — | Stroke Placement choisit le point de référence ou la surface de projection (Origin, 3D Cursor, Surface, Stroke) ; Drawing Plane choisit l'orientation du plan qui passe par ce point (View, Front, Side, Top, Cursor). |
| Q2 | **b** — Drawing Plane Top (X-Y), curseur à Z = 0 | Top (X-Y) est le plan horizontal ; le curseur fixe sa hauteur. |
| Q3 | — | Barre latérale N → onglet View → 3D Cursor → Location Y = 14 (Shift+clic droit pour un placement à la souris). |
| Q4 | — | Elle affiche le plan de dessin actif pour vérifier qu'on dessine bien à plat ou de face (Viewport Overlays → Canvas → Use Grid). |
| Q5 | — | Parce que la perspective de la caméra réduit les éléments lointains : un trait petit à 25 m paraît minuscule à l'écran. |
| Q6 | **b** — Une vraie parallaxe quand la caméra bouge | Les éléments proches défilent plus vite que les lointains. |
| Q7 | — | Poser la caméra, puis un calque par plan (sol, fond, plan moyen, premier plan) en plaçant le curseur à la bonne distance, en dessinant en vue caméra et en vérifiant en orbitant. |
| Q8 | — | Add → Image → Reference ; puis File → External Data → Pack Resources (ou garder un chemin relatif valide). |
| Q9 | **a** — Render → Simplify → Grease Pencil | Simplify → Grease Pencil : Playback Only, Fill, Modifiers, Shader Effects… |
| Q10 | — | Quand on veut des couleurs plates fidèles au dessin, non assombries ou modifiées par les lampes de la scène. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
Quand la caméra se déplace latéralement, un objet proche change beaucoup de position à l'écran,
un objet lointain très peu : c'est la parallaxe. Un dessin plat est à une seule distance, tous ses
éléments se déplacent ensemble : aucune sensation de profondeur.

## Exercice 3
Référence : `COMPLETED_EXAMPLES/ch18_09_set_solution.blend`, rendus `ch18_09_set_reference.png`
(caméra) et `ch18_09_set_top.png` (vue de dessus orthographique) :
- **BG** : 4 montagnes remplies à Y ≈ 14–15 ; **MID** : maison, 2 arbres (Y ≈ 3–4), personnage
  (Y = 2) ; **FG** : grand arbre coupé par le bord gauche, 3 buissons (Y = −5) ;
- **GROUND** : route remplie de Y = −9 à Y = +13 à Z = 0,02, tirets, touffes d'herbe ;
- calques avec *Lights* décoché, passe Z activée.
Distances moyennes mesurées par le correcteur sur la solution : FG ≈ 8,2 m, MID ≈ 14,6 m,
BG ≈ 28,8 m de la caméra.
