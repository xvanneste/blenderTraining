# CH04.08 — Cours théorique : relief

## 1. Trois techniques
| Technique | Ce qu'elle fait | Silhouette | Coût | Usage |
|---|---|---|---|---|
| **Bump** | hauteur → normale perturbée (nœud Bump) | inchangée | faible | grain, rayures, détail fin |
| **Normal map** | normales stockées dans une image (CH04.07) | inchangée | faible | détail bakés d'un haute définition |
| **Displacement** | déplace les sommets | **modifiée** | élevé (subdivision) | terrain, pierres, reliefs vus de profil |
On les combine : displacement pour la forme moyenne, bump pour le grain.

## 2. Le nœud Displacement
Entrées : **Height**, **Midlevel**, **Scale**, Normal ; sortie : Displacement → entrée **Displacement** du Material Output. Déplacement ≈ (Height − Midlevel) × Scale, selon la normale (espace Object par défaut).
Solution : Noise Texture (Scale 0,9 ; Detail 4 ; Roughness 0,55) → Height ; Midlevel 0,5 ; Scale 0,25 m.

## 3. Réglage du matériau
Material Properties > **Settings** : menu **Displacement** (`displacement_method` : *Bump Only*, *Displacement Only*, *Displacement and Bump*). Par défaut Bump Only : le nœud est alors utilisé comme un bump. Un champ **Max Displacement** existe aussi pour Cycles (libellés confirmés dans `properties_material.py` et `cycles/ui.py`).

## 4. Subdivision
Le déplacement agit sur les sommets : un plan d'une face reste plat. Solutions :
- modificateur **Subdivision Surface** en mode adaptatif (propriété `use_adaptive_subdivision`, avec `adaptive_object_edge_length` et `adaptive_pixel_size`) : Cycles subdivise selon la distance à la caméra ;
- ou niveaux de rendu élevés (≥ 6 ici).
Le correcteur accepte l'un ou l'autre.

## 5. Moteur
Le vrai displacement de ce chapitre s'effectue avec **Cycles**. Dans les sources de l'interface 5.3, la méthode « Displacement Only » est signalée « Unsupported displacement method » dans le contexte EEVEE ; le correcteur exige donc Cycles.

## 6. Pièges
- Méthode laissée sur Bump Only : aucun déplacement de silhouette.
- Pas de subdivision : un plan reste plat.
- Scale trop grand : relief absurde ; trop petit : invisible.
- Height non alimentée : déplacement constant.
- Midlevel à 0 : toute la surface monte de Scale.
- Soleil de face : le relief ne se voit pas ; l'éclairer en lumière rasante.

## 7. Limites
Le correcteur contrôle le graphe et les réglages, pas la quantité de relief rendue ; le rendu de référence (soleil rasant, silhouette ondulée) a été regardé. L'option « adaptatif » n'est pas visible dans le maillage évalué en arrière-plan.
