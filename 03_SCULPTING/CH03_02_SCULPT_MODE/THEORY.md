# CH03.02 — Cours théorique : le Sculpt Mode

## 1. Sculpter, c'est déplacer des sommets
En Sculpt Mode, les brosses **déplacent les sommets existants** d'un maillage dense (des dizaines de
milliers de faces). La forme dépend donc de la **densité** : pas de détail possible sans assez de
sommets. Ce chapitre travaille à densité fixe (24 576 faces) ; les méthodes pour changer de densité
(DynTopo, Voxel Remesh, Multiresolution) sont au CH03.03.
Entrer : sélection de l'objet, **Ctrl+Tab** (pie des modes) > Sculpt Mode, ou le menu de mode de
l'en-tête, ou l'espace de travail *Sculpting*.

## 2. Les brosses de base (assets « Essentials » de Blender 5.3)
| Brosse (raccourci) | Effet | Usage |
|---|---|---|
| **Draw** (V) | pousse la surface le long de la normale | volumes généraux |
| **Clay Strips** (C) | ajoute de la matière en bandes plates | construire des plans, des masses |
| **Inflate/Deflate** (I) | gonfle / dégonfle | joues, lèvres |
| **Grab** (G) | tire une zone entière | corriger une silhouette |
| **Snake Hook** (K) | étire en suivant la souris | cornes, mèches |
| **Crease Polish** (Shift+C) | creuse un sillon net | plis, bouche, paupières |
| **Pinch/Magnify** (P) | resserre les arêtes | arêtes vives |
| **Scrape/Fill** (Shift+T) | aplanit les bosses / comble les creux | plans |
| **Smooth** (S, ou **Shift** maintenu) | adoucit | à tout moment |
| **Mask** (M) | peint un masque protecteur | protéger des zones |
Toutes ces brosses sont des *assets* : le sélecteur de brosses de l'en-tête ou de la barre d'outils
liste les autres (Blob, Layer, Pose, Boundary, Cloth…).

## 3. Rayon, force, inversion
- **F** : rayon (glisser puis clic) ; **Shift+F** : force ; **Ctrl+F** : rotation de la texture.
- **[** et **]** : rayon par pas.
- **Ctrl** maintenu : inverse la brosse (Draw creuse au lieu de pousser).
- **Shift** maintenu : lissage temporaire.
- Rayon en *View* (taille à l'écran) ou *Scene* (taille réelle) : à choisir dans les réglages de la brosse.
- Une tablette graphique (pression) aide beaucoup, mais n'est pas obligatoire.

## 4. La symétrie
En-tête du Sculpt Mode : **Mirror X / Y / Z**. Activée, chaque coup de brosse est répété de l'autre
côté du plan de symétrie **local** de l'objet. Un visage se sculpte avec Mirror X (face vers −Y).
*Symmetrize* recopie un côté sur l'autre si la symétrie a été oubliée.

## 5. Les masques
Un masque **protège** les sommets : les brosses n'agissent plus sur eux (zones sombres à l'écran).
Brosse **Mask** (M), **B** : masque rectangulaire, **Alt+M** : effacer le masque, **Ctrl+I** : inverser,
**Shift+A** : *Expand* (masque qui s'étend depuis la souris). Le masque est enregistré dans le fichier
(attribut de sommet `.sculpt_mask`). Usage : protéger ce qui est fini, isoler une zone, préparer une
extraction.

## 6. Les Face Sets
Des **groupes de faces** colorés, pour organiser le sculpt : masquer/afficher une zone (**H** : cacher
le Face Set sous la souris, **Shift+H** : l'isoler / tout réafficher (bascule), **Alt+H** : tout afficher), masquer rapidement,
travailler par parties. Création : brosse **Face Set Paint**, menu *Face Sets* (*Initialize Face Sets*
par parties, normales, matériaux…), **Ctrl+W** (édition : agrandir/réduire). Stockés comme attribut de
face `.sculpt_face_set`.

## 7. Méthode
Grandes formes d'abord (Draw, Clay Strips, Grab) → formes secondaires (Crease, Inflate) → lissage →
détails seulement quand les volumes sont justes. Tournez constamment autour du sujet, regardez la
silhouette, sculptez avec la symétrie active et protégez ce qui est fini par un masque.
