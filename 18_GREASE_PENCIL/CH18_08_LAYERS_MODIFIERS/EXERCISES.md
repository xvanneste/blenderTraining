# CH18.08 — Exercices

## Exercice 1 — Facile : les modes de fusion ⏱ 10 min
Dans la solution (copie), passez le calque SHADE successivement en *Regular*, *Multiply*, *Add*,
*Subtract*, *Hard Light*. Notez en une phrase l'effet de chacun sur le sol.

## Exercice 2 — Moyen : un titre qui s'écrit ⏱ 25 min
Nouveau fichier **2D Animation** : écrivez votre prénom à la main (calque TITLE), ajoutez **Build**
(*Mode* Sequential, *Length* 48, *Transition* Grow), puis un second **Build** en *Vanish* qui
démarre à l'image 72 (*Delay*). Ajoutez un **Noise** léger. Lecture : le titre s'écrit, tremble,
puis s'efface.

## Exercice 3 — Difficile : la pièce éclairée (SANS procédure) ⏱ 30 min
À partir du starter, sans relire les tutoriels : Thickness, Noise et Build sur LINE, Tint sur BG ;
FX_LIGHT masqué par MASK_WINDOW (masque invisible mais actif) ; SHADE en Multiply ; CLOUDS déplacé
par la transformation du calque ; aucun modificateur appliqué.
Validation : `--exercise layers --render`.

### Grille d'auto-évaluation (sur 20)
| Critère | 0 | 1 | 2 |
|---|---|---|---|
| Aucun trait redessiné ni modificateur appliqué | non | — | oui |
| Chaque modificateur limité au bon calque | non | partiel | oui |
| Thickness lisible, Noise discret | non | un des deux | oui |
| Build : le personnage se trace en 2 s | non | partiel | oui |
| Rayons visibles uniquement par la fenêtre | non | partiel | oui |
| Calque masque invisible et actif (opacité 0) | non | — | oui |
| Ombre en Multiply, semi-transparente | non | une des deux | oui |
| Nuages déplacés par le calque (objet immobile) | non | — | oui |
| Ordre de la pile cohérent | non | — | oui |
| Temps < 30 min | > 45 | 30–45 | < 30 |
**≥ 14/20** : acquis.

## Défis
- **Défi 1 :** inversez le masque (icône d'inversion) : la lumière éclaire tout **sauf** la fenêtre.
  Pourquoi est-ce utile pour une ombre de fenêtre projetée au sol ?
- **Défi 2 :** Add → Grease Pencil → **Object Line Art** sur un cube 3D : observez le modificateur
  **Line Art** créé, changez son *Line Types* et son épaisseur.

## Mini-projet — Une pièce éclairée à votre façon ⏱ 1 h 30
Dessinez votre propre intérieur (calques BG, LINE, SHADE, FX_LIGHT, MASK) : une source de lumière
(fenêtre, lampe) limitée par un masque, des ombres en Multiply, une lueur en *Add* ou un effet
**Glow**, un élément qui apparaît avec Build. Rendu F12 dans
`PORTFOLIO/drawing/ch18_08_piece_eclairee.png`.
