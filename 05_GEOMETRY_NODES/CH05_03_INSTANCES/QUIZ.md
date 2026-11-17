# CH05.03 — Quiz (10 questions, seuil 8/10)

Répondez sans regarder le cours, puis corrigez avec [SOLUTIONS.md](SOLUTIONS.md).
Version interactive : application de l'académie (`QUIZZES/ch05_03.json`).

**Q1.** (L1) Qu'est-ce qu'une instance ?

   a) Une copie complète de la géométrie
   b) Une référence à une géométrie partagée, placée par une matrice
   c) Un modificateur
   d) Un matériau

**Q2.** (L1) Que reçoit l'entrée Points d'Instance on Points ?

   a) Une couleur
   b) Un maillage ou un nuage de points : une instance par sommet
   c) Un matériau
   d) Une image

**Q3.** (L1) Pourquoi translater le piquet de z = 0,5 avant d'instancier ?

   a) Pour le rendre plus grand
   b) Le Cylinder est centré : son origine doit être à sa base pour qu'il se pose sur le point
   c) Pour le colorer
   d) Pour le lisser

**Q4.** (L1) Combien d'instances produit une Grid de 21 × 21 sommets ?

**Q5.** (L1) Quelles entrées d'Instance on Points pilotent la variation ?

**Q6.** (L2) Comment rendre la rotation aléatoire autour de Z ?

   a) Random Value (Vector, Max z = 6,283) → Rotation
   b) Math → Scale
   c) Set Position
   d) Realize Instances

**Q7.** (L2) Quel est le défaut de Realize Instances ici ?

   a) Il lisse
   b) Il transforme chaque instance en géométrie propre : 441 fois les sommets, plus de partage
   c) Il supprime le matériau
   d) Il colore

**Q8.** (L2) Pourquoi borner le nombre d'instances (100–1 600) ?

**Q9.** (L2) Comment le correcteur mesure-t-il les orientations réparties ?

**Q10.** (L2) Quand faut-il réaliser les instances ?

