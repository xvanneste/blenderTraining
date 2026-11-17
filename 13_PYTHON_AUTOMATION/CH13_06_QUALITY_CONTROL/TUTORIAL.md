# Atelier guidé — Validation d’une scène

Lancez depuis la racine sur la référence puis sur une copie volontairement dégradée.

```powershell
& "C:/Program Files/Blender Foundation/Blender 5.3/blender.exe" -b 13_PYTHON_AUTOMATION/ASSETS_ATELIERS/presentoir_plans.blend --python-exit-code 1 --python 13_PYTHON_AUTOMATION/ASSETS_ATELIERS/controler_scene.py
```

Le script affiche le rapport et conserve la scène. Le code de sortie Blender signale une panne Python. Pour décider si la scène est conforme, examinez le contenu du rapport.

## 1. Point zéro

Exécutez le contrôleur sur la scène de référence. Relisez le périmètre COL_Presentoir et les images externes utilisées.

**Pourquoi** Un rapport de production doit préciser son périmètre. Les images intégrées sont disponibles dans le .blend.

**Contrôle** Le terminal affiche zéro anomalie pour la référence.

## 2. Défauts contrôlés

Sur une copie, renommez un bloc en BOX_01. Mettez l’échelle X d’un autre bloc à 1,20. Affectez une Image Texture externe à un matériau puis rendez son chemin invalide.

**Pourquoi** Une mutation volontaire par règle permet d’identifier ce que signale chaque test.

**Contrôle** Le rapport contient NOM, ECHELLE et IMAGE_ABSENTE avec les noms concernés.

## 3. Réparation

Rétablissez le préfixe, appliquez l’échelle si le mesh doit conserver sa taille, puis reliez la texture ou empaquetez-la.

**Pourquoi** La réparation doit préserver le résultat visuel. Une échelle appliquée modifie les données locales.

**Contrôle** Le rapport repasse à zéro et une vue de contrôle compare la silhouette.

## Vérification sur une variante

Introduisez les trois défauts du tutoriel l’un après l’autre et conservez le message exact de chaque mutation. S’il manque une texture, comparez les résultats quand elle est empaquetée et quand elle est relocalisée. Rouvrez chaque solution testée.
