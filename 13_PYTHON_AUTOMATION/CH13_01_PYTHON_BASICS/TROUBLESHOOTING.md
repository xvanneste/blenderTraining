# CH13.01 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| « NameError : name 'bpy' is not defined » | import bpy oublié | Ajouter `import bpy` en haut du texte |
| « IndentationError » | Indentation mélangée | 4 espaces par niveau |
| « ZeroDivisionError » | Division par len([]) | Traiter la liste vide d'abord |
| La fonction renvoie None | return oublié | Ajouter return |
| Rock_1 au lieu de Rock_001 | Format sans 03d | f"{i:03d}" |
| Les cubes sont tous à l'origine | location oublié | location=p |
| Cube.001 au lieu de Cube_001 | Nom non fixé | ob.name = f"Cube_{i:03d}" |
| La grille est transposée | Boucles inversées | y à l'extérieur, x à l'intérieur |
