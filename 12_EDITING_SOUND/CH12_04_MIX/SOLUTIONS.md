# CH12.04 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — L'énergie moyenne d'un signal sur une fenêtre | Musique à 0,3 : 0,040 ; voix : 0,137. |
| Q2 | **a** — Baisser la musique pendant la voix | Volume animé : 0,3 → 0,1 → 0,3. |
| Q3 | **a** — Des clés sur la propriété Volume du strip (I sur le champ) | Chemin d'animation : `sequence_editor.strips_all["MUSIC"].volume` (vérifié par l'API). |
| Q4 | — | Pour l'intelligibilité : mesuré, voix 8,7 fois la musique pendant la réplique ; au départ 0,9 (la musique dominait). |
| Q5 | — | Une musique constante à 0,3 : le rapport entre pendant et avant vaut 1,19 : pas de ducking ; la voix est quand même audible (2,9 ×) mais le ducking est exigé. |
| Q6 | **a** — Place le son à gauche (le canal droit est nul) | HIT : gauche 0,129, droite 0,000. |
| Q7 | **a** — Pour garder une marge avant l'écrêtage à 1,0 | hot_mix : crête 1,00 (écrêtage) ; solution 0,60. |
| Q8 | — | Dans le mixage complet on ne peut pas séparer la musique de la voix : on coupe les autres strips (mute temporaire) pour mesurer chacun. |
| Q9 | — | Non : le RMS brut n'est pas pondéré par l'oreille ; le chapitre utilise un RMS borné, pas une norme de diffusion (LUFS) : voir CH12.06. |
| Q10 | — | Sons synthétiques simples, un seul pan, un ducking par volume ; ni compresseur, ni égaliseur, ni normalisation de loudness. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch12_04_mix_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch12_04_files.py`) : trois WAV synthétiques, trois strips, volume animé ; mesures par mixdown de chaque strip seul et du mixage. Score 56/56 ; starter 14/56. Enveloppes regardées.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_no_duck` | musique constante (ducking 1,19) | ducking |
| `…_loud_music` | musique à volume 1 (RMS 0,132) | niveau de la musique ; niveau global |
| `…_no_pan` | HIT au centre (gauche = droite) | panoramique |
| `…_hot_mix` | voix et coup à 4 : crête 1,00 | niveau global ; crête |
| `…_quiet_mix` | tout trop faible (RMS 0,005) | niveaux ; niveau global |
Aussi refusé : le starter.

## Limites
- Sons synthétiques.
- RMS, pas LUFS.
- Panneau Sound non regardé.
