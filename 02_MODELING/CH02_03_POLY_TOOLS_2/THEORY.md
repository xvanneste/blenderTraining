# CH02.03 — Cours théorique : outils polygonaux II

Les outils de CH02.02 **ajoutent** de la matière ; ceux-ci **découpent**, **font tourner** et
**nettoient**.

## 1. Knife — `K`
Dessine des coupes libres sur les faces. Clic gauche = point de coupe ; `Entrée` ou `Espace` =
valider ; `Échap` = annuler ; **clic droit** = terminer la ligne en cours et en commencer une
nouvelle. Pendant la coupe (keymap 5.3) : **maintenir `Shift`** aimante au **milieu** des arêtes,
**maintenir `Ctrl`** ignore l'aimantation, `A` contraint les angles, `C` coupe **à travers** l'objet
(faces cachées comprises), `X` / `Y` / `Z` contraignent à un axe, `S` affiche distances et angles,
`V` bascule le test de profondeur. `Shift+K` coupe seulement la sélection, à travers. Le Knife est l'outil pour **rediriger une
boucle**, ouvrir une fenêtre dans un mur, découper un motif — en restant en quads si possible.

## 2. Bisect — menu *Mesh*
Coupe l'objet par un **plan** infini. On trace une ligne à l'écran, puis on règle dans le panneau :
*Plane Point*, *Plane Normal* (en coordonnées **locales**), **Fill** (boucher la coupe),
**Clear Inner / Clear Outer** (supprimer un côté). Usages : couper un objet en deux pour le mirrorer
(CH02.07), ajuster une hauteur exacte, créer une section.

## 3. Spin — `Alt+E` → *Spin* (ou outil Spin de la barre d'outils)
Fait **tourner** la sélection autour d'un axe passant par le **curseur 3D** : un profil devient un
objet de révolution (vase, verre, pied de lampe, roue). Réglages : *Steps*, *Angle* (360° pour un
tour complet), *Axis*, *Center*, *Auto Merge*, *Use Duplicates*.
**Constat vérifié (Blender 5.3.0)** : *Auto Merge* soude la **couture** entre le début et la fin du
tour, mais **pas** les sommets d'un profil posé **sur l'axe** : on obtient 24 points superposés au
centre du fond. Toujours terminer par `A` puis `M` → *By Distance*.

## 4. Screw — modificateur (Generate) ou opérateur (menu *Edge*)
Combine rotation **et** translation : hélices, ressorts, vis, escaliers tournants. Le **modificateur
Screw** reste non destructif : *Angle*, *Screw* (montée par tour), *Iterations* (nombre de tours),
*Steps* / *Render Steps*, *Axis*, *Merge Vertices*. La forme de départ (cercle de section) est
**décalée** de l'origine : ce décalage est le rayon de l'hélice.

## 5. Merge — `M`
Fusionne des sommets sélectionnés : **At Center**, **At Cursor**, **Collapse** (chaque groupe
connecté en un point), **At First**, **At Last**, **By Distance** (doublons). *At Center* sur les 4
sommets du haut d'un cube donne une pyramide.

## 6. Dissolve — `X` → *Dissolve…* ou `Ctrl+X`
**Supprime sans trouer** : les faces voisines se réunissent.
| Commande | Effet |
|---|---|
| *Dissolve Vertices / Edges / Faces* | retire l'élément, fusionne les faces autour |
| **Limited Dissolve** | retire toutes les arêtes **inutiles** sur des zones planes (*Max Angle*) |
| *Collapse Edges & Faces* | réduit chaque élément à un point |
| *Edge Loops* (Delete) | retire une boucle entière proprement |
`Delete` (X → Vertices/Edges/Faces) **troue** le maillage ; *Dissolve* le **simplifie** : ce sont deux
gestes différents. *Limited Dissolve* nettoie un maillage importé ou issu d'un booléen (CH02.07)
— attention, il crée volontiers des n-gons, à réserver aux surfaces plates qui ne se déformeront pas.

## 7. Bon réflexe
Après chaque découpe : **Statistics** (sommets, faces), *Select All by Trait → Non Manifold* et
*Faces by Sides* (CH02.01). Découper vite, mais vérifier toujours.
