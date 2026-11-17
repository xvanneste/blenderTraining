# Théorie — Générer des volumes et des matériaux

## 1. Coordonnées locales et position de l’objet

Les huit points du bloc sont définis autour de son origine. Les quatre sommets du bas ont Z = 0 et les quatre du haut ont Z = hauteur. Chaque face contient les indices de ses sommets dans l’ordre du contour. Le sens de parcours fixe l’orientation de sa normale. Une fois les faces écrites dans le maillage avec `from_pydata`, le bloc existe comme datablock. Créer l’objet puis le lier à la collection le rend visible sur la scène. La position en X et Y appartient à l’objet, donc le même constructeur fonctionne pour chaque case.

## 2. BMesh et maillage évalué

BMesh expose la connectivité des faces et des arêtes. On copie le maillage, on recalcule ses normales, puis on réécrit le résultat avant de libérer la structure temporaire. Pour un bloc fermé, chaque arête sépare deux faces. Le recalcul des normales dépend d’une connectivité cohérente. Une face manquante demande de réparer la géométrie. Le modificateur Bevel travaille ensuite sur le maillage évalué. Les sommets ajoutés par le biseau apparaissent dans le résultat visible, tandis que le maillage de base garde huit sommets.

## 3. Le graphe pilote le reflet

La couleur de base est un triplet RGB avec un alpha de 1. Le Noise Texture produit un facteur. Map Range transforme l’intervalle 0–1 en 0,25–0,65. La connexion vers Roughness rend les reflets plus ou moins diffus selon le point de la surface. Le Principled BSDF transmet son résultat à Material Output. En affichage Solid avec la couleur Material, la couleur est lisible. Pour voir le résultat du graphe, passez à Material Preview ou lancez un rendu.

## 4. Une règle pour produire une série

Les hauteurs forment deux rangées. Les indices déterminent les positions et le bloc accent. Quand vous modifiez une hauteur dans le tableau, sa position reste la même. Quand vous modifiez le pas, le nombre de blocs reste le même. Cette séparation permet de diagnostiquer la dimension, l’implantation et le matériau indépendamment.

## Cas de production

Dans le présentoir, le pas de 1,12 m et la largeur de 0,88 m donnent 0,24 m de libre entre deux blocs. Si vous augmentez la largeur pour voir un chanfrein au premier plan, comparez-la au pas avant de relancer. Une collision entre blocs peut provenir du placement plutôt que des sommets locaux ou des normales.
