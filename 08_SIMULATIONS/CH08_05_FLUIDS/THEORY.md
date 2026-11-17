# CH08.05 — Cours théorique : Fluides (Mantaflow)

## 1. Mantaflow
Moteur de fluides de Blender : un **domaine** (boîte) simule liquide ou gaz ; des **Flow** y injectent la matière ; des **Effector** sont des obstacles. La simulation est cuite dans un cache.

## 2. La scène
FLUID_Domain : cube de 2 m centré à z = 1 m. FLUID_Source : cube de 0,6 m centré à z = 1,2 m. Domaine : Liquid, Resolution Divisions 32, cache modulaire images 1–20, Mesh activé. Source : Flow, Liquid, Geometry.

## 3. Le cache
Après bake_data : `data/fluid_data_NNNN.vdb` (la grille), `config/`. Après bake_mesh : `mesh/fluid_mesh_NNNN.bobj.gz` (la surface) : un entier (nombre de sommets) puis les positions (flottants xyz). Le correcteur lit ces fichiers.

## 4. Mesures
Solution : 43/43 ; 20 maillages ; image 1 : z de −0,056 à 0,266 m, 3 066 sommets ; image 20 : z de −0,475 à −0,006 m, x de −0,475 à 0,475 m (étalé sur le fond), 18 594 sommets. Contre-exemples : sans source ni liquide ; source de gaz (aucun liquide) ; résolution 8 (146 puis 380 sommets) ; cache de 5 images (z minimal −0,15 m).

## 5. Temps de calcul
Le bake de 20 images à la résolution 32 prend moins d'une seconde en arrière-plan ; une vraie simulation (128 et plus, centaines d'images) prend des minutes à des heures : on teste en basse résolution.

## 6. Pièges
- Source non déclarée Flow, ou de mauvais type.
- Résolution trop basse (liquide grossier).
- Cache trop court.
- Cuire les données sans cuire le maillage (aucune surface).
- Domaine trop petit ou trop grand pour la scène.

## 7. Limites
Un liquide qui tombe, sans obstacle ni vitesse initiale ni viscosité ; pas de gaz (CH08.06) ni de rendu d'eau (shader) ; le test de gravité du domaine n'a pas pu être fabriqué (la propriété du domaine n'a pas changé le résultat).
