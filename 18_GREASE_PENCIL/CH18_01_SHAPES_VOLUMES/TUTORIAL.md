# CH18.01 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch18_01_volumes_starter.blend`. Le texte `README_EXERCICE` (workspace
*Scripting*) récapitule les consignes. Le calque `GUIDE` est verrouillé (cadenas) : vous ne
pouvez pas l'abîmer.

## Tutoriel 1 — Préparer la feuille
1. Vue caméra : `Num 0`. Puis `Home` en vue caméra pour que le cadre remplisse la vue.
2. Cliquez `GP_Practice` dans l'Outliner, `Ctrl+Tab` → **Draw Mode**.
3. *Properties → Object Data* (icône Grease Pencil) → panneau *Layers* : cliquez **USER_Lines**
   (il devient actif, surligné).
4. Barre d'outils : outil **Draw** ; dans l'en-tête de l'outil, *Radius* ≈ 10–20 px, *Strength* 1.

## Tutoriel 2 — Échauffement : traits et ellipses (USER_Lines)
1. Dans la zone encadrée en haut à gauche, tracez 20 traits horizontaux **d'un seul geste**,
   de gauche à droite, en visant à chaque fois un point d'arrivée imaginaire.
2. Puis 10 ellipses de largeurs et d'ouvertures différentes, chacune en un geste, en
   « repassant » 2 fois sur la même ellipse si besoin (méthode du tour multiple).
3. Ne gommez pas : la répétition compte plus que la perfection.

## Tutoriel 3 — Les boîtes (USER_Boxes)
1. Calque **USER_Boxes** actif.
2. Pour chaque boîte, dans la zone du bas :
   a. Tracez l'**arête verticale avant**.
   b. Depuis ses deux extrémités, tracez des lignes **vers le point de fuite gauche** (petit
      cercle sur la ligne d'horizon, à gauche), puis vers le **point de fuite droit**.
   c. Fermez les faces latérales par deux verticales.
   d. Le dessus : depuis les coins hauts, lignes vers les points de fuite opposés ; leur
      croisement donne le coin arrière.
3. Faites 10 boîtes de proportions différentes (plates, hautes, cubiques), certaines au-dessus de
   l'horizon (on voit le dessous), d'autres en dessous (on voit le dessus).
4. Astuce : outil **Line** (barre `T`) pour des lignes parfaitement droites au début ; passez
   ensuite à main levée.

## Tutoriel 4 — Les valeurs (USER_Values)
1. Calque **USER_Values** actif. `U` → **MAT_GP_Light** (matériau à remplissage clair).
2. Dessinez un cercle fermé (outil **Circle** ou à main levée) : c'est la sphère.
3. `U` → **MAT_GP_Shadow** : dessinez la zone d'**ombre propre** (croissant du côté opposé à la
   lumière), puis l'**ombre portée** au sol (ellipse aplatie, la plus sombre au contact).
4. Variante au trait : remplissez les ombres par des **hachures** (traits parallèles) avec
   l'encre.
5. Répétez pour 3 sphères avec trois directions de lumière différentes.

## Tutoriel 5 — Vérifier et s'auto-évaluer
Enregistrez `ch18_01_volumes_<prenom>_v001.blend` (en Object Mode : `Ctrl+Tab`), puis :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_01_volumes_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch18_01.py" -- --exercise volumes --render
```
Le correcteur vérifie la **quantité et l'emplacement** du travail. La **qualité** s'évalue avec
la grille d'EXERCISES.md. Rendu `F12` de votre feuille → `PORTFOLIO/drawing/`.
Référence : `COMPLETED_EXAMPLES/ch18_01_volumes_reference.png`.

## Variante de contrôle

Tracez trois ellipses qui appartiennent à un même cylindre. Repérez l’axe et l’ouverture avant de dessiner le contour. Faites varier l’orientation du cylindre et comparez. **Preuve** Les ellipses et les arêtes lisent le même volume dans les deux vues.
