# CH05.05 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — L'élément qui porte la valeur : point, arête, face, coin… | Un attribut de domaine Point a une valeur par sommet ; de domaine Face, une par face. |
| Q2 | **b** — Store Named Attribute | Store Named Attribute écrit un champ dans un attribut nommé, de type et de domaine choisis. |
| Q3 | **b** — Float | Une grandeur continue : Float. |
| Q4 | — | Position.z lue avant le déplacement vaudrait 0 partout ; après, elle contient le relief : l'attribut vaut la coordonnée z des sommets. |
| Q5 | — | Dans le Spreadsheet : colonne portant son nom pour le domaine concerné (Vertex, Face…). |
| Q6 | **b** — Attribute (type Geometry) | Le nœud Attribute, Type Geometry, Name = nom de l'attribut. |
| Q7 | **b** — Le shader ne trouve pas l'attribut : valeur 0, couleur uniforme | Le correcteur exige le même nom ; sinon le shader lit zéro. |
| Q8 | — | La hauteur varie de −0,6 à +0,6 : Map Range la ramène à 0–1 (−0,5 → 0 ; 0,5 → 1) pour que la rampe en tire parti. |
| Q9 | — | Une valeur par face (le champ est évalué sur le domaine cible) : l'attribut n'est plus un attribut de point, le shader lit des facettes et le correcteur le refuse. |
| Q10 | — | Un masque (pente, humidité) lu par le shader, par un Instance on Points (Selection) ou par un autre nœud de l'arbre (Named Attribute). |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`COMPLETED_EXAMPLES/ch05_05_attributes_solution.blend` (+ `_reference.png`).

**Fabrication.** Générée par script (`build_ch05_05_files.py`). Score du correcteur 38/38 ; starter 10/38.
Mesures évaluées : « height » Point / Float, écart-type 0,139, écart moyen à z 0,000 mm, 10 000 sommets ; shader Attribute « height » → Map Range → Color Ramp.
Rendu regardé : bleu dans les creux, vert à mi-hauteur, blanc sur les crêtes ; deux vues cohérentes.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_no_store` | pas de Store Named Attribute | Store, type/domaine, Value, nom, attribut évalué, variation, z, nom du shader (même défaut) |
| `…_wrong_name` | attribut nommé « altitude » | Nom ; attribut évalué ; variation ; z ; cohérence avec le shader (même défaut) |
| `…_wrong_domain` | domaine Face | Type et domaine ; attribut évalué ; variation ; z (même défaut) |
| `…_shader_unlinked` | shader sans nœud Attribute | Shader ; cohérence des noms (même défaut) |
| `…_constant` | Value constante 0,5 | Value par un champ ; variation ; z (même défaut) |
| `…_orphan` | un nœud Cube inutilisé | Aucun nœud orphelin (seul) |
Aussi refusé : le starter.

## Limites
- Attribut évalué et graphe du shader ; le matériau n'est pas rendu par le correcteur.
- Un seul Store Named Attribute est lu (le premier).
