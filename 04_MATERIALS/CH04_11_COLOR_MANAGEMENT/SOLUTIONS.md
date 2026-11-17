# CH04.11 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — sRGB | Une image de couleur peinte ou photographiée est encodée en sRGB ; Blender la convertit en linéaire pour le calcul. |
| Q2 | **b** — Non-Color | La rugosité est un nombre : Non-Color évite toute conversion qui fausserait la valeur. |
| Q3 | **b** — Les vecteurs sont décodés avec une courbe qui les déforme : relief faux | La conversion sRGB→linéaire modifie les composantes : normales incorrectes. |
| Q4 | — | Si l'image sera VUE comme couleur (albedo, émission) : sRGB. Si ses valeurs sont des DONNÉES (rugosité, métal, normales, hauteur, masques) : Non-Color. |
| Q5 | — | Parce que l'image n'est pas une couleur : ses pixels sont lus tels quels, sans transformation. |
| Q6 | **b** — Convertir l'image linéaire de la scène en image affichable en compressant les hautes lumières | Les valeurs de la scène dépassent 1 ; le View Transform les ramène dans la plage d'affichage. |
| Q7 | **b** — La conversion d'affichage est déjà faite par le Display Device ; un gamma supplémentaire délave l'image | Un Gamma ≠ 1 ajoute une seconde courbe par-dessus celle du périphérique d'affichage. |
| Q8 | — | Standard : (1 ; 1 ; 1) — la teinte crème est perdue (écrêtage). AgX : (0,87 ; 0,85 ; 0,82) — la hauteur de la lumière est compressée et la teinte conservée. |
| Q9 | — | EXR stocke des flottants linéaires sans écrêtage ni courbe : le grade et la composition peuvent reprendre toute la dynamique ; PNG 8 bits est une livraison finale. |
| Q10 | — | Elle masque un éclairage mal réglé : on corrige la lumière dans la scène ; une exposition extrême rend le rendu fragile et incohérent entre plans. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`COMPLETED_EXAMPLES/ch04_11_color_solution.blend` (+ `_reference.png`).

**Fabrication.** Générée par script (`build_ch04_11_files.py`). Images 64 × 64 créées en réglant l'espace colorimétrique AVANT d'écrire les pixels (sinon le tampon est réinitialisé, cf. CH04.07) puis empaquetées ; View Transform AgX, Look None, Exposure 0, Gamma 1, Display Device sRGB, sortie OpenEXR 16 bits. Score 25/25 ; starter 14/25.
Rendu regardé : damier net, panneau lumineux crème tone-mappé ; deux versions (panneau coupé au bord, monde trop sombre) corrigées avant validation.
Mesure du panneau (régions de 200 × 100 px) : Standard → (1 ; 1 ; 1), AgX → (0,87 ; 0,85 ; 0,82).

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Test qui le refuse (et lui seul) |
|---|---|---|
| `…_albedo_noncolor` | albedo en Non-Color | T_Albedo |
| `…_rough_srgb` | rugosité en sRGB | T_Rough |
| `…_standard_view` | View Transform Standard | View Transform |
| `…_raw_view` | View Transform Raw | View Transform |
| `…_big_exposure` | Exposure +4 | Exposure |
| `…_gamma2` | Gamma 2,2 | Gamma |
| `…_png_master` | sortie maître PNG 8 bits | Sortie maître |
Aussi refusé : le starter (T_Rough, T_Normal, View Transform, sortie).

## Limites
- Le choix de View Transform parmi AgX, Filmic, ACES 1.3/2.0, Khronos PBR Neutral est une règle pédagogique de ce cours, pas une obligation absolue : Standard est légitime pour certains rendus plats ou publicitaires.
- Aucun contrôle de l'espace de l'écran réel ni d'un OCIO personnalisé.
- Le correcteur ne compare pas visuellement les rendus.
