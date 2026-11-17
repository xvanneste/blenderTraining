# Proposition pour les phases Modélisation et Sculpture

Les deux fichiers Blender de ce dossier sont des essais autonomes pour discuter du niveau attendu avant de revoir les chapitres.

Pour comparer les formes sous le même angle, ouvrez les références actuelles du [boîtier](../../02_MODELING/CH02_05_HARD_SURFACE/COMPLETED_EXAMPLES/ch02_05_device_reference.png), de la [main](../../03_SCULPTING/CH03_07_HANDS_FEET/COMPLETED_EXAMPLES/ch03_07_hand_reference.png), du [visage](../../03_SCULPTING/CH03_06_FACES/COMPLETED_EXAMPLES/ch03_06_face_reference.png) et du [personnage P3](../../03_SCULPTING/PROJECT_P3/REFERENCE/renders/p3_turnaround.png).

| Support actuel | Ce que montre le rendu | Proposition |
|---|---|---|
| CH02.05, appareil hard surface | Le boîtier jaune montre les opérations de base. La façade uniforme donne peu d’indices sur l’usage, l’assemblage et les rayons propres à chaque pièce. | Garder l’exercice de bevel et d’inset, puis appliquer ces gestes à un enregistreur dont l’usage se comprend par la silhouette, la taille du bouton REC et la séparation coque, joint, écran et commandes. |
| CH03.06, visage | Le rendu de profil montre la saillie du nez. Les yeux très exposés, les paupières peu enveloppantes et les transitions joue-mâchoire rendent le résultat difficile à prendre comme cible réaliste. | Valider d’abord le crâne et la mâchoire en trois vues. Faire ensuite une étude d’orbite à grande échelle avec globe, paupière supérieure et inférieure, et transition vers la joue. Tester fermeture et sourire avant d’ajouter les détails de peau. |
| CH03.07, main | Les cinq doigts sont faciles à compter. Les phalanges ressemblent à des billes et le pouce se raccorde brusquement au poignet. | Partir d’une paume en coin, placer les premières articulations et le pouce dans la masse, tirer les doigts selon des axes et longueurs distincts, puis comparer le dessus et le profil avant les ongles. |
| P3, personnage complet | Le résultat illustre une pose A et un transfert de détails. La tête, les mains et les transitions du corps restent au stade mannequin. Le 68/68 couvre les points mesurés par le correcteur. | Présenter cette scène comme référence technique de départ. Scinder la validation artistique en silhouette, volumes et pose. Demander une retopologie locale et une déformation observable avant de valider la préparation à l’animation. |

## Étude de main

Ouvrez [main_etude.blend](main_etude.blend). La collection `01_Construction` contient les sections originales de la paume et des doigts. Activez-la dans l’Outliner et masquez `02_Etude` et `03_Ongles` pour retrouver le blocage. Les caméras `CAM_Dessus` et `CAM_Profil` servent à contrôler l’étagement des doigts et la courbure. [Rendu de trois-quarts](main_etude.png) · [Profil](main_profil.png)

Cette étude vise une main stylisée en argile. Les doigts effilés se raccordent à une paume continue, les bouts forment un arc et le pouce s’écarte sur son propre plan. Les masses du côté paume, les plis et les déformations restent à travailler sur des références réelles. Le maillage fusionné sert à revoir les volumes et à préparer une retopologie.

**Exercice à essayer.** Photographier sa main sous deux angles. Bloquer la paume et les axes sans ongles. Comparer les espaces entre les doigts et la hauteur de chaque articulation. Choisir une autre pose de référence et montrer ce qui doit changer dans la silhouette et dans le profil, même si la longueur des doigts reste identique.

## Accessoire hard surface

Ouvrez [atlas_r07.blend](atlas_r07.blend). Les pièces sont séparées et les modificateurs Bevel sont éditables. Travaillez d’abord coque, boucliers et commandes dans la vue solide. L’écran et sa typographie permettent ensuite de vérifier le sens de lecture au cadrage prévu. Le modèle est un concept de premier plan avec une face et un côté travaillés. Son dos et ses connexions restent à développer avant une rotation complète. [Rendu de l’Atlas R-07](atlas_r07.png)

**Exercice à essayer.** Garder la coque et dessiner deux façades, l’une pour une prise de son à main nue et l’autre pour un opérateur ganté. Comparer les vues de silhouette, les espaces autour de REC et les reflets des rayons sous la même lumière. Réaliser ensuite deux images de la commande, au repos et enfoncée, pour vérifier que les pièces ne se traversent pas.

## Jalons proposés pour un personnage

| Jalon | Livrable | Validation observable |
|---|---|---|
| Première séance | Deux silhouettes contrastées en aplats | En miniature, la pose et les masses principales se distinguent. |
| Blocage | Face, profil et trois-quarts dans une lumière neutre | Le bassin, la cage et les appuis se lisent. Une correction faite de face reste cohérente de profil. |
| Étude ciblée | Une main ou une orbite basée sur deux vues de référence | Une deuxième pose ou expression explique où les volumes changent. |
| Préparation à l’animation | Une zone critique retopologisée et une pose test | À 90° au coude ou lors d’un clignement, examiner le pincement, les intersections et la perte de volume. |

Contrôlez les volumes sous une lumière neutre avec une caméra fixe. Faites ensuite la même revue après un changement de pose. Pour l’échelle, les normales et les contraintes de livraison, utilisez des mesures reproductibles. Pour juger le caractère et la perte de volume, comparez les images à la référence et décrivez le raccord précis qui demande une correction.

## Références de travail

- [Blender Studio · Stylized Character Workflow](https://studio.blender.org/training/stylized-character-workflow/) pour l’ordre blocage, plans, expression, retopologie. Les principes de forme sont utiles même si la série emploie une ancienne version de Blender.
- [Blender Studio · Generic Retopology](https://studio.blender.org/training/realistic-human-research/retopology/) pour placer les boucles en fonction des futurs mouvements.
- [Blender Studio · Modeling](https://studio.blender.org/tools/artist-guide/asset-creation/modeling) pour construire et vérifier les pièces d’un accessoire en fonction de son usage et de l’échelle.

Les deux essais sont générés par [build_studies.py](build_studies.py). Les fichiers existants du cours sont conservés.
