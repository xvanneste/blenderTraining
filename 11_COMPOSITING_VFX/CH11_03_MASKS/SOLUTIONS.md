# CH11.03 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Un entier propre à l'objet, écrit dans la passe Object Index | Object Properties > Relations > Pass Index : A = 1, B = 2, C = 3. |
| Q2 | **a** — Un masque (alpha) des pixels dont l'index vaut la valeur choisie | Entrées : ID value (la prise Object Index), Index, Anti-Alias. |
| Q3 | **a** — Object Index | Constaté : les prises dépendent des passes activées ; Cycles seulement. |
| Q4 | — | L'index d'objet est une passe Cycles : avec un autre moteur la prise n'est pas créée (constaté). |
| Q5 | — | Index 1 : c'est la sphère rouge qui reste en couleur : le masque suit l'index, pas la position. |
| Q6 | **a** — On choisit par nom, et les bords sont anti-aliasés (transparence, flou de mouvement) | Variante vérifiée : matte_id « Sphere_B », prise Matte. |
| Q7 | **a** — Prend B là où le masque vaut 1 et A là où il vaut 0 | A = image désaturée, B = image d'origine. |
| Q8 | — | La saturation HSV d'un patch donne un nombre contrôlable : 0,59 en couleur, 0,00 en gris. |
| Q9 | — | Le masque inversé donne l'effet inverse : B grise, A et C en couleur : il faut vérifier le sens du masque. |
| Q10 | — | Trois sphères nettes, pas de transparence ni de mouvement : le bord anti-aliasé de Cryptomatte n'est pas mesuré. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch11_03_masks_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch11_03_files.py`) : trois sphères avec index, arbre de masquage ; mesures par rendu. Score 41/41 ; starter 27/41. Rendus regardés.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_wrong_index` | masque de l'index 1 : la sphère rouge reste en couleur | sphère B ; sphères A et C |
| `…_all_gray` | pas de masque : tout désaturé | nœud de masque ; sphère B |
| `…_inverted` | masque inversé : B grise, A et C en couleur | sphère B ; sphères A et C |
| `…_no_mask_node` | aucun nœud de masque | nœud de masque ; sphères A et C |
Aussi refusé : le starter.

## Limites
- Bords nets seulement.
- Création de nœuds par l'interface non vérifiée.
- Transparence non mesurée.
