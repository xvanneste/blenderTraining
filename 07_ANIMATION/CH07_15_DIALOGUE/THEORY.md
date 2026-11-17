# CH07.15 — Cours théorique : Scène dialoguée

## 1. Les étapes d'une scène
1. **Blocking** : poses clés principales, souvent en interpolation Constant ; on valide l'histoire et le timing des poses.
2. **Splining** : passage en courbes (Bezier), ajout de breakdowns entre les poses, réglage des maintiens.
3. **Polish** : overlap, follow-through, détails (clignements, souffle), nettoyage des courbes.

## 2. La scène de l'exercice
GEO_Head (sphère de 25 cm avec un nez pour lire l'orientation), lacet autour de Z, 73 images à 24 i/s. Poses : 1 neutre (0°), 13 regarde A (+40°), 25 écoute A (+40°), 37 regarde B (−30°), 49 écoute B (−30°), 61 regarde la caméra (0°), 73 maintien final (0°).

## 3. Marqueurs
beat_1 à beat_7 aux images des poses : repères pour la navigation et le montage (touche M dans la timeline).

## 4. Splining
Action FINAL (active) : mêmes poses en Bezier (poignées Auto Clamped) et trois breakdowns : image 7 (+22°), 31 (+5°), 55 (−12°). Un breakdown choisit le trajet (courbe plus rapide au début, plus lente à la fin...) sans changer les poses.

## 5. Les maintiens
Entre deux clés de même valeur (13–25, 37–49, 61–73), la courbe Auto Clamped reste plate : écarts mesurés de 0,0° aux images 19, 43, 67. Un breakdown placé dans un maintien le casse.

## 6. Mesures
Solution : 36/36 ; BLOCK : 7 clés, toutes Constant ; FINAL : 10 clés (7 poses + 3 breakdowns), toutes Bezier ; variation maximale du lacet 8,7°/image ; maintiens à 0,0° d'écart. Contre-exemples : FINAL en Constant (saut de 70°) ; aucun breakdown ; pose à 55° (écart de 13,1° au maintien) ; breakdown de 25° dans un maintien (15,0°) ; aucun marqueur ; BLOCK active (saut de 70°).

## 7. Pièges
- Splinner en détruisant le blocking (travailler dans la même action).
- Breakdown dans un maintien.
- Modifier les poses pendant le splining.
- Oublier d'activer FINAL.
- Marqueurs mal nommés.

## 8. Limites
Un objet, un canal (le lacet) ; pas de dialogue audio ni de lip sync dans cette scène (CH07.11) ; le polish est présenté, non mesuré ; le correcteur lit des clés et des valeurs, pas la justesse du jeu.
