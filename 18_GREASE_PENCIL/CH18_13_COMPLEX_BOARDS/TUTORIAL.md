# CH18.13 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch18_13_action_starter.blend` : gabarit de 12 cases (4 × 3), calques
`USER_Drawing` et `USER_Arrows`.

## Tutoriel 1 — Écrire la séquence en 12 lignes
Avant de dessiner, écrivez 12 lignes : une action par plan, avec sa valeur et sa durée. Vérifiez :
installation (long) → déclencheur → action (courts) → réaction (GP) → résolution (long).

## Tutoriel 2 — Les vignettes rapides
1. Calque `USER_Drawing`, pinceau Pencil : en 1 minute par case, silhouettes et grandes lignes.
2. Lisez la planche de gauche à droite : l'action se comprend-elle sans texte ? Sinon, changez la
   valeur ou l'angle de la case fautive.

## Tutoriel 3 — Action et émotion
1. Poses extrêmes, lignes de vitesse (traits parallèles derrière l'objet en mouvement).
2. Gros plans de réaction : sourcils, yeux, bouche (CH18.04).
3. Calque `USER_Arrows` : flèches pleines (personnages, objets), en tirets (caméra).

## Tutoriel 4 — Les notes et le rythme
1. Douze textes `TXT_SH0010`… sous les cases (méthode de CH18.12), format
   `SQ020_SH0050 · INS · fixe · 0,5 s`.
2. Calculez la durée moyenne (≤ 2,5 s) ; gardez au moins un plan ≤ 1 s et un ≥ 3 s.
3. En-tête : `… — SQ020 — Page 01`.

## Tutoriel 5 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_13_action_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch18_13.py" -- --exercise action --render
```
Référence : `COMPLETED_EXAMPLES/ch18_13_action_reference.png`.

## Variante de contrôle

Sur la planche de douze plans, trouvez une répétition d’intention et remplacez-la par une information nouvelle ou retirez le plan. **Preuve** La scène conserve sa durée cible et le lecteur retrouve le moment du choix sans explication.
