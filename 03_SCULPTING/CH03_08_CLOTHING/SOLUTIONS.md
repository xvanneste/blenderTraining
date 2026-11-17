# CH03.08 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — Un objet masqué dans la vue (hide_viewport) n'est pas évalué : le tissu le traverse | Mesuré dans ce chapitre : avec le collider masqué, le tissu est tombé à travers le corps jusqu'au sol. Utilisez l'affichage Wire. |
| Q2 | — | La collision coûte cher : 74 000 faces ralentiraient la simulation ; un collider à ≈ 10 000 faces suffit (ici 8 % de faces) et se règle avec une distance de collision de quelques mm. |
| Q3 | — | Les quads réguliers donnent des plis plus propres et une simulation stable ; la maille fixe aussi la finesse des plis (ici 1,6 cm). |
| Q4 | **a** — Properties > Physics > Cloth (Physical Properties, Stiffness, Damping) | Libellés vérifiés : Quality Steps, Vertex Mass, Air Viscosity, Stiffness (Tension, Compression, Shear, Bending), Damping. |
| Q5 | — | Faible : plis nombreux et petits, tissu souple. Forte : plis larges et rares, tissu raide. Ici 0,4 ; à 0,08 l'ourlet se froisse davantage. |
| Q6 | **b** — Elles faisaient vibrer le tissu (aspect dentelé) sans gain visible | Réglage constaté sur ce cas ; à réactiver pour des vêtements qui se plient sur eux-mêmes (manches). |
| Q7 | — | La simulation n'est évaluée que dans le cache : le tissu devient un maillage figé, réutilisable (rendu, retopologie, export) ; sans application, le fichier relu en arrière-plan ne contient pas la simulation. |
| Q8 | — | Pénétration du corps (sommets sous la surface), étirement (arêtes plus longues que le repos), plis trop lisses ou ourlet dentelé (rugosité), tissu qui ne couvre pas (couverture des épaules). |
| Q9 | **a** — Pinch Folds Cloth, Drag Cloth, Grab Cloth, Push Cloth, Inflate Cloth… | Ces brosses « Cloth » existent dans les brosses essentielles 5.3 (noms vérifiés) ; elles n'ont pas été essayées dans ce chapitre. |
| Q10 | — | Plus de qualité de collision, plus de matière ou un tissu plus court, une flexion plus forte, ou refaire le bas à la main ; pour de la production, un maillage dédié (retopologie, CH03.09) plutôt qu'une grille brute. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`COMPLETED_EXAMPLES/ch03_08_poncho_solution.blend` (+ `_reference.png` : face, 3/4, profil).

**Honnêteté sur la fabrication.** La solution est **générée et simulée par script** (`build_ch03_08_files.py`, ≈ 20 s par simulation de
120 images) : réglages du tableau de THEORY.md §3, simulation, puis modificateur Cloth appliqué. Retouche à la brosse réalisée ensuite dans Blender 5.2 via MCP (*Smooth* sur l'ourlet : 207 sommets déplacés, jusqu'à 10 mm ; *Crease Sharp* pour deux plis) ; les brosses *Cloth* n'ont pas été essayées. **Défaut visible** : les quatre coins du tissu restent légèrement froissés ; la simulation sur une
grille brute ne donne pas un résultat de production (voir THEORY.md §5).

Mesures du correcteur sur la solution : 1 112 sommets ; 0 % de sommets dans le corps ; arête moyenne 16,4 mm (repos 16,4 mm, plus longue
16,9 mm) ; z minimal 22 mm (au-dessus du sol) ; épaules couvertes à 94 % ; rugosité (90ᵉ centile) 10,6 mm. Score 17/17.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Test qui le refuse |
|---|---|---|
| `…_penetrating` | tissu repoussé de 1,5 cm dans le corps | pénétration (80,4 %), couverture, étirement local |
| `…_smoothed` | plis effacés (60 lissages) | plis (rugosité 0,93 mm) — et lui seul |
| `…_stretched` | tissu mis à l'échelle ×1,6 | étirement (23,9 mm), couverture |
| `…_tiny` | tissu de 28 cm de côté (réf. 54 cm) | couverture (60 %), nombre de sommets |
Aussi refusé : le starter (tissu plat : pas de couverture, pas de plis).

**Ce que le développement a appris** (consigné aussi dans CLAUDE.md) :
1. un collider mis en `hide_viewport` n'est PAS évalué : le tissu l'a traversé jusqu'au sol (vu sur le rendu) ; l'afficher en Wire ;
2. avec l'auto-collision, le tissu vibrait et l'ourlet devenait dentelé ; désactivée + amortissements + qualité de collision 5 ;
3. une première mesure de plis (lobes du rayon maximal autour du corps) ne séparait PAS le tissu lissé de la solution (4–5 lobes dans les
   deux cas) : remplacée par la rugosité locale (écart d'un sommet à la moyenne de ses voisins), 12× plus forte dans la solution ;
4. un tissu trop grand (50 cm de demi-côté) s'étale en nappe sur le sol ; 27 cm tombe sur les épaules et reste au-dessus du sol.

## Limites
- Le correcteur juge des mesures géométriques ; il ne juge ni la beauté des plis ni le réalisme du tissu.
- La « rugosité » mesure aussi les dentelures : un tissu dentelé et un tissu plissé se ressemblent pour lui ; le rendu départage.
- Il attend le tissu nommé `CLOTH_Poncho` et le corps `SCULPT_Bust`.
