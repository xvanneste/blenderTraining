# CH11.04 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — La distance de chaque pixel à la caméra | Prise « Depth » de Render Layers (passe Z). |
| Q2 | **a** — Sur la caméra : Depth of Field > Focus Distance | Mesuré : mise au point à 5 m : Far 0,30 ; à 30 m : Far 0,92. |
| Q3 | **a** — La quantité de flou (petit = plus de flou) | Propriété `f_stop` du nœud (1,0 dans la solution). |
| Q4 | — | Pour que le flou dépende de la passe Depth reliée à la prise Z ; sans elle on utilise un flou constant. |
| Q5 | — | Le rendu doit rester net : la profondeur de champ est faite en post ; la caméra ne fournit que la distance de mise au point. |
| Q6 | **a** — Le déplacement de chaque pixel entre deux images | Prise « Vector » ; activer View Layer > Passes > Data > Vector. |
| Q7 | **a** — La durée d'obturation : plus grande, plus d'étalement | Mover : 12 px sans flou, 27 px à Shutter 1,0 ; Shutter 0,1 donne 12 px. |
| Q8 | — | Il l'utilise pour que les objets lointains ne bavent pas sur les objets proches ; la prise Depth est un des entrées du nœud. |
| Q9 | — | Pour doser le flou en post et ne pas le compter deux fois. |
| Q10 | — | Ils manquent d'information cachée (ce qui est derrière un objet) : bords de profondeur de champ moins fidèles qu'au rendu ; la mesure ne juge que des barres fines. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch11_04_depth_fx_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch11_04_files.py`) : trois barres émissives, arbre Defocus / Vector Blur ; mesures par rendu de l'image 10. Score 39/39 ; starter 23/39. Rendus regardés.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_no_defocus` | sans Defocus : Far nette (0,92) | Far floue |
| `…_wrong_focus` | mise au point à 30 m : Far nette (0,92) | Far floue |
| `…_no_vector_blur` | sans Vector Blur : Mover de 10 pixels | Mover étalée |
| `…_weak_shutter` | Shutter 0,1 : Mover de 12 pixels | Mover étalée |
Aussi refusé : le starter.

## Limites
- Barres fines, fond noir.
- Pas de bokeh coloré.
- Création de nœuds par l'interface non vérifiée.
