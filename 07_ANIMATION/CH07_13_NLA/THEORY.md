# CH07.13 — Cours théorique : Animation non linéaire

## 1. Actions, pistes, strips
Une **action** contient des courbes d'animation. Le **NLA** place des actions sur des **pistes** sous forme de **strips**, comme des clips vidéo : début, fin, échelle, répétition, fondu. Les pistes s'empilent de bas en haut ; plusieurs strips d'une même piste ne se chevauchent pas.

## 2. Pousser une action
**Push Down** transforme l'action active en strip d'une nouvelle piste ; l'objet n'a plus d'action active. Une action restée active s'évalue PAR-DESSUS les pistes (elle masque le montage).

## 3. Répétition
Un strip répété joue son action plusieurs fois de suite : Repeat = 2 fait passer « Slide » de 1–25 à 1–49. Les valeurs repartent de la première clé à chaque passage : X(13) = 2, X(30) = 0,83, X(37) = 2.

## 4. Décalage, échelle, fondu
Début du strip : où l'action commence dans la scène (Spin à l'image 13). Échelle : durée du strip ÷ durée de l'action (0,5 : deux fois plus rapide). **Blend In** : entrée en fondu : influence de 0 à 1 sur 6 images (influence 0,5 à l'image 16).

## 5. L'exercice
Deux actions (24 images, interpolation linéaire) : Slide (X de 0 à 4), Spin (rotation Z de 0° à 180°). Montage : piste Move (Slide, répété ×2), piste Spin (images 13 à 37, fondu de 6 images) ; plage 1–49 ; aucune action active.

## 6. Mesures
Solution : 39/39 ; X(13) = 2,00 ; X(30) = 0,833 ; X(37) = 2,00 ; rotation : 0° (13), 11,25° (16), 90° (25), 180° (37). Contre-exemples : pas de répétition (X(30) = 4,00) ; Spin à l'image 1 (90° à l'image 13) ; pas de fondu (22,5° à l'image 16) ; action active (X(30) = 4,00) ; pas de piste Spin ; échelle 0,5 (180° à l'image 25).

## 7. Pièges
- Laisser l'action active.
- Oublier la plage de la scène.
- Strips qui se chevauchent sur une même piste.
- Confondre durée du strip et durée de l'action (échelle).
- Slots (5.x) : `NlaStrips.new` assigne le slot de l'action à la création (mesuré en script) ; vérifiez-le si vous construisez les strips à la main.

## 8. Limites
Un objet, deux actions ; pas de blend_type (Add, Multiply), d'extrapolation, de strips sonores ni de transitions entre deux strips d'une même piste ; la réutilisation d'actions entre objets (slots multiples) n'est pas testée.
