# CH18.22 — Cours théorique : conduire les projets de la phase 18

## 1. Pourquoi 7 projets
Chaque module de la phase a été validé par des exercices courts. Les projets obligatoires vérifient
que vous savez **enchaîner** les compétences sur une durée réaliste, comme en production :

| N° | Projet | Modules mobilisés | Durée indicative* |
|---|---|---|---|
| 1 | Planche de 12 cases | A, C (CH18.10–13) | 4–6 h |
| 2 | Séquence de dialogue storyboardée | C (CH18.11–12) | 4–6 h |
| 3 | Scène d'action de 30 s (board + animatique) | C, D | 8–12 h |
| 4 | Animatique complète de 1 min (son, export, révision) | D (CH18.14–15) | 10–15 h |
| 5 | Animation Grease Pencil de 15–30 s | B, E (CH18.16–18) | 20–40 h |
| 6 | Scène hybride 2D/3D | F (CH18.19–20) | 10–20 h |
| 7 | Storyboard + animatique d'un court de 3–5 min | tout | 40–80 h |

\* Estimations pour un apprenant seul, à ajuster ; elles ne sont pas des promesses.
Le projet 7 est réutilisé en phase 15 (projet B) : soignez-le.

## 2. Méthode de production (valable pour les 7)
1. **Note d'intention** (5 lignes) : ce que le spectateur doit ressentir et comprendre.
2. **Périmètre** : durée, nombre de plans, personnages, décors — réduisez avant de commencer.
3. **Jalons** : brouillon (vignettes) → version de travail → révision → version finale. Datez-les.
4. **Organisation** : un dossier par projet, nommage `projet_SQxxx_<étape>_v001.blend` (CH00.06),
   versions incrémentées, jamais d'écrasement d'une version montrée.
5. **Vérification** : à chaque jalon, le correcteur du projet (`--exercise pN`) puis la grille.
6. **Revue** : regarder en entier, noter (code · image · remarque), corriger, nouvelle version.

## 3. Ce que vérifie le correcteur, ce qu'il ne vérifie pas
Le correcteur contrôle la **structure** mesurable : nombre de cases et de plans, notes normées, durées,
présence et calage des sons, réglages d'export, notes de révision, occlusion, etc. Il ne juge pas la
**qualité artistique** (clarté, émotion, rythme ressenti, style) : c'est le rôle des grilles
d'EXERCISES.md et d'un regard extérieur. Un projet est **validé** quand les deux sont satisfaits.

## 4. Exemples techniques
Les fichiers `ch18_22_pN_*_example.blend` montrent la **structure** attendue ; ils sont construits à
partir des solutions des chapitres (contenus répétés ou rallongés) et ne sont pas des modèles
artistiques. Pour les projets 1 et 6, les solutions de CH18.13 et CH18.19 servent d'exemple.

## 5. Conventions communes
- Planches : gabarit et notes de CH18.12 (`SQnnn_SHnnnn · valeur · mouvement · durée`), objet GP
  `GP_Practice`, calques `USER_Drawing` / `USER_Arrows`, en-tête « … Page nn ».
- Animatiques GP : marqueurs nommés par plan, un dessin au début de chaque plan (CH18.14).
- Montages : Video Sequencer, texte `REVIEW_NOTES`, export MPEG-4 / H.264 / AAC (CH18.15).
- Scènes hybrides : collection `SET`, objets `GP_Character` et `GP_Decal`, passe Z (CH18.19).
- Usage d'IA : journal `AI_LOG` (CH18.21).
