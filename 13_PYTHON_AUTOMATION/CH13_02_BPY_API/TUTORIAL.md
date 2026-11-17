# CH13.02 — Réparer un atelier depuis la console

Ouvrez `STARTER_FILES/ch13_02_bpy_starter.blend` puis enregistrez une copie nommée `ch13_02_bpy_<prenom>_v001.blend` dans `STARTER_FILES`. Dans le mode Objet, ouvrez une console avec **Shift+F4** au-dessus de la vue 3D. Exécutez les lignes une par une.

## 1. Identifier la cible et le maillage partagé

```python
import bpy
a = bpy.data.objects["GEO_Crate_A"]
b = bpy.data.objects["GEO_Crate_B"]
print(bpy.context.view_layer.objects.active.name, b.name)
print(a.data == b.data)
```

Attendu au départ : A est actif alors que `b` désigne B. Le second affichage vaut `True`. Déplacez la sélection via l’Outliner, puis réaffichez la première ligne. Le nom enregistré dans `b` reste stable.

## 2. Recolorer B

```python
b.data = b.data.copy()
orange = bpy.data.materials.get("MAT_Orange") or bpy.data.materials.new("MAT_Orange")
orange.diffuse_color = (0.85, 0.25, 0.055, 1)
b.data.materials[0] = orange
print(a.data.materials[0].name, b.data.materials[0].name)
```

Attendu : `MAT_Blue MAT_Orange`. La couleur diffuse sert ici à Workbench. En vue solide, choisissez *Material* comme source de couleur si les deux caisses paraissent grises.

## 3. Ajouter un repère et restaurer la sélection

```python
bpy.ops.mesh.primitive_uv_sphere_add.poll()
bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.3, location=(1.7, 0, 0.3))
marker = bpy.context.object
marker.name = "GEO_Marker"
props = bpy.data.collections["COL_Props"]
if marker.name not in props.objects: props.objects.link(marker)

for collection in list(marker.users_collection):
    if collection != props:
        collection.objects.unlink(marker)

bpy.ops.object.select_all(action="DESELECT")
b.select_set(True)
bpy.context.view_layer.objects.active = b
print(bpy.context.view_layer.objects.active.name)
```

Dans la console interactive, terminez les blocs `if` et `for` par une ligne vide avant de passer à la suite. Le `poll()` doit afficher `True`. Avant d’exécuter la dernière partie, vérifiez dans l’Outliner que le repère apparaît dans `COL_Props`. La dernière ligne affiche `GEO_Crate_B`. Revenez à la vue 3D avec **Shift+F5** et enregistrez.

Pour retrouver la commande d’un geste, ouvrez une autre copie du starter, ajoutez une UV Sphere via le menu *Add*, puis affichez l’éditeur **Info**. Cherchez la ligne `bpy.ops.mesh.primitive_uv_sphere_add` et comparez ses arguments à ceux de l’étape 3.

## Vérifier

Depuis le dossier de ce chapitre, remplacez `<prenom>` dans la commande suivante. Le correcteur attend **12/12**.

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch13_02_bpy_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch13_02.py" -- --exercise bpy
```

## Vérification sur une variante

Dans une seconde scène, sauvegardez les identifiants de l’objet actif et du maillage de A. Reproduisez le changement de matériau sur B. Vérifiez le maillage de A et le résultat de l’opération même si A était sélectionné au départ.
