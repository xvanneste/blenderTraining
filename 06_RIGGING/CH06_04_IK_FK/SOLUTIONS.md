# CH06.04 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — FK : on tourne chaque os ; IK : on place l'extrémité et le solveur calcule les rotations | FK convient aux gestes en arc (balancement) ; IK aux contacts (main posée sur un objet, pied au sol). |
| Q2 | **a** — À choisir de quel côté le coude (ou le genou) se plie | Le pôle oriente le plan de la chaîne : coude vers le haut ou vers le bas. |
| Q3 | **a** — Deux os sont affectés (fore et son parent upper) | Le solveur remonte la hiérarchie sur le nombre d'os indiqué ; 0 = jusqu'à la racine. |
| Q4 | — | Une chaîne parfaitement droite est une singularité : le solveur ne sait pas de quel côté plier et le bras reste droit (coude à 0,0 mesuré). Une légère pré-flexion vers le pôle lève l'ambiguïté. |
| Q5 | — | Avec un étirement non nul, les os s'allongent quand la cible est hors de portée (0,29 m au lieu de 0,30 m au repos et 0,45 m en tension dans le contre-exemple) ; on garde des os de longueur constante. |
| Q6 | **a** — Un driver relie l'influence de la contrainte IK à une propriété personnalisée (ik_fk) | Influence 1 = IK, 0 = FK ; la propriété ik_fk sert d'interrupteur animable. |
| Q7 | **a** — Suivre ses rotations (tourner upper entraîne fore) et ignorer la cible | Avec l'influence à 0, la contrainte n'agit plus : seules les rotations des os comptent. |
| Q8 | — | L'influence de l'IK reste à 1 : le bras ne passe jamais en FK (le bout reste sur la cible : écart de 352 mm au lieu de 0 à l'attendu pour un FK). |
| Q9 | — | Pour vérifier que le bras se tend sans s'étirer : longueurs conservées (0,300 m) et bout à 0,59–0,60 m de l'épaule. |
| Q10 | — | Pour ne pas modifier le fichier de l'apprenant : il déplace les contrôleurs, mesure, puis restaure l'état de départ (pose, propriété ik_fk). |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`COMPLETED_EXAMPLES/ch06_04_ikfk_solution.blend` (+ `_reference.png`).

**Fabrication.** Générée par script (`build_ch06_04_files.py`) : contrainte IK (cible, pôle, Chain Length 2, Pole Angle 90° calibré par balayage), driver sur l'influence. Score du correcteur 40/40 ; starter 15/40. Mesures : voir THEORY.md §5.
Croquis comparé : pôle haut = coude en haut ; pôle bas = coude en bas ; hors de portée = bras tendu ; FK = fore suit upper et la cible est laissée de côté.

**Ce que le développement a appris** : (1) un bras parfaitement droit est une singularité (coude à 0,000 pour tous les Pole Angle essayés) : pré-flexion de 10° ; (2) la location d'un bone s'exprime dans son repère de repos (les axes d'un bone le long de X ne sont pas ceux du monde) : placer via la matrice du bone ; (3) la contrainte IK a Stretch actif par défaut, mais seul `ik_stretch` des bones compte : le test lit `ik_stretch` ; (4) le côté du coude se mesure par rapport à la droite épaule–bout, pas par z.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_no_pole` | IK sans pôle | Pôle ; bout à 85 mm de la cible ; côté du coude |
| `…_no_driver` | influence non pilotée | Driver ; FK (352 mm d'écart) |
| `…_stretch` | ik_stretch 0,1 et Stretch actif | Étirement ; longueurs ; bras tendu à 0,90 m |
| `…_chain_one` | Chain Length 1 | Chain Length ; côté du coude ; portée |
| `…_no_ik` | aucune contrainte IK | Contrainte absente et ses conséquences |
Aussi refusé : le starter.

## Limites
- Un seul bras plan, deux os ; le correcteur dépend des noms upper, fore, ik_hand, ik_pole, switch.
- Le Pole Angle dépend de l'orientation des bones.
