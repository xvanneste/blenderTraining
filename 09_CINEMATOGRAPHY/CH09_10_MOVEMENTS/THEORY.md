# CH09.10 — Cours théorique : Mouvements et grammaire

## 1. Échelle de plans
Large : on voit les personnages et leur environnement ; moyen : de la taille aux pieds ; gros plan : le visage. Dans l'exercice la taille se mesure en fraction de la hauteur de l'image : 27 %, 58 %, 82 %.

## 2. La ligne d'action
La droite qui relie A et B. Toutes les caméras du même côté : A reste à gauche, B à droite. Traverser la ligne inverse les côtés (mesuré : A à 74 % de la largeur au lieu de 26 %).

## 3. Le découpage
Large → moyen → serré : le spectateur se rapproche progressivement. Chaque plan a une image de départ (repère de timeline).

## 4. Les repères de caméra
Timeline : M ajoute un repère ; Marker > Bind Camera to Markers lie la caméra sélectionnée au repère. L'image active détermine la caméra de la scène.

## 5. Le travelling avant
Clés de `location.y` de CAM_MED : −8 (image 25) puis −6 (image 48), interpolation linéaire.

## 6. L'exercice
Départ : gros plan de l'autre côté (y = +4, tournée vers −Y), aucun repère, CAM_MED fixe. Solution : CAM_CLOSE en y = −4, repères 1/25/49, travelling.

## 7. Pièges
- Traverser la ligne pour un « beau » gros plan.
- Oublier de lier la caméra au repère.
- Un travelling à interpolation Bézier.
- Repères dans le désordre.

## 8. Limites
Pas de raccord de regard, de rythme ni de plan de coupe ; une seule ligne d'action ; le travelling est le seul mouvement mesuré.
