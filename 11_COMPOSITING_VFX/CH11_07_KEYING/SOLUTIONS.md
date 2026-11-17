# CH11.07 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Un masque qui sépare le sujet du fond | Sortie Matte du nœud Keying. |
| Q2 | **a** — Sa couleur est éloignée des tons de peau | Le vert ressort loin du rouge de la peau : la clé est plus propre. |
| Q3 | **a** — La couleur à retirer | Ici (0,10 ; 0,80 ; 0,15) ; avec un bleu : le fond reste (écart 0,46). |
| Q4 | — | Un détourage dur donne des bords crénelés ; le matte garde une transition d'environ 4 pixels que l'Alpha Over respecte. |
| Q5 | — | Sans keying, l'Alpha Over ne trouve pas de matte : le fond vert reste (écart 0,44). |
| Q6 | **a** — Le vert du fond qui se reflète sur le sujet | Mesurée : vert − (rouge + bleu)/2 = +0,130 sur l'anneau avant correction. |
| Q7 | **a** — Color Spill (et le nœud Keying lui-même la corrige déjà) | Chroma Matte ne la corrige pas : no_spill reste à +0,130. |
| Q8 | — | Le nœud RGB est linéaire (0,10 ; 0,20 ; 0,80) ; à l'écran il devient (0,35 ; 0,48 ; 0,91) : le correcteur convertit. |
| Q9 | — | Il est uniforme et éclairé parfaitement : un vrai écran vert est inégal, avec des plis, des ombres et des cheveux fins. |
| Q10 | — | Un sujet convexe, un anneau, quatre coins : elle ne juge ni les cheveux, ni la transparence, ni le flou de mouvement. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch11_07_keying_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch11_07_files.py`) : image greenscreen empaquetée, arbre Keying / Color Spill / Alpha Over ; mesures par rendu. Score 34/34 ; starter 18/34. Rendus regardés.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_no_key` | Alpha Over sans Keying : le fond reste vert | fond ; contamination |
| `…_wrong_key_color` | Key Color bleu au lieu de vert | fond ; contamination |
| `…_no_spill` | Chroma Matte sans correction de contamination (+0,130) | contamination |
| `…_no_background` | Keying seul : fond noir au lieu de bleu | fond remplacé |
Aussi refusé : le starter.

## Limites
- Image générée plus propre qu'une vraie.
- Sujet convexe simple.
- Cheveux et transparence non traités.
