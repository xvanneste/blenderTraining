# CH18.08 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | — | Empiler des réglages (modificateurs, masques, fusion, transformations) sans modifier les traits, pour pouvoir tout changer ensuite sans redessiner. |
| Q2 | **b** — Multiply | Multiply fonce ce qui est dessous ; Add éclaircit (lumières). |
| Q3 | — | Mettre son Opacity à 0 ; ne pas fermer son œil (un masque caché n'agit plus). |
| Q4 | — | Calque actif → Object Data → Layers → sous-panneau Masks : cocher l'en-tête, puis + et choisir le calque masque. |
| Q5 | **b** — Build | Build : Sequential/Concurrent/Additive, Grow/Shrink/Vanish. |
| Q6 | — | Panneau Influence du modificateur → Layer : LINE. |
| Q7 | **d** — Color | Color : Hue/Saturation, Opacity, Tint. |
| Q8 | — | À générer automatiquement des traits de contour à partir de la géométrie 3D (scène, collection ou objet). |
| Q9 | — | La transformation du calque CLOUDS : Layers → Transform → Translation. |
| Q10 | **b** — le résultat est figé dans les traits : on perd le réglage | Apply est destructif : on fige le résultat ; à réserver aux exports, après une copie de sécurité. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 1
*Regular* : gris opaque posé sur le sol. *Multiply* : fonce ce qui est dessous (ombre naturelle).
*Add* : éclaircit (lumière, lueur). *Subtract* : retire de la couleur (teinte froide/sombre
étrange). *Hard Light* : contraste fort, mélange de Multiply et de Screen selon la clarté.

## Exercice 3
Référence : `COMPLETED_EXAMPLES/ch18_08_layers_solution.blend`, rendus
`ch18_08_layers_reference.png` (image 60) et `ch18_08_layers_build_frame20.png` (image 20) :
- modificateurs dans l'ordre : Thickness (×2,5, Layer LINE), Noise (0,3, LINE), Tint (orange 0,2,
  BG), Build (48 images, LINE) ; effet Shadow ;
- FX_LIGHT : Use Masks + MASK_WINDOW ; MASK_WINDOW visible, Opacity 0 ;
- SHADE : Multiply, opacité 0,6 ; CLOUDS : Translation X = 2.
Le correcteur vérifie aussi que LINE contient toujours ses 18 traits d'origine (rien d'appliqué)
et que l'objet n'a pas bougé.

## Défi 1
Masque inversé : la lumière remplit tout sauf la fenêtre. Pour une **tache de lumière au sol**, on
dessine la forme de la fenêtre projetée sur un calque masque, et on utilise ce masque (non inversé)
sur un calque d'éclairage en *Add* ; l'inversion sert, elle, à créer une **zone d'ombre** autour.
