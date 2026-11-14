# CH00.01 — Quiz (20 questions, seuil de réussite 16/20)

Répondez sans regarder le cours, puis corrigez avec [SOLUTIONS.md](SOLUTIONS.md).
Le format est aussi disponible en JSON pour l'application : `QUIZZES/ch00_01.json`.

### Écosystème (L1)
**Q1.** Sous quelle licence Blender est-il distribué ?
a) Freeware propriétaire · b) GNU GPL · c) Creative Commons BY · d) MIT

**Q2.** Vous vendez un court-métrage entièrement réalisé dans Blender. Qu'en est-il des droits sur le film ?
a) Le film doit être publié sous GPL · b) Il vous appartient · c) Il appartient à la Blender Foundation · d) Vous devez payer une licence commerciale

**Q3.** Que signifie le dernier chiffre de `5.3.1` ?
a) Une version bêta · b) Une version de correction de bugs · c) Une version LTS · d) Le numéro de build

**Q4.** Combien de temps une version LTS est-elle maintenue ?
a) 3 mois · b) 1 an · c) 2 ans · d) 5 ans

**Q5.** Pourquoi ne faut-il pas utiliser une *daily build* pour un projet réel ?
(réponse courte)

### Installation (L2)
**Q6.** Quelle méthode ne nécessite PAS de droits administrateur ET permet d'avoir plusieurs versions ?
a) Installeur .msi · b) Microsoft Store · c) Zip · d) Aucune

**Q7.** Comment rendre une installation zip « portable » ?
(réponse courte)

**Q8.** Quel est le principal risque du Microsoft Store pour une production longue ?
(réponse courte)

**Q9.** Une installation zip ne crée pas d'association de fichiers. Citez une façon de l'ajouter.

### Dossiers et préférences (L3)
**Q10.** Où se trouvent les préférences de Blender 5.3 sous Windows (installation non portable) ?

**Q11.** Quelle est la différence entre `userpref.blend` et `startup.blend` ?

**Q12.** Que fait l'argument `--factory-startup` ?
a) Réinstalle Blender · b) Supprime vos préférences · c) Démarre sans lire vos préférences ni votre startup.blend · d) Démarre en mode sans échec réseau

### GPU et ligne de commande (L4)
**Q13.** Vous avez coché votre GPU dans les préférences, mais le rendu Cycles utilise toujours le CPU. Pourquoi ?

**Q14.** Quelle API de calcul choisir pour une NVIDIA RTX 3080 ? (deux réponses acceptables, dites laquelle vous testez en premier)

**Q15.** Pourquoi le premier rendu GPU d'une session est-il souvent plus lent ?

**Q16.** Que fait cette commande ? `blender -b scene.blend -o //out/img_#### -f 10`

**Q17.** À quoi sert `--python-exit-code 1` ?

### Diagnostic (L5)
**Q18.** Citez les 5 suspects d'un rendu noir ou vide, dans l'ordre de la méthode « de la caméra vers la lumière ».

**Q19.** Une collection entière n'apparaît pas au rendu alors que ses objets sont visibles dans le viewport. Que vérifiez-vous ?

**Q20.** Pourquoi faire un rendu de contrôle à 25 % et 8 échantillons plutôt qu'un rendu final pour diagnostiquer ?
