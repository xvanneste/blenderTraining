# CH00.08 — Tutoriels pas à pas

## Tutoriel 1 — Lire le schéma du pipeline
Ouvrez `ASSETS/bcma_pipeline_diagram.svg` (navigateur web). Pour chaque boîte, trouvez la
phase de l'académie correspondante dans [CURRICULUM.md](../../CURRICULUM.md).

## Tutoriel 2 — Découper un mini-scénario en plans
Scénario (30 s) : *« Un petit robot répare seul une ampoule dans un atelier, la nuit, sous
la pluie. L'ampoule s'allume. La pluie cesse, le soleil se lève sur la ville. Le robot
sourit. »*
1. Lisez le scénario trois fois. Soulignez les **actions** et les **émotions**.
2. Pour chaque action/émotion, choisissez une valeur de plan (THEORY §6) : un lieu → EWS ;
   une action précise → MS/FS ; une émotion → CU/ECU.
3. Ouvrez `STARTER_FILES/ch00_08_shotlist_template.csv` avec LibreOffice Calc ou Excel
   (séparateur **point-virgule**, encodage **UTF-8**) ou le Bloc-notes.
4. Une ligne par plan : `sq010;sh0010;…`, numéros de 10 en 10, durée en images (24 i/s :
   48 = 2 s), valeur, mouvement de caméra, description (sans point-virgule !), personnages,
   assets, statut `board`.
5. Enregistrez en CSV (UTF-8, point-virgule) sous `ch00_08_shotlist_<prenom>.csv`.
6. Vérifiez :
```powershell
python "..\..\SCRIPTS\bcma_shotlist_check.py" "ch00_08_shotlist_<prenom>.csv" --target-seconds 30 --tolerance 3
```
✅ `RÉSULTAT : VALIDÉ`, 6 à 12 plans, ~30 s.

## Tutoriel 3 — Corriger une shot list cassée
```powershell
python "..\..\SCRIPTS\bcma_shotlist_check.py" "STARTER_FILES\ch00_08_shotlist_broken.csv"
```
Lisez chaque `✘`, corrigez le fichier (copie), relancez jusqu'à `VALIDÉ`.

## Tutoriel 4 — Tableau de suivi
Dans un tableur, créez un onglet *Suivi* : lignes = plans, colonnes = étapes (Board,
Animatique, Layout, Anim, FX, Light, Rendu, Comp), cases = statut. Ajoutez une mise en forme
conditionnelle (vert = done). Vous le réutiliserez pour le court A (phase 15).
