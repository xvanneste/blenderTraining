# CH18.12 — Cours théorique : cadrage et découpage technique

## 1. Du scénario au découpage technique
Le **découpage technique** traduit chaque scène en **plans numérotés**, avec pour chacun : valeur,
angle, mouvement, durée, action, dialogue, son. Le **storyboard** en est la version dessinée. Les
deux servent à toute l'équipe : layout, animation, lumière, montage, production (budget, planning).

## 2. La planche de storyboard normée
Une planche professionnelle comporte toujours :
| Élément | Contenu |
|---|---|
| **En-tête** | projet, séquence, numéro de page (« Page 01 »), version, date |
| **Cases** | au **format de l'image finale** (16:9, 2,39:1…), toutes identiques |
| **Code de plan** | `SQ010_SH0010` (séquence 010, plan 0010 : on numérote de 10 en 10 pour insérer des plans) |
| **Valeur et angle** | PE, PM, PA, PRT, PRP, GP, TGP, INS ; plongée / contre-plongée |
| **Mouvement** | fixe, panoramique, travelling, zoom, grue, steadicam, caméra épaule |
| **Durée** | en secondes (ou en images) |
| **Action / dialogue / son** | une ligne courte sous la case |
La norme adoptée par l'académie pour chaque note : **`SQ010_SH0020 · PM · travelling avant · 4 s`**.
Le correcteur du chapitre vérifie cette norme par expression régulière.

## 3. Les flèches
- **Flèche pleine** : mouvement d'un **personnage** ou d'un objet dans le cadre.
- **Flèche en tirets** : mouvement de **caméra** ; travelling avant = flèches des coins vers le
  centre ; arrière = du centre vers les coins ; panoramique = flèche au-dessus de la case ; grue =
  flèche verticale à côté de la case.
- Un mouvement de caméra important peut aussi se dessiner en **deux cases** (début, fin) ou avec un
  **cadre élargi** (*cadre de départ / cadre d'arrivée* dans un grand dessin).

## 4. Composer chaque case
Tout ce qui a été vu au module A s'applique (CH18.05 : tiers, valeurs, profondeur) : silhouette lisible,
3 valeurs, personnage coupé par le cadre au bon endroit (CH18.10), regards cohérents (CH18.11). Une case
se lit en **une seconde**.

## 5. Dans Blender
La planche du chapitre est un objet Grease Pencil : gabarit (calque GUIDE verrouillé), dessin
(USER_Drawing), flèches (USER_Arrows, matériau rouge), et **objets texte** (*Add → Text*, `Tab` pour
éditer) pour les annotations — un texte par case, nommé `TXT_SH0010`… L'ensemble se rend comme une
image (PDF ou PNG) et devient, au module D, une **animatique** (chaque case → un plan de la timeline).
