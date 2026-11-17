# CH05.06 — Cours théorique : paramètres et interfaces

## 1. L'interface d'un arbre
L'**interface** (`node_group.interface`) liste les sockets d'entrée et de sortie et les **panneaux**. Chaque entrée (`NodeSocketFloat`, `NodeSocketInt`, `NodeSocketBool`, `NodeSocketVector`, `NodeSocketColor`, `NodeSocketObject`, `NodeSocketGeometry`…) possède : `name`, `description`, `default_value`, `min_value`, `max_value` (pour les nombres), `parent` (panneau). En script : `interface.new_socket(name, in_out='INPUT', socket_type=..., parent=...)`, `interface.new_panel(nom)`.
Dans l'interface graphique, ces réglages se modifient dans la colonne Group de l'éditeur de nœuds (l'entrée sélectionnée affiche Default, Min, Max, Description). Panneaux : à créer et à remplir en glissant les entrées.

## 2. Du Group Input aux nœuds
Le nœud **Group Input** expose une sortie par entrée. Une entrée non reliée ne fait rien. Dans l'outil : Count → Mesh Line [Count] ; Spacing → Combine XYZ [X] → Offset ; Radius → Cylinder [Radius] ; Height → Cylinder [Depth] et Math (Divide 2) → Combine XYZ [Z] → Transform [Translation].

## 3. Les valeurs dans le modificateur
En 5.3, les valeurs du modificateur sont dans `modifier.properties.inputs[identifiant]` (un groupe de propriétés contenant `value`) : on écrit `…inputs[identifiant]["value"] = 3.5`. L'identifiant (`Socket_3`…) se lit sur l'élément d'interface (`item.identifier`) ; l'ancienne écriture `modifier["Socket_3"]` n'existe plus (TypeError : « this type doesn't support IDProperties »).

## 4. L'outil de la solution
| Panneau | Entrée | Type | Défaut | Min | Max | Description |
|---|---|---|---|---|---|---|
| Dimensions | Height | Float | 2 | 0,2 | 10 | Hauteur des piliers en mètres |
| Dimensions | Radius | Float | 0,2 | 0,05 | 1 | Rayon des piliers en mètres |
| Layout | Count | Integer | 8 | 1 | 50 | Nombre de piliers |
| Layout | Spacing | Float | 1,2 | 0,3 | 5 | Distance entre deux piliers |
Arbre : Mesh Line (OFFSET) → Instance on Points (Instance = Cylinder → Transform) → Join Geometry (avec la géométrie d'entrée) → Set Material → Group Output.

## 5. Tester un outil
Un outil se teste en CHANGEANT ses paramètres. Mesures de la solution : par défaut 8 piliers, hauteur 2,00 m, étendue 8,40 m ; réglage B (Height 3,5 ; Radius 0,3 ; Count 12 ; Spacing 1,0) : 12 piliers, hauteur 3,50 m, largeur 0,60 m, étendue 11,00 m.

## 6. Pièges
- Entrée exposée mais non branchée, ou nœud laissé en dur : l'outil ment.
- Height branché seulement à Depth : base décalée du sol.
- Bornes absentes : valeurs destructrices.
- Pas de description : outil illisible.
- Noms d'entrées incohérents (casse, langue) : confusion à plusieurs.

## 7. Limites
Le correcteur teste quatre paramètres précis de cet outil ; il ne couvre ni les menus, ni les booléens, ni les objets en entrée. Les panneaux sont vérifiés par nom et appartenance.
