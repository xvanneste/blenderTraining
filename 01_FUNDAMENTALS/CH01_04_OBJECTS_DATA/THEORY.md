# CH01.04 — Cours théorique : objets et données (datablocks)

## 1. L'idée la plus importante de Blender
Un **objet** n'est pas sa géométrie. Un objet est un **conteneur** qui possède :
- une **transformation** (position, rotation, échelle) ;
- des **modificateurs**, contraintes, propriétés ;
- un lien vers des **données** (*Object Data*) : un *Mesh* (maillage), une *Camera*, une
  *Light*, une *Curve*, une *Armature*…

```
 Objet « GEO_Post_01 » ──┐
 Objet « GEO_Post_02 » ──┼──►  Mesh « ME_Post » ──► Matériau « MAT_Wood »
 Objet « GEO_Post_03 » ──┘      (8 sommets)
```
Trois objets à des endroits différents peuvent **partager** le même maillage.

**Analogie.** Le maillage est une **partition de musique** ; l'objet est **un musicien**
qui la joue à un endroit donné. Dix musiciens peuvent jouer la même partition : si l'on
corrige une note sur la partition, les dix jouent la correction.

## 2. Les datablocks
Tout ce que contient un `.blend` est un **datablock** : objets, maillages, matériaux,
textures, images, caméras, lumières, mondes, actions d'animation, collections, scènes…
- Chaque datablock a un **nom** et un **nombre d'utilisateurs** (combien d'éléments s'en
  servent), affiché à côté de son nom (ex. `ME_Post  7`).
- Un datablock à **0 utilisateur** est *orphelin* : il est supprimé à l'enregistrement
  (ou par *File → Clean Up → Purge Unused Data*).
- Le **bouclier** (*Fake User*) donne un utilisateur fictif pour garder une donnée non
  utilisée (ex. un matériau de bibliothèque).
- L'**Outliner en mode *Blender File*** liste tous les datablocks par type.

## 3. Dupliquer : copie ou duplication liée
| Commande | Raccourci | Nouvel objet | Données |
|---|---|---|---|
| **Duplicate** | `Shift+D` | oui | **copiées** selon *Preferences → Editing → Copy on Duplicate* (maillage : oui ; matériau : non, par défaut en 5.3) |
| **Duplicate Linked** | `Alt+D` | oui | **partagées** (même maillage) |

Duplication liée : idéale pour les éléments répétés (piquets, chaises, arbres) — on modifie
la forme une fois, toutes les copies suivent ; fichier et mémoire plus légers (CH00.03).

**Rendre unique** : *Object Data* → cliquer le **nombre d'utilisateurs** à côté du nom
du maillage (*Make Single User*), ou *Object → Relations → Make Single User*.
⚠️ À faire **avant** de modifier la forme, sinon tous les objets liés sont modifiés.

**Lier après coup** : `Ctrl+L` → *Link Object Data* (CH00.03).

## 4. Joindre et séparer
- **Join** (`Ctrl+J`, Object Mode) : fusionne les objets sélectionnés **dans l'objet
  actif**. Le résultat garde le nom, l'origine et les modificateurs de l'objet actif.
  Usage : regrouper les morceaux d'un même objet rigide (une table).
- **Separate** (`P`, Edit Mode) : *Selection* (la sélection devient un nouvel objet),
  *By Material*, *By Loose Parts* (chaque partie non connectée devient un objet).
- Joindre ≠ grouper : pour **organiser** sans fusionner, on utilise les **collections**
  ou le **parentage** (CH01.08).

## 5. Ajouter des objets
`Shift+A` (ou menu *Add*) : *Mesh* (Plane, Cube, Circle, UV Sphere, Ico Sphere, Cylinder,
Cone, Torus, Grid, Monkey), *Curve*, *Surface*, *Metaball*, *Text*, *Volume*, *Grease
Pencil*, *Armature*, *Lattice*, *Empty*, *Image*, *Light*, *Light Probe*, *Camera*,
*Speaker*, *Force Field*, *Collection Instance*. Les nouveaux objets apparaissent au
**curseur 3D** (CH01.07). Le panneau *Adjust Last Operation* règle taille, segments, etc.
Supprimer : `X` (confirmation) ou `Suppr`.

## 6. En production
- Les décors utilisent massivement les **duplications liées** et les **instances de
  collections** : une forêt de 10 000 arbres = 10 modèles d'arbres.
- Un modèle livré à l'animation est souvent **un seul objet par partie déformable**,
  alors que les accessoires rigides peuvent être joints.
- Les noms de **données** comptent aussi (`ME_`, `MAT_`) : ils apparaissent dans les
  outils de pipeline et les exports.
