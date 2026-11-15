# CH18.21 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch18_21_assist_starter.blend` et **enregistrez-le sous**
`STARTER_FILES/ch18_21_assist_<prenom>_v001.blend` (le script retrouve les outils de l'académie
à partir de cet emplacement).

## Tutoriel 1 — Auditer la proposition
1. Text Editor : texte `SHOTLIST`. Lisez l'en-tête : durée cible 12 s.
2. Pour chaque ligne, vérifiez : code unique ? valeur et sujet valides ? côté « face » (A à gauche,
   B à droite : toutes les caméras devant la table) ? durée > 0 ?
3. Additionnez les durées : 10,5 s ≠ 12 s.
4. Notez chaque problème trouvé (vous les reporterez dans AI_LOG).

## Tutoriel 2 — Corriger
1. Dans `SHOTLIST` : le 4ᵉ plan devient `SQ040_SH0040`, côté `face` ; le TGP passe à `1.5` s.
2. Vérifiez le total (12 s). Ne touchez pas au format (6 champs séparés par « ; »).

## Tutoriel 3 — Lire puis lancer le script
1. Text Editor : `shot_prep.py`. Lisez l'en-tête et la fonction `build()` : il supprime les caméras
   `CAM_SH*`, crée une caméra par plan, cherche la focale qui donne la valeur demandée, lie un marqueur,
   ajoute un board vide enfant de la caméra.
2. *Text > Run Script* (ou le bouton ▶). La console système affiche une ligne par plan.
3. Timeline : 6 marqueurs ; flèches haut/bas + vue caméra (Num 0) : vérifiez chaque cadrage.

## Tutoriel 4 — Le journal
Text Editor : `AI_LOG`. Écrivez (lignes sans « # ») : l'outil, la demande, ce que vous avez **accepté**,
ce que vous avez **refusé** ou **corrigé** et pourquoi, l'origine des éventuelles images de référence.

## Tutoriel 5 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_21_assist_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch18_21.py" --python-exit-code 1 -- --exercise assist --render
```
Référence : `COMPLETED_EXAMPLES/ch18_21_assist_contact.png` (les 6 plans générés).
