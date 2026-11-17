# Exercices dans Blender

## 1 · Construire et inspecter un bloc

Dans une copie du starter, ajoutez à la fin du premier bloc Python du tutoriel les trois lignes suivantes, puis lancez le script.

```python
essai = bpy.data.collections.new("COL_Essai")
bpy.context.scene.collection.children.link(essai)
creer_bloc(essai, "GEO_Essai", 0, 0, 0.54)
```

Sélectionnez le bloc, passez en mode Édition et activez **Face Orientation** dans le panneau Overlays. Cherchez des faces extérieures retournées. Revenez en mode Objet et examinez le biseau en désactivant puis réactivant l’icône d’écran du modificateur. Notez quelles arêtes changent dans le reflet. Conservez ce fichier si vous souhaitez comparer les étapes.

## 2 · Générer le présentoir de référence

Ouvrez une nouvelle copie du starter et insérez les trois blocs du tutoriel. Enregistrez la scène générée et vérifiez les points suivants avant de lancer le correcteur.

- Vue de dessus, deux rangées de trois avec un écart entre les blocs.
- Vue caméra, pente des hauteurs et accent ocre dans la rangée arrière à la troisième colonne.
- Shader Editor, Noise → Map Range → Roughness sur chacun des deux matériaux.
- Deuxième copie propre du starter, le même script produit les mêmes six objets.

**Livrable** Le .blend avec son script et une capture de la vue caméra ou un rendu. Le correcteur standard s’applique à cet exercice.

## 3 · Décliner le présentoir

Sur une copie distincte, générez trois rangées de deux blocs avec un pas de 1,35 m. Alternez les deux matériaux en fonction de la parité de la somme des indices. Faites une capture de dessus et une vue caméra. Vérifiez l’absence de chevauchement et les six emplacements. Ajustez le cadre en agrandissant l’échelle orthographique de la caméra si la nouvelle grille déborde. Comparez votre règle de placement au [corrigé](SOLUTIONS.md).
