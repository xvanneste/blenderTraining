# Quiz — Pipelines de rendu

1. Quel est l’avantage principal d’images numérotées ?
   - Garantir seul le rendu final
   - Éliminer les contrôles de couleur
   - Reprendre les frames manquantes

2. Que vérifier après le code de retour ?
   - Plage, fichiers, dimensions, version
   - Seulement le temps annoncé
   - Le nom du worker seul

3. Pourquoi isoler les versions ?
   - Rendre les PNG opaques
   - Éviter de mélanger des images de calculs différents
   - Modifier automatiquement le montage

4. Quel défaut explique ce résultat et quelle correction testez-vous ? « Le montage montre un mélange de contrastes après la reprise. »

## Questions ouvertes

5. Un lot de 96 images a trois blocs égaux. Le second échoue. Quels numéros locaux reprendre si le lot commence à 1 ?
6. Le lot sort en 320 × 180 à la place de 640 × 360. Pourquoi la présence des fichiers ne suffit pas ?
7. Comment justifier des poignées ?
8. Quelle preuve rend l’étape « Préparer le lot » vérifiable ?
9. Quelle preuve rend l’étape « Distinguer retour et résultat » vérifiable ?
10. Quelle preuve rend l’étape « Reprendre et publier » vérifiable ?
