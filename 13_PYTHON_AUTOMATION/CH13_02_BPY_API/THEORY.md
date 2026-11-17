# CH13.02 — Données, contexte et opérateurs

## Où chercher une information

| API | Question | Exemple |
|---|---|---|
| `bpy.data` | Quels blocs existent dans le fichier ? | `bpy.data.objects.get("GEO_Crate_B")` |
| `bpy.context` | Sur quoi l’utilisateur travaille-t-il ici ? | `bpy.context.view_layer.objects.active` |
| `bpy.ops` | Quelle action Blender puis-je déclencher ici ? | `bpy.ops.mesh.primitive_uv_sphere_add(...)` |

Un objet trouvé dans `bpy.data.objects` peut appartenir à une autre scène ou à une collection masquée. Pour travailler dans la scène courante, cherchez dans `bpy.context.scene.objects` ou vérifiez l’appartenance avant d’agir. `get` renvoie `None` quand le nom est absent.

## Objet, maillage et matériau

L’objet porte notamment sa position. Son `data` contient le maillage. Deux objets peuvent pointer vers le même maillage et conserver des positions différentes. Le premier slot du starter utilise une liaison **Data**. Remplacer le matériau dans ce maillage touche donc les deux caisses tant que le maillage reste partagé. Après `b.data = b.data.copy()`, la liste de matériaux du maillage B est indépendante. Les matériaux qu’elle contient restent eux-mêmes des références. Pour modifier les réglages internes d’un matériau encore partagé, copiez aussi ce matériau.

## Sélection et opérateurs

Un seul objet peut être actif dans le calque de vue. Plusieurs objets peuvent être sélectionnés. `obj.select_set(True)` et `bpy.context.view_layer.objects.active = obj` règlent chacun un état distinct. La propriété `bpy.context.object` se lit. Elle reflète le contexte courant.

La console et l’éditeur Info répondent à deux besoins différents. Dans la console, exécutez une expression et lisez son résultat. Dans l’éditeur Info, observez la commande produite par une action de l’interface. Lorsqu’un opérateur dépend de la zone ou du mode, vérifiez `poll()` dans le contexte où vous comptez l’appeler. Après un ajout réussi, l’opérateur renvoie un statut comme `{'FINISHED'}`. L’objet créé se retrouve via le contexte, ici immédiatement après l’appel.

## Cas de production

Deux cubes liés peuvent avoir des noms, positions et matériaux visibles différents selon le lien utilisé par les slots. Si la couleur de B est modifiée dans ses données et que A change aussi, inspectez l’utilisateur du maillage. Une copie de B seule n’isole pas automatiquement les données de maillage. Le b.data = b.data.copy() intervient quand vous voulez modifier cette copie en particulier.
