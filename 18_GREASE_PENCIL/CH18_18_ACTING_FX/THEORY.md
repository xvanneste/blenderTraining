# CH18.18 — Cours théorique : personnages, expressions, effets, caméra 2D

## 1. Le jeu d'acteur (*acting*) en 2D
Un personnage animé **pense** : le spectateur doit voir la pensée avant l'action. Structure d'une
réaction :
1. **Attente / état initial** tenu (on lit le personnage) ;
2. **Déclencheur** (un son, un éclair) ;
3. **Anticipation** : un petit mouvement contraire (les yeux se plissent, la tête se rentre) ;
4. **Réaction** (*take*) : écrasé (1–2 images) puis étiré (1–2 images), puis pose extrême ;
5. **Tenue** (*hold*) de la pose extrême : 12 à 30 images pour qu'elle soit lue ;
6. **Retour** (*settle*) vers une nouvelle attitude, tenue à son tour.
La réaction arrive **après** le déclencheur (1 à 6 images) : avant, elle paraît prévue ; trop tard,
le personnage paraît lent. Une pose tenue en dessin fixe peut « mourir » : on la garde vivante par un
clignement, un léger mouvement (*moving hold*).

## 2. Les expressions
Trois zones suffisent : **sourcils** (l'émotion), **yeux** (l'attention, la direction du regard),
**bouche** (l'intensité). Surprise : sourcils hauts et arqués (intérieur relevé), yeux ronds, bouche
ouverte en O, tête étirée. Anticipation/méfiance : yeux plissés, sourcils froncés. Soulagement :
paupières détendues, sourire, joues. Le **regard** (pupilles) dit où pense le personnage : il regarde
l'ampoule AVANT qu'elle n'éclate.

## 3. Les effets (*FX*) dessinés
Les effets 2D s'animent souvent **droit devant** (straight ahead) et sur leur **propre calque** :
- **éclair / impact** : très court (1 à 3 dessins en un), formes en étoile, puis disparition ;
- **fumée** : volumes qui grossissent, montent, se séparent puis se dissipent (en deux) ;
- **lignes de vitesse, poussière, étincelles**.
Un effet **finit** : une image clé vide (*Insert Blank Keyframe*) le fait disparaître, sinon le dernier
dessin reste affiché jusqu'à la fin du plan.

## 4. La caméra 2D
La caméra orthographique de la feuille peut être animée comme une caméra de banc-titre :
- **tremblement** (*camera shake*) sur un impact : positions alternées, amplitude décroissante, ~8 à
  12 images, retour exact à la position initiale ;
- **recadrage** (*Orthographic Scale*), **panoramique** sur un grand décor (CH18.14).
Le tremblement commence **sur** l'image de l'impact (± 1 image).

## 5. Construire le plan
Ordre de travail : poses du personnage (acting) → timing (feuille d'exposition, CH18.17) → effets →
caméra → vérification en boucle. Mesures de l'exemple : 15 dessins de personnage, 4 tenues, sursaut
1 image après l'éclatement, 13 dessins d'effet (3 d'éclair en un, 10 de fumée en deux), tremblement
de 8 clés sur 11 images.
