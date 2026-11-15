# CH18.10 — Cours théorique : le langage cinématographique

## 1. La valeur de plan : quelle part du corps on montre
La **valeur de plan** (ou échelle de plan) indique la taille du sujet dans le cadre. On la nomme d'après
l'endroit où le **bord bas de l'image coupe le corps** (personnage de 1,75 m ; hauteurs des repères
utilisées par le correcteur du chapitre) :
| Code | Nom | Coupe / taille | Ce qu'il raconte |
|---|---|---|---|
| **PE** | Plan d'ensemble | personnage entier, petit (≤ 30 % de la hauteur d'image) | le lieu, la solitude, l'échelle |
| **PM** | Plan moyen (en pied) | personnage entier, 55–95 % de la hauteur | l'action du corps entier |
| **PA** | Plan américain | entre le genou et la mi-cuisse (0,50–0,85 m) | le personnage et son geste (western : l'étui du revolver) |
| **PRT** | Plan rapproché taille | à la taille (0,90–1,15 m) | le dialogue, les mains |
| **PRP** | Plan rapproché poitrine | à la poitrine (1,20–1,40 m) | l'écoute, l'émotion naissante |
| **GP** | Gros plan | sous le menton (1,40–1,55 m) | l'émotion, la pensée |
| **TGP** | Très gros plan | au-dessus du menton : une partie du visage | l'intensité, le détail révélateur |
| **INS** | Insert | un objet ou un détail occupe le cadre | une information (lettre, montre, arme, tasse) |
Les plans encore plus larges (*plan général*, *très grand plan d'ensemble*) montrent un paysage où le
personnage est minuscule ou absent. Règle de montage : on **varie** les valeurs ; deux plans de
même valeur sur le même sujet donnent un *jump cut*.

## 2. Les angles
- **Niveau des yeux** : neutre.
- **Plongée** : caméra au-dessus, regard vers le bas → le personnage paraît **petit, dominé, vulnérable**.
- **Contre-plongée** : caméra en dessous, regard vers le haut → **puissant, menaçant, héroïque**.
- **Vue de dessus / zénithale**, **plan débullé** (*dutch angle*, caméra penchée) : malaise, instabilité.
Le correcteur vérifie la plongée (caméra > 2,1 m, regard vers le bas) et la contre-plongée
(caméra < 1 m, regard vers le haut).

## 3. L'axe et la règle des 180°
Deux personnages qui se parlent définissent une **ligne d'action** (l'axe A–B). Toutes les caméras
d'une même scène restent **du même côté** de cette ligne : A regarde toujours vers la droite de
l'écran, B vers la gauche. Franchir l'axe sans transition inverse les directions de regard et perd le
spectateur (« saute-axe »). On peut le franchir **visiblement** : travelling qui passe l'axe, plan
neutre dans l'axe, ou nouveau repère (un personnage se déplace).
**Champ / contrechamp** : plan sur B (souvent par-dessus l'épaule de A), puis plan sur A, caméras du
même côté de l'axe.

## 4. Les focales
La **focale** (CH01.12) change la perspective, pas seulement le cadrage :
| Focale (plein format) | Effet | Usage |
|---|---|---|
| 14–24 mm | grand-angle : perspective exagérée, profondeur, déformation des visages de près | décors, action, malaise |
| 35–50 mm | proche de la vision humaine | plans « naturels », dialogue |
| 85–135 mm | téléobjectif : visages flatteurs, arrière-plan rapproché et flou | portraits, gros plans |
| 200 mm + | écrase les plans | foules, poursuites, espionnage |
Même valeur de plan à deux focales : en grand-angle on est **près** du sujet (déformation, fond large),
au téléobjectif on est **loin** (fond resserré, flou).

## 5. Du dessin à la caméra 3D
Dans le pipeline (DOCUMENTATION/PIPELINE_BRIDGES.md), chaque case de storyboard devient une
**caméra** nommée (`CAM_SQ010_SH0010`) au layout : la valeur de plan, l'angle et la focale décidés au
board se reproduisent exactement en 3D. Le chapitre fait les deux : dessiner les 8 valeurs (planche
GP) et les cadrer avec de vraies caméras (scène 3D), mesurées par le correcteur.
