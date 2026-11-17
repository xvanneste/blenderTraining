# CH07.13 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Monter des actions comme des clips | On place, décale, répète et fond des actions sans modifier leurs clés. |
| Q2 | **a** — Une action placée sur une piste, avec début, fin, échelle et répétition | Strip Slide : images 1 à 49 avec Repeat 2. |
| Q3 | **a** — Le strip couvre 48 images (l'action joue deux fois) | Le strip passe de 1–25 à 1–49 ; X repart de 0 à l'image 25. |
| Q4 | — | Une action réutilisée reste unique : on corrige une fois et tous les strips suivent ; le NLA décale, répète, ralentit et fond sans toucher aux clés. |
| Q5 | — | Transformer l'action active en strip d'une nouvelle piste NLA ; l'objet n'a plus d'action active. |
| Q6 | **a** — Elle passe par-dessus le NLA et le masque | Contre-exemple : X(30) = 4,00 au lieu de 0,83 : l'action active écrase le montage. |
| Q7 | **a** — Le strip entre progressivement en 6 images | À l'image 16 (3 images après le début), l'influence est de 0,5 : rotation 11,25° au lieu de 22,5°. |
| Q8 | — | Elle ralentit (> 1) ou accélère (< 1) l'action : avec 0,5 le strip Spin dure 12 images (13 à 25). |
| Q9 | — | Deux strips qui se chevauchent dans le temps ne peuvent pas partager une piste ; Move et Spin agissent sur des canaux différents et se combinent. |
| Q10 | — | Le strip Move s'arrête à l'image 49 : la plage doit le couvrir. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch07_13_nla_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch07_13_files.py`) : deux actions linéaires, pistes NLA, strips (repeat, blend_in, scale). Score 39/39 ; starter 2/39. Éditeur NLA schématisé regardé.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_no_repeat` | strip Slide non répété (1 à 25) | piste Move ; position évaluée |
| `…_late_spin` | strip Spin à l'image 1 au lieu de 13 | piste Spin ; rotation ; fondu |
| `…_no_blend` | Blend In = 0 | piste Spin (valeur) ; fondu |
| `…_active_action` | l'action Slide est restée active | action active ; position évaluée |
| `…_missing_spin_track` | pas de piste Spin | pistes ; piste Spin ; rotation ; fondu |
| `…_wrong_scale` | strip Spin à l'échelle 0,5 (13 à 25) | piste Spin ; rotation ; fondu |
Aussi refusé : le starter.

## Limites
- Un objet, deux actions ; pas de blend_type ni de transitions.
- Les contre-exemples « no_repeat », « late_spin », « wrong_scale » échouent aussi sur les mesures évaluées (les strips décident des valeurs).
- Le croquis est schématique (l'éditeur NLA lui-même n'est pas rendu en arrière-plan).
