# Corrigés

## Quiz

1. **Sommets, arêtes, faces**. Chaque face référence des indices de sommets.
2. **La position de l’objet**. Les huit sommets gardent leurs coordonnées locales.
3. **Deux**. Une seule face caractériserait ici une bordure ouverte.
4. **Pour libérer la structure temporaire**. Le maillage Blender a déjà reçu les données via bm.to_mesh(mesh).
5. Le modificateur ajoute des faces dans le résultat évalué et laisse le datablock d’origine éditable.
6. **Fac**. Le tutoriel remappe un facteur scalaire.
7. **Roughness**. La valeur pilote la rugosité locale du reflet.
8. **X**. X dépend de la colonne et Y de la rangée.
9. Le bloc à cet indice change de dimension verticale et conserve sa position au sol.
10. Repartir d’une copie propre du starter, lancer le même texte et retrouver les six objets, leurs positions et leur matériau.

## Exercices

1. Le bloc de contrôle mesure 0,88 × 0,88 × 0,54 m. Le dessus pointe vers +Z et le fond vers −Z. Le biseau crée une petite surface intermédiaire qui attrape la lumière.
2. Ouvrez le [corrigé Blender](COMPLETED_EXAMPLES/ch13_03_presentoir_solution.blend). Le bloc ocre GEO_Bloc_2_3 se trouve en (1,12 ; 1,12 ; 0) et mesure 0,90 m de haut. Le [script de référence](SCRIPTS/generer_presentoir.py) montre la construction de chaque bloc et des deux matériaux.
3. Utilisez trois lignes de deux hauteurs dans le tableau. Dans la boucle, placez X à (colonne − 0,5) × 1,35 et Y à rang × 1,35. Attribuez l’ocre si (rang + colonne) % 2 vaut 1 et le bleu sinon. La grille comporte alors trois blocs de chaque couleur.
