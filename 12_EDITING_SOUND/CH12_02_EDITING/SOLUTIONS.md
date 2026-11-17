# CH12.02 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Une coupe entre deux plans trop semblables (même échelle, même axe) | SH3_close → SH5_close : deux gros plans de suite. |
| Q2 | **a** — Des plans de plus en plus courts augmentent la tension | 30, 24, 18, 12, 12 images. |
| Q3 | **a** — Il résout : le spectateur reprend son souffle | 28 images ≥ 2 × 12. |
| Q4 | — | Un changement net d'échelle et d'angle rend la coupe invisible ; deux plans proches donnent un saut. |
| Q5 | — | Un plan central qui s'allonge (30 images) casse l'accélération : 30, 24, 18, 30, 12. |
| Q6 | **a** — Pour marquer un passage (temps, lieu) ; la coupe sèche reste la règle | Ici un seul fondu : SH5 → SH6. |
| Q7 | **a** — SH6 sur un autre canal, en recouvrement, plus un strip Crossfade (type CROSS) aux entrées SH5 et SH6 | Add > Transition > Crossfade ; API : `strips.new_effect(type='CROSS', input1=…, input2=…)`. |
| Q8 | — | La moyenne à 50 % : (0 ; 0,5 ; 1) pour du cyan (0, 1, 1) et du bleu (0, 0, 1) : mesuré (0 ; 0,6 ; 1) avant conversion d'affichage. |
| Q9 | — | Sinon le rendu contient des images noires après le montage (no_crossfade, frame_end). |
| Q10 | — | Elle mesure des durées et des noms : pas la qualité narrative, le contenu des plans ni le son. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch12_02_editing_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch12_02_files.py`) : six strips COLOR, Crossfade ; mesures par données et rendu. Score 60/60 ; starter 17/60. Rendus regardés.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_jump_cut` | SH3_close puis SH5_close : deux gros plans de suite | faux raccord d'échelle |
| `…_slow_rhythm` | SH4 plus long que SH3 | rythme qui accélère |
| `…_no_resolution` | SH6 de 22 images (< 2 × 12) | résolution |
| `…_no_crossfade` | SH6 enchaîné sans fondu | canaux ; recouvrement ; Crossfade |
| `…_frame_end` | plage de la scène non ajustée (1–120) | plage de la scène |
Aussi refusé : le starter.

## Limites
- Plans de couleur.
- Règles d'exercice.
- Menu Transition non regardé.
