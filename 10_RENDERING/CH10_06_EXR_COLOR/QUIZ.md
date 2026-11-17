# CH10.06 — Quiz (10 questions, seuil 8/10)

Répondez sans regarder le cours, puis corrigez avec [SOLUTIONS.md](SOLUTIONS.md).
Version interactive : application de l'académie (`QUIZZES/ch10_06.json`).

**Q1.** (L1) Pourquoi l'EXR peut-il stocker un pixel de valeur 1000 ?

   a) C'est un format flottant linéaire sans limite à 1,0
   b) Il compresse les couleurs
   c) Il est en 8 bits
   d) Il ignore les lampes

**Q2.** (L1) Quelle valeur relit-on pour 1000,7 en 16 bits flottants ?

   a) 1000,5 (arrondi du demi-flottant)
   b) 1000,7
   c) 1000
   d) 0,7

**Q3.** (L1) Que fait le codec DWAA ?

   a) Compression avec perte : valeurs modifiées (1001,5 mesuré)
   b) Compression sans perte
   c) Rien
   d) Il ajoute du bruit au rendu

**Q4.** (L1) Quels codecs sont sans perte ?

**Q5.** (L1) Pourquoi changer de type de média remet-il la profondeur à zéro ?

**Q6.** (L2) Comment le correcteur contrôle-t-il le format 32 bits d'un multicouche ?

   a) Il lit le type du canal Combined.R dans l'en-tête (FLOAT = 2, HALF = 1)
   b) Il regarde l'extension
   c) Il demande à l'élève
   d) Il mesure la taille

**Q7.** (L2) Pourquoi contrôle-t-il la valeur dans un EXR monocouche ?

   a) Blender relit les pixels d'un monocouche ; un multicouche n'a pas de pixels lisibles ainsi
   b) Par habitude
   c) Pour la taille
   d) Par erreur

**Q8.** (L2) La passe Depth est-elle écrite en 16 bits quand la couleur l'est ?

**Q9.** (L2) L'espace colorimétrique de l'EXR est-il vérifié ?

**Q10.** (L2) Quelle est la limite de cette mesure ?

