# CH07.11 — Cours théorique : Animation faciale et lip sync

## 1. Phonèmes et visèmes
Un phonème est un son ; un **visème** est la forme de bouche qui le produit. Plusieurs phonèmes partagent un visème. Visèmes de l'exercice : **M** (bouche fermée : M, B, P), **A** (grande ouverture), **O** (lèvres arrondies), **E** (étirée, souriante).

## 2. Les cibles
M : mâchoire 0°, sourire 0. A : mâchoire −12°. O : −7°. E : −4° et ctl_smile à 0,04 m. Le sens d'ouverture de la mâchoire est celui de CH06.09 (−15° ouvre).

## 3. Synchronisation
La piste : images 1 M, 7 A, 13 O, 19 E, 25 M, 31 A, 37 E, 43 M. La forme est atteinte à l'image qui précède le son et tenue sur l'image du son (mêmes valeurs aux images f − 1 et f). Entre deux visèmes la bouche passe d'une forme à l'autre en 4 images environ (6 images entre phonèmes, moins 2 pour la forme tenue).

## 4. Continuité
Pas de saut : la mâchoire ne change jamais de plus de 6° d'une image à l'autre (maximum de la solution : 3,55°) et le sourire de plus de 30 mm (11,8 mm). Interpolation Bezier ou Linear ; jamais Constant (12° de saut, 40 mm).

## 5. Le clignement
ctl_blink : 0 → 0,05 m → 0 ; durée de 3 à 8 images ; départ vers l'image 19 : solution : départ à l'image 20, au-dessus de 5 mm pendant 3 images. Ni avant l'image 16, ni après l'image 26 dans l'exercice.

## 6. L'exercice
Fichier de départ : le visage de CH06.09 (GEO_Face, RIG_Face, shape keys pilotés par les glissières) et le texte PHONEMES. Plage 1–48 à 24 i/s ; contrôle : rotation X de jaw, position X de ctl_smile et ctl_blink.

## 7. Mesures
Solution : 35/35 ; visèmes justes ; ouvertures A, O, E : −12,0°, −7,0°, −4,0° ; saut maximal de la mâchoire 3,55° ; du sourire 11,8 mm ; clignement : maximum 50 mm, 3 images. Contre-exemples : visèmes en retard (écart jusqu'à 7,8° sur A) ; M à −4,0° ; A, O, E identiques (−12°) ; saut de 12,0° (Constant) ; aucun clignement ; clignement de 17 images.

## 8. Limites
Visage de CH06.09 : une sphère avec mâchoire, sourire et clignement ; pas de langue, de dents ni d'arrondi des lèvres ; piste de phonèmes fixe (huit) ; le correcteur mesure les contrôles, pas le rendu de la bouche.
