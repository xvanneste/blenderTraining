# Ressources et exercices de préparation pour la phase 13

Les références Blender 5.3 accompagnent les exercices de l'académie. Le Quickstart courant présente les notions communes. Pour un appel précis ou une option d'interface, vérifiez la version de la documentation et testez dans le Blender du cours.

| Chapitre | Lecture ciblée | Résultat à vérifier |
|---|---|---|
| CH13.01 — Python pour artistes | [Boucles et fonctions](https://docs.python.org/fr/3/tutorial/controlflow.html) | Produisez des noms numérotés pour une rangée de 3 objets, puis de 12. |
| CH13.02 — API bpy | [Quickstart](https://docs.blender.org/api/current/info_quickstart.html) et [opérateurs Blender 5.3](https://docs.blender.org/api/5.3/bpy.ops.html) | Sur une copie, retrouvez un objet par son nom, puis comparez le résultat avec et sans sélection active. Expliquez ce qui relève de `bpy.data` ou du contexte. |
| CH13.03 — Objets et matériaux | [BMesh](https://docs.blender.org/api/5.3/bmesh.html) | Générez une géométrie simple, vérifiez son nombre de faces et attribuez deux matériaux. |
| CH13.04–05 — Plans et rendu par lot | [Arguments de Blender 5.3](https://docs.blender.org/manual/es/5.3/advanced/command_line/arguments.html) | Rendez une image de deux scènes vers deux dossiers distincts. Relevez le code de sortie et le chemin produit. |
| CH13.06 — Contrôle qualité | [Quickstart, section Data Access](https://docs.blender.org/api/current/info_quickstart.html) | Contrôlez les noms et les échelles d'une scène. Introduisez un défaut à la fois et vérifiez le rapport. |
| CH13.07 — Opérateurs et interface | [Classe Operator](https://docs.blender.org/api/5.3/bpy.types.Operator.html) | Dans une scène de test, essayez un opérateur avec et sans objet actif et affichez un retour compréhensible. |
| CH13.08 — Extensions | [Créer une extension](https://docs.blender.org/manual/en/5.2/advanced/extensions/getting_started.html) et [commandes Blender 5.3](https://docs.blender.org/manual/en/5.3/advanced/command_line/extension_arguments.html) | Construisez et validez localement le ZIP de votre opérateur avec son manifeste. |
| CH13.09 — Débogage et performance | [Erreurs et exceptions](https://docs.python.org/3/tutorial/errors.html) | Reproduisez une erreur sur une petite scène, identifiez la ligne fautive, puis comparez les durées sur deux tailles de scène après correction. |

Au premier jalon, enregistrez un fichier qui contient la rangée générée et une capture après changement du nombre d'objets. Au jalon de fin de phase, démontrez votre outil sur une deuxième scène et montrez un cas qu'il signale correctement.
