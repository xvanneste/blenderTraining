# CH05.09 — Cours théorique : boucles et simulation

## 1. La zone de répétition
Une **Repeat Zone** est formée de deux nœuds appariés : **Repeat Input** (`GeometryNodeRepeatInput`) et **Repeat Output** (`GeometryNodeRepeatOutput`) (en script : `repeat_input.pair_with_output(repeat_output)`). Entrées du Repeat Input : **Iterations** et les éléments d'état (ici **Geometry**) ; sorties : **Iteration** (numéro de l'itération en cours, à partir de 0) et l'état courant. Le Repeat Output reçoit l'état de fin d'itération et le renvoie à la suivante, puis à la sortie de la zone après la dernière.
Éléments d'état : `repeat_output.repeat_items` (Geometry par défaut ; on peut en ajouter : flottants, vecteurs…).

## 2. L'escalier en colimaçon
Dans la zone : Cube (1,0 × 0,4 × 0,1) → Transform 1 (Translation x = Radius) → Transform 2 (Rotation z = Iteration × radians(Angle) ; Translation z = 0,05 + Iteration × Rise) ; Join Geometry (état précédent + marche) → Repeat Output.
Interface : Steps (Integer 3–60, 16), Angle (Float 5–45, 22,5°), Rise (0,05–0,5, 0,18 m), Radius (0,5–3, 1,2 m). Set Material (MAT_Step) en sortie.

## 3. Mesures
Réglage A (16 ; 22,5° ; 0,18 ; 1,2) : 16 marches, première à z = 0,05, contremarche 0,18, 22,5° entre marches, rayon 1,20. Réglage B (30 ; 15° ; 0,12 ; 2,0) : 30 marches, 0,12 m, 15°, rayon 2,00.

## 4. Simulation Zone et For Each Element (présentation)
- **Simulation Zone** (`GeometryNodeSimulationInput`/`Output`) : l'état évolue d'une IMAGE à la suivante (Delta Time) ; il est mis en cache et peut être baké. Idéal pour des particules, de la croissance, un tissu simplifié. Elle exige une lecture de la timeline : non évaluée ici.
- **For Each Element** (`GeometryNodeForeachGeometryElementInput`/`Output`) : exécute un traitement pour chaque élément d'un domaine. Plus lourd qu'un champ, il sert quand le résultat de chaque élément est de la géométrie.
Les trois zones existent dans l'API 5.3 (nœuds créés sans erreur) ; ce chapitre ne teste que la Repeat Zone.

## 5. Pièges
- Join sans l'état précédent : une seule marche.
- Iterations en dur : la zone ignore Steps.
- Rotation avant translation : marches sur l'axe, pas en spirale.
- Itérations sans borne : la zone peut bloquer Blender ; borner Steps.
- État non déclaré (item manquant) : la valeur ne survit pas à l'itération.

## 6. Limites
Le correcteur mesure les marches d'une Repeat Zone ; il ne teste ni Simulation Zone ni For Each Element. Le résultat est de la géométrie réelle (pas d'instances).
