# CH04.11 — Quiz (10 questions, seuil 8/10)

Répondez sans regarder le cours, puis corrigez avec [SOLUTIONS.md](SOLUTIONS.md).
Version interactive : application de l'académie (`QUIZZES/ch04_11.json`).

**Q1.** (L1) Quel espace pour une image d'albedo (couleur) ?

   a) Non-Color
   b) sRGB
   c) Linear Rec.709
   d) Raw

**Q2.** (L1) Quel espace pour une carte de rugosité ?

   a) sRGB
   b) Non-Color
   c) AgX Base sRGB
   d) Rec.2020

**Q3.** (L1) Que se passe-t-il si une normal map est en sRGB ?

   a) Rien
   b) Les vecteurs sont décodés avec une courbe qui les déforme : relief faux
   c) Le moteur plante
   d) La couleur est plus vive

**Q4.** (L1) Donnez la règle simple pour décider de l'espace d'une image.

**Q5.** (L1) Pourquoi le nom « Non-Color » ?

**Q6.** (L2) Quel est le rôle d'un View Transform ?

   a) Changer les UV
   b) Convertir l'image linéaire de la scène en image affichable en compressant les hautes lumières
   c) Choisir le moteur
   d) Baker

**Q7.** (L2) Pourquoi laisser Gamma à 1 ?

   a) C'est faux, il faut 2,2
   b) La conversion d'affichage est déjà faite par le Display Device ; un gamma supplémentaire délave l'image
   c) Gamma est désactivé
   d) Pour baker

**Q8.** (L2) Que montre la mesure du panneau lumineux avec Standard et avec AgX ?

**Q9.** (L2) Pourquoi une sortie maître en OpenEXR ?

**Q10.** (L2) Pourquoi éviter une exposition de +4 ?

