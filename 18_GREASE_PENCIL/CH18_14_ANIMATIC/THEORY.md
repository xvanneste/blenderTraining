# CH18.14 — Cours théorique : du scénario à l'animatique

## 1. La chaîne scénario → découpage → planche → animatique
1. **Scénario** : ce qui se passe (actions, dialogues), sans caméra.
2. **Découpage technique** (CH18.12) : la scène divisée en plans, chacun avec valeur, mouvement, durée.
3. **Liste de plans** (*shot list*) : le découpage sous forme de tableau — c'est elle qui fixe le temps.
4. **Storyboard** (CH18.13) : une image (ou quelques-unes) par plan.
5. **Animatique** : les images du storyboard **montées dans le temps**, à leurs durées réelles, avec
   éventuellement des mouvements de caméra simples et du son (CH18.15).

L'animatique est le **premier film complet** : on y juge le rythme, la clarté et la durée avant de
fabriquer un seul plan définitif. Changer un plan dans l'animatique coûte des minutes ; dans la
production, des jours.

## 2. Le temps en images
À 24 images par seconde (i/s) : 1 s = 24 images, 0,5 s = 12, 3 s = 72.
Début du plan *n* = image de départ + somme des durées des plans précédents × 24 (arrondie).
Exemple « La tasse tombe » : 12 plans, 19 s = **456 images** ; SH0020 commence à l'image 73,
SH0050 à 152, le dernier (4 s) à 361. Une durée « ronde » (1,5 s) donne un nombre d'images exact ;
0,8 s = 19,2 images → arrondi à 19 : tenez la liste de plans **en images** dès que le montage se précise.

## 3. Deux façons de faire une animatique dans Blender
**a) Animatique 2D image par image (Grease Pencil).** Un objet GP face à une caméra orthographique ;
sur un calque, une **image clé par plan** (le dessin reste affiché jusqu'à l'image clé suivante). Les
**marqueurs** de la timeline portent les codes des plans. Les mouvements de caméra se simulent en
animant la caméra (Orthographic Scale = zoom, position = panoramique sur un grand dessin).
Le modèle d'application *Storyboarding* (File > New > Storyboarding) prépare un espace de travail
de ce type (keyframing automatique activé, Dope Sheet avec barre latérale).

**b) Animatique 3D (layout).** Le décor et les personnages sont des volumes simples ; on pose **une
caméra par plan** et on lie chaque caméra à un marqueur (*Bind Camera to Markers*, Ctrl+B) : à la
lecture, Blender change de caméra au passage de chaque marqueur — un montage sans logiciel de montage.
La valeur de plan s'obtient par la focale et la position (CH18.10) ; les axes respectent la règle des
180° (CH18.11).

On combine souvent les deux : storyboard 2D pour les intentions, layout 3D pour les plans difficiles
(mouvements, profondeur). L'extension tierce *Story Pencil* existe pour gérer une animatique dans le
monteur ; elle n'est **ni installée ni utilisée** dans cette formation (aucune installation sans votre
accord) : tout ce chapitre fonctionne avec Blender seul.

## 4. Les informations incrustées
Une animatique circule (réalisateur, monteur, équipe) : chaque image doit dire **quel plan** et **quelle
image**. Output Properties > *Metadata* : cochez *Marker*, *Frame* (et *Camera* en 3D), puis activez
*Burn Into Image* : ces informations sont écrites dans le rendu.

## 5. Ce que l'on juge dans une animatique
- **Durée totale** et durée de chaque plan (trop long ? trop court pour être lu ?) ;
- **Clarté** : l'histoire se comprend-elle sans explication ?
- **Continuité** de direction et de regards d'un plan à l'autre ;
- **Rythme** : alternance plans longs / courts (CH18.13), respiration avant et après les temps forts.
Ces jugements deviennent des **notes de révision** (CH18.15).
