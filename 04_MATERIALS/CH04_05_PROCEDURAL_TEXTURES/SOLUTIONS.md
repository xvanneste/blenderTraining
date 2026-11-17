# CH04.05 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — Elle n'a pas de résolution fixe et ne dépend pas des UV | Calculée à la volée à n'importe quelle échelle ; avec les coordonnées Object ou Generated, aucun UV n'est nécessaire. |
| Q2 | **b** — Difficile d'obtenir une apparence précise dessinée à la main (logo, usure localisée) | Pour un logo ou une usure placée à la main, on peint une image (CH04.06). |
| Q3 | **b** — Object | Object (coordonnées locales) : la texture suit l'objet sans UV. Generated est une autre option, liée à la boîte englobante. |
| Q4 | — | Les coordonnées Object sont locales : une échelle d'objet non uniforme étire la texture. Le mur est donc construit à sa taille réelle dans le maillage. |
| Q5 | — | Un visage peint, une étiquette, un logo, des taches d'usure précises : des détails que l'artiste place à la main. |
| Q6 | **b** — À faire varier la couleur d'une brique à l'autre | Elles alternent de façon pseudo-aléatoire entre briques ; Mortar colore le joint. |
| Q7 | **b** — Offset (0,5) | Offset (propriété du nœud) vaut 0,5 par défaut : les joints verticaux ne s'alignent pas d'une rangée à l'autre. |
| Q8 | — | Fac vaut 1 sur le mortier et 0 sur la brique. Activez Invert sur Bump pour obtenir des joints en creux. |
| Q9 | — | Les briques se fondent : le motif disparaît ; le correcteur exige un joint plus clair d'au moins 0,15 en luminance. |
| Q10 | — | Briques minuscules (de l'ordre du millimètre à l'écran) : aspect de bruit gris et moirage ; le correcteur exige 3–12. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
[Corrigé avec inversion](COMPLETED_EXAMPLES/ch04_05_procedural_solution.blend) · [Rendu](COMPLETED_EXAMPLES/ch04_05_procedural_reference.png) · [Contre-exemple avec joints saillants](COMPLETED_EXAMPLES/COUNTER_EXAMPLES/ch04_05_procedural_raised_mortar.blend)

**Fabrication.** Générée par script (`build_ch04_05_files.py`) avec les valeurs de THEORY.md §3–4. Score du correcteur 28/28 ; starter refusé (Brick non reliée).
Rendu regardé : mur de briques rouges, joints clairs, rangées décalées, lisible dans les deux vues. Une première version avait des briques trop petites (Scale 5) et pâles (couleurs trop claires) : recalibrée (Scale 3, couleurs plus sombres).

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Test qui le refuse |
|---|---|---|
| `…_no_bump` | pas de Bump | Bump relié à Normal (+ Height et Strength : même défaut) |
| `…_bump_unlinked` | Bump relié à Normal mais Height non alimentée | Bump : Height alimentée par la Brick (seul test en échec) |
| `…_flat_colors` | Color1 = Color2 | Color1 / Color2 : distance (seul) |
| `…_mortar_same` | Mortar de la couleur des briques | Mortar plus clair (seul) |
| `…_huge_scale` | Scale 100 | Brick Scale (seul) |
| `…_no_stagger` | Offset 0 | Offset des rangées (seul) |
Aussi refusé : le starter.

## Limites
- Réglages et liens, pas l'esthétique ; seul un Bump relié directement à Normal est reconnu (pas de Normal Map ni de Displacement ici).
- Le correcteur impose Brick [Color] directement relié à Base Color.
