# CH18.15 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | — | Dialogues temporaires, bruitages clés, musique temporaire. |
| Q2 | **c** — 83 ms | 2/24 s ≈ 83 ms : perceptible sur un impact. |
| Q3 | — | Ils fixent la durée des plans parlés ; le reste se cale ensuite. |
| Q4 | **b** — Add > Fade > Fade In and Out | Il anime Volume (son) ou l'opacité (image). |
| Q5 | — | Deux strips image/vidéo sélectionnés qui se chevauchent (sur deux canaux) ; la durée du fondu = le chevauchement. |
| Q6 | **b** — la coupe franche | Les autres transitions doivent être justifiées. |
| Q7 | — | Allonger le début du plan suivant (sur un autre canal) pour qu'il chevauche le précédent, sans déplacer sa fin. |
| Q8 | **b** — Audio Codec : No Audio | Encoding > Audio > Audio Codec doit être AAC (par exemple). |
| Q9 | — | Code du plan · numéro d'image · remarque concrète (action à faire). |
| Q10 | — | Pour comparer, revenir en arrière et savoir quelle version a reçu quelles notes. |
<!-- QUIZ_ANSWERS_END -->

## Exercices 1 à 3 (référence)
`COMPLETED_EXAMPLES/ch18_15_edit_solution.blend`, vidéo réellement exportée
`COMPLETED_EXAMPLES/ch18_15_animatic_v001.mp4` (640 × 360, 456 images, son AAC stéréo, ~0,9 Mo) et
`ch18_15_edit_contact.png` (images 140, 354 = milieu du fondu enchaîné, 446 = fondu au noir).
- Musique : canal 5, volume 0 → 0,6 (images 1–24) → 0,6 → 0 (432–456).
- Sons : `sfx_whoosh` à 152, `sfx_catch` à 205, `temp_dialogue_oh` à 133 (débuts des plans).
- SH0120 sur le canal 3, de 349 à 456 ; Crossfade canal 4, images 349–360 ; opacité 1 → 0 (432–456).
- Export : MPEG-4, H.264, AAC ; Metadata : Strip Name + Frame.
- Notes : voir le texte `REVIEW_NOTES` (4 notes, chacune dans son plan).

Contre-épreuve du correcteur : bruitage du rattrapage décalé de 6 images, audio « No Audio », note
pointant une image hors de son plan → refusé (19/28), dont une vidéo exportée sans son (RMS 0).

## Exercice 2 — justification
Ici le fondu enchaîné SH0110 → SH0120 adoucit le passage de la gêne au plan large de conclusion ; une
coupe franche est tout aussi défendable (l'action est continue, aucune ellipse de temps). Ce qui compte :
un choix motivé, pas un effet décoratif.
