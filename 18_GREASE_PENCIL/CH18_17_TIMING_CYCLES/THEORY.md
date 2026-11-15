# CH18.17 — Cours théorique : timing, espacement, cycles

## 1. La feuille d'exposition (*X-sheet*, *dope sheet* papier)
Tableau vertical, une ligne par image : quel **dessin** est exposé à chaque image, sur quel niveau
(calque), avec dialogue et caméra. C'est la « partition » de l'animation 2D. Dans Blender, la
**Dope Sheet** en mode *Grease Pencil* joue ce rôle horizontalement : chaque losange = un dessin,
qui reste exposé jusqu'au losange suivant.
**Exposer** un dessin : décider combien d'images il dure.
- **En un** (*singles*) : 1 image par dessin — mouvements rapides, précis.
- **En deux** (*doubles*) : 2 images — le standard.
- **En trois** ou plus : mouvements lents, ou pause (*hold*).
On **mélange** dans une même action : en deux pour l'ensemble, en un pour un geste vif, tenue longue
pour une pose qui doit être lue.

## 2. Re-minuter sans redessiner
Le même jeu de dessins change de caractère selon l'exposition. Exemple du chapitre : une tête qui
tourne en 8 dessins. En un (8 images = 1/3 s) : sec, mécanique. Avec la feuille A en trois, B en
deux, C–F en un, G en deux, H tenu : **démarrage lent, passage rapide, arrivée amortie** puis tenue
(18 images). C'est le *slow in / slow out* obtenu par l'exposition plutôt que par l'espacement.

## 3. Le cycle
Un **cycle** est une animation dont la dernière image s'enchaîne sur la première : marche, course,
battement d'ailes, flamme. Règles :
- la pose après la dernière image = la **première** (on ne la redessine pas en fin de cycle) ;
- vérifier la boucle à l'**onion skinning** : *Show Start Frame* affiche l'image 1 après la dernière ;
- un cycle de marche contient **deux pas** (gauche, droit).

## 4. Le cycle de marche (de profil, sur place)
Cycle de 24 images (1 s, deux pas de 12 images ≈ marche normale) animé en deux = 12 dessins.
Quatre poses par pas :
1. **Contact** (images 1 et 13) : jambes au plus écarté, talon avant qui touche, bras opposés.
2. **Bas** (*down*, 3 et 15) : le poids tombe sur la jambe avant, genou fléchi : corps au plus bas.
3. **Passage** (*passing*, 7 et 19) : jambe libre qui passe sous le corps, pied levé.
4. **Haut** (*up*, 9 et 21) : poussée sur l'orteil arrière : corps au plus haut.
Les dessins 13–23 sont les 1–11 avec **jambes et bras inversés**. Marche **sur place** : le corps
reste sur l'axe, le pied d'appui **glisse vers l'arrière** à vitesse constante (dans le film, c'est le
décor ou le personnage entier qui avance à cette même vitesse, sinon les pieds patinent).
Mesures de l'exemple : écart des pieds 1,28 m au contact, 0,64 m au passage ; rebond de la tête
≈ 3 % de la taille.

## 5. Variantes
Le timing fait le personnage : 16 images par cycle = pressé, 32 = lent, fatigué ; un rebond fort =
léger, joyeux ; aucun rebond = robot ; buste penché en avant = détermination. La course : une phase
sans appui (les deux pieds en l'air), cycle plus court (8–16 images).
