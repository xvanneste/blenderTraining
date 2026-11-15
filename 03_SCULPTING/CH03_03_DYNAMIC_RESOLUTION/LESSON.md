# CH03.03 — Leçons

## Leçon 1 — Voxel Remesh
**Niveau :** intermédiaire · **Durée :** 1 h · **Compétence :** C03.03.a
### A. Comprendre
Reconstruction uniforme, chevauchement obligatoire, taille de voxel. → THEORY.md §1–2.
### B. Observer
`ch03_03_remesh_reference.png` ; dans la solution, Edit Mode : quads réguliers, un seul morceau.
### C. Reproduire
Tutoriel 1 (avec l'essai raté).
### D. Pratiquer
- **Facile :** exercice 1.
### G. Évaluer
Quiz Q1–Q4 ; correcteur `--exercise remesh`.

## Leçon 2 — DynTopo et Multiresolution
**Durée :** 1 h 30 · **Compétence :** C03.03.a
### A. Comprendre
Densité locale vs niveaux de subdivision ; ce que chaque méthode détruit ou conserve. → THEORY.md §3–4.
### C. Reproduire
Tutoriels 2 et 3.
### D. Pratiquer
- **Moyen :** exercice 2.
### E. Déboguer
TROUBLESHOOTING.md (morceaux séparés, sol joint par erreur, Multires lent).
### G. Évaluer
Quiz Q5–Q8 ; correcteur `--exercise multires`.

## Leçon 3 — Choisir
**Durée :** 30 min · **Compétence :** C03.03.a
### A. Comprendre
Le flux de travail type d'un personnage. → THEORY.md §5.
### D. Pratiquer
- **Difficile :** exercice 3 ; tutoriel 4.
### F. Optimiser
Gardez une copie de chaque étape (`_v001_block`, `_v002_remesh`, `_v003_multires`) : un remesh est
irréversible, et revenir à l'étape précédente est souvent plus rapide que réparer.
### G. Évaluer
Quiz Q9–Q10 ; correcteur `--exercise decide`.
