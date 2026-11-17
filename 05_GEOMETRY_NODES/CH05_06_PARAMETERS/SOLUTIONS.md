# CH05.06 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — Dans le modificateur, sous le sélecteur de l'arbre | Chaque entrée de l'interface devient un champ du modificateur Nodes. |
| Q2 | **a** — Défaut, minimum, maximum, description | Ces réglages se règlent dans l'interface de l'arbre : ils bornent la valeur et documentent l'entrée (infobulle). |
| Q3 | **a** — À regrouper des entrées sous un titre repliable | Les panneaux (« Dimensions », « Layout ») rendent un outil de dizaines d'entrées lisible. |
| Q4 | — | Elle devient l'infobulle de l'outil : l'utilisateur (ou vous dans six mois) comprend l'unité et l'effet sans ouvrir l'arbre. |
| Q5 | — | Pour empêcher une valeur absurde (100 000 piliers) qui bloquerait Blender ; une borne est une protection autant qu'une indication. |
| Q6 | **b** — Non : Depth ET la translation z (Height ÷ 2), sinon les piliers flottent ou s'enfoncent | Le Cylinder est centré : pour poser sa base sur le sol il faut le monter de Height ÷ 2. |
| Q7 | **b** — Il change sa valeur dans le modificateur et mesure la géométrie évaluée | Une entrée non branchée, ou une valeur codée en dur, laisse la géométrie inchangée : le test échoue. |
| Q8 | — | L'entrée Height existe mais le nœud garde 2,0 en dur : changer Height à 3,5 laisse la hauteur à 2,0 m, ce que seul un test de comportement détecte. |
| Q9 | — | Avec `modifier.properties.inputs[identifiant]["value"] = valeur` (l'ancienne écriture `modifier[identifiant]` n'est plus disponible). |
| Q10 | — | 8 piliers espacés de 1,2 m : 7 intervalles × 1,2 = 8,4 m entre le premier et le dernier. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`COMPLETED_EXAMPLES/ch05_06_parameters_solution.blend` (+ `_reference.png`).

**Fabrication.** Générée par script (`build_ch05_06_files.py`) : interface créée par `node_group.interface` (4 entrées, 2 panneaux, descriptions, bornes). Score du correcteur 35/35 ; starter 9/35.
Mesures : réglage par défaut 8 piliers, 2,00 m, étendue 8,40 m ; réglage B 12 piliers, 3,50 m, largeur 0,60 m, étendue 11,00 m.
Rendu regardé : deux réglages (haut : défaut ; bas : réglage B) ; le cadrage a été élargi pour que les 12 piliers entrent.
**Ce que le développement a appris** : `modifier["Socket_n"]` n'existe plus en 5.3 (TypeError) ; la valeur s'écrit `modifier.properties.inputs[identifiant]["value"]` (le premier essai d'affectation directe d'un flottant échouait aussi : « Cannot assign a 'float' value to the existing Group IDProperty »).

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_no_panels` | entrées à plat, sans panneaux | Panneaux (seul) |
| `…_no_description` | descriptions vides | Descriptions (seul) |
| `…_unused_input` | Spacing exposé mais non branché | Entrée inutilisée ; étendue du réglage B (13,2 m au lieu de 11,0) |
| `…_hardcoded` | Height exposé mais codé en dur dans les nœuds | Entrée inutilisée ; hauteur du réglage B (2,00 m au lieu de 3,50 m) |
| `…_bad_range` | bornes Count 1–100 000 et Height min −5 | Bornes (seul) |
Aussi refusé : le starter (sans interface).

## Limites
- L'outil et ses quatre paramètres sont fixés par le correcteur ; il ne généralise pas à n'importe quelle interface.
- Les menus et les entrées de type Objet/Collection ne sont pas testés ici.
