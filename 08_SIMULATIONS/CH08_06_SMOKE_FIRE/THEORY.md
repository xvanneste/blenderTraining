# CH08.06 — Cours théorique : Fumée et feu

## 1. Domaine de gaz
Le domaine (Gas) simule une grille (densité, température, combustible, flamme). Résolution : nombre de divisions de la plus grande dimension (32 ici). Flottabilité, dissipation et turbulence règlent le comportement.

## 2. Foyer
Un objet Flow produit du gaz : Smoke (fumée), Fire (flammes), Fire + Smoke (BOTH). Comportement Inflow : alimentation continue ; Geometry : remplit le volume à l'image 1.

## 3. L'exercice
FLAME_Domain : 2 × 2 × 3 m. FLAME_Source : 0,4 × 0,4 × 0,2 m au fond (z = 0,3 m). Domaine : Gas, Resolution Divisions 32, Modular, images 1–30. Foyer : Fire + Smoke, Inflow. Matériau MAT_Flame : Principled Volume ; Attribute « density » vers Density, Attribute « flame » vers Emission Strength.

## 4. Shader de volume
Le gaz se rend comme un volume : le nœud Principled Volume reçoit la densité (absorption/diffusion) et l'émission de la flamme via des nœuds Attribute. Relié à la sortie Volume du Material Output.

## 5. Mesure par le cache
Le correcteur cuit les données (Bake Data) dans un dossier temporaire et lit la taille des fichiers `fluid_data_NNNN.vdb`. Solution : 62 Ko (image 1) à 165 Ko (image 30), rapport 2,64 ; fumée seule : 51 à 111 Ko ; sans foyer : 17 Ko constants ; résolution 8 : 54 Ko à 55 Ko.

## 6. Pièges
- Cache en mode Replay : seule l'image 1 est cuite (essai : un seul fichier). Il faut Modular.
- Résolution trop basse.
- Foyer non déclaré Flow.
- Oublier le shader de volume (rien ne s'affiche au rendu).
- Domaine trop petit : le gaz en sort.

## 7. Limites
Le correcteur ne voit pas la forme de la flamme (la grille n'est pas lue) mais sa taille de cache ; le rendu du volume (EEVEE ou Cycles) n'est pas testé ; la fumée seule n'est refusée que par la configuration (type du foyer) ; pas de collisions ni de vent (CH08.09).
