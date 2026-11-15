# CH02.13 — Cours théorique : assets réutilisables

## 1. Pourquoi une bibliothèque ?
Un film réutilise sans cesse les mêmes objets : chaises, lampes, arbres, accessoires. Les
re-modéliser ou les copier-coller de fichier en fichier crée des doublons, des versions divergentes et
des fichiers lourds. Blender gère cela avec les **assets** : des données (objets, matériaux,
collections, node groups, poses…) **marquées** pour être retrouvées dans l'**Asset Browser** et
glissées dans n'importe quelle scène.

## 2. Marquer et documenter un asset
- *Object → Asset → Mark as Asset* (ou clic droit dans l'Outliner). *Clear Asset* l'annule.
- Dans l'Asset Browser (bibliothèque *Current File*), panneau latéral `N` : **Description**,
  **Author**, **Copyright**, **License**, **Tags** (+), aperçu (icône ⟳ = *Generate Preview*).
- **Catalogues** : arborescence de rangement (*Props/Mobilier*, *Props/Nature*…), créée par **+**
  dans l'Asset Browser ; on y glisse les assets. Blender les enregistre dans
  **`blender_assets.cats.txt`** à côté du fichier : ce fichier fait partie de la bibliothèque.
Bonne pratique de l'académie : *License* et *Author* toujours renseignés, comme dans
`ASSET_MANIFEST.json` (provenance traçable).

## 3. Déclarer une bibliothèque
**Edit → Preferences → Asset Libraries** : bouton **+**, choisir le **dossier** qui contient vos
fichiers-bibliothèques (`ASSETS/` de l'académie par exemple), nom, *Import Method*. Tous les assets
des `.blend` de ce dossier apparaissent alors dans l'Asset Browser de **tous** vos projets.

## 4. Link, Append, Append (Reuse Data)
Quand on glisse un asset dans une scène (ou *File → Link / Append*) :
| Méthode | Effet | Usage |
|---|---|---|
| **Link** | référence vers le fichier source, non modifiable localement | décors partagés, personnages de production (une correction se propage partout) |
| **Append** | copie indépendante | point de départ à modifier |
| **Append (Reuse Data)** | copie, mais réutilise les données déjà importées (matériaux, textures) | éviter les doublons de matériaux |
| *Pack* | copie empaquetée | fichiers autonomes |
En production, on **lie** les assets validés et on ne les modifie que dans leur fichier source
(versionné). Pour animer un personnage lié : *Library Override* (phase 6).

## 5. Organisation conseillée
```
ASSETS/
  props_library.blend        (assets + catalogues)
  blender_assets.cats.txt
  materials_library.blend    (phase 4)
```
Un asset = un nom clair (`GEO_Stool`), origine au sol, échelle 1, transformations appliquées,
topologie validée (CH02.01–CH02.12), UV propres (CH02.11).
