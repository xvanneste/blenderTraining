# CH13.01 — Cours théorique : Python pour artistes

## 1. Variables et nombres
`x = 3` crée une variable ; `x * 2` calcule. Les décimaux sont des `float` (0.5), les entiers des `int`. Les textes (chaînes) s'écrivent entre guillemets ; `f"{prefix}_{i:03d}"` insère des valeurs dans un texte (f-string) : `03d` = entier sur 3 chiffres avec des zéros.

## 2. Listes
`L = [1, 2, 3]` ; `len(L)` = longueur ; `L.append(4)` ajoute ; `sum(L)` additionne ; `L[0]` est le premier élément. Une liste vide `[]` est « fausse » : `if not L:` est vrai pour une liste vide. Un tuple `(x, y, z)` est une liste figée, pratique pour une position.

## 3. Boucles et conditions
`for i in range(3):` donne 0, 1, 2 ; `range(1, 4)` donne 1, 2, 3 (la fin est exclue). `enumerate(positions)` donne (indice, élément). Deux boucles imbriquées parcourent une grille : l'extérieure varie lentement, l'intérieure vite. `if … :` choisit un chemin ; `max(a, b)` et `min(a, b)` aident à borner : `max(bas, min(haut, valeur))`.

## 4. Fonctions
`def f(a, b):` définit ; `return` renvoie une valeur ; sans `return`, la fonction renvoie `None`. Une fonction fait UNE chose et se teste seule. L'indentation (4 espaces) délimite le corps.

## 5. Blender : bpy et les opérateurs
`import bpy` donne accès à Blender. `bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, y, z))` ajoute un cube ; le nouvel objet est `bpy.context.object`, qu'on renomme (`ob.name = "Cube_000"`). C'est le même opérateur que Add > Mesh > Cube dans l'interface. Les objets de la scène sont dans `bpy.data.objects`.

## 6. Le texte exercise.py
Le fichier contient un Texte (Text Editor, espace de travail Scripting). Menu Text > Run Script (Alt+P) l'exécute : les fonctions sont définies, rien ne se passe tant que vous ne les appelez pas. Le correcteur les appelle pour vous avec des cas précis.

## 7. Ce que teste le correcteur
clamp (4 cas) ; average (4 cas dont la liste vide) ; grid_positions (3 cas dont 0 colonne) ; numbered_names (3 cas dont 0 nom) ; make_cubes (3 positions : nombre, noms Cube_000 à Cube_002, maillage de 8 sommets, position à 1 mm, liste renvoyée). Total 56 points. Le starter fait 6/56 ; chaque contre-exemple perd uniquement les points de sa fonction.

## 8. Limites
Les fonctions « pures » sont exécutées dans un fil séparé avec un délai de 5 s (boucle infinie détectée) ; make_cubes est exécutée directement (bpy.context n'existe pas dans un autre fil) et n'a donc pas de délai. Le correcteur teste le comportement, pas le style du code. Un code qui triche (renvoyer les valeurs attendues en dur) ne passerait que les cas connus : d'où plusieurs cas par fonction.

## Cas de production

Une fonction qui renvoie des positions peut se tester avant d’ouvrir Blender. Pour 3 colonnes espacées de 1,2 m, les positions X attendues par grid_positions à partir de l’origine sont 0, 1,2 et 2,4. Calculez cette sortie sur papier, puis comparez la liste renvoyée. Contrôlez aussi le cas d’une colonne. Ce test sépare erreur de calcul et erreur de liaison d’objet dans Blender.
