# CH18.21 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | — | C'est une hypothèse : on la contrôle avec les mêmes critères que son propre travail, et on trace le contrôle. |
| Q2 | **b** — Les droits d'auteur et l'imitation de style | Licence de chaque image, sources notées. |
| Q3 | — | Incohérences d'un dessin à l'autre (proportions, costume) : à redessiner depuis une feuille de référence unique. |
| Q4 | **b** — lire et accepter consciemment ses conditions d'usage | Confidentialité et droits. |
| Q5 | — | Outil et date, demande, ce qui est accepté, refusé ou corrigé et pourquoi, origine/droits des références. |
| Q6 | — | Code en double, plan qui franchit l'axe, durée nulle, total différent de la cible. |
| Q7 | **b** — on le lit et on le teste sur une copie | Savoir ce qu'il crée et supprime. |
| Q8 | — | Les caméras CAM_SH* et boards BOARD_SH* existants, et les marqueurs. |
| Q9 | — | Une image peut sembler juste alors que la valeur, l'image de début ou le côté de l'axe sont faux ; la mesure est objective et rapide. |
| Q10 | — | Intention, rythme, émotion, continuité, choix des cadrages et dessin final. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 1
1. `SQ040_SH0030` en double (le 4ᵉ plan) → règle : un code unique par plan.
2. 4ᵉ plan côté « dos » → règle des 180° (caméra de l'autre côté de l'axe A–B).
3. `SQ040_SH0050` à 0 s → durée impossible.
4. Total 3 + 2 + 2 + 1,5 + 0 + 2 = 10,5 s ≠ 12 s annoncés.

## Exercice 2
`COMPLETED_EXAMPLES/ch18_21_assist_solution.blend` (+ `_contact.png`) : liste corrigée (SH0040 GP B
face 1,5 s ; SH0050 TGP 1,5 s ; total 12 s), plans générés par `shot_prep.py` — focales trouvées :
PE 27 mm, PRP 57 mm (×2), GP 61 mm, TGP 88 mm, PM 39 mm ; marqueurs aux images 1, 73, 121, 169, 205,
241 ; fin 288 ; journal `AI_LOG` complet.
Contre-épreuves : starter → 2/17 ; script exécuté SANS corriger la liste → refusé (3/17 : doublon,
axe, durée nulle, total, plan non conforme, journal vide).

## Défi 1 (piste)
Dans `build()`, avant toute création : construire la liste des problèmes (mêmes tests que
`validate_ch18_21.py`) et lever une exception s'il y en a — l'outil devient « sûr par défaut ».
