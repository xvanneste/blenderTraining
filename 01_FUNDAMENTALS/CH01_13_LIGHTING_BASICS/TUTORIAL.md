# CH01.13 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch01_13_bust_starter.blend`. Vue caméra (`Num 0`), mode **Rendered**
(`Z` → *Rendered*) : tout est noir.

## Tutoriel 1 — La key
1. Placez le curseur 3D à l'origine (`Shift+C`), puis `Shift+A` → *Light* → **Area**.
   Renommez-la `LGT_Key` (`F2`).
2. `N` → *Location* : (−2,2 ; −2,2 ; 2,8).
3. Faites-la viser le buste : *Properties → Constraints* → *Add Object Constraint* →
   **Track To** → *Target* : `EMP_Target`. (Ou tournez-la à la main avec `R`.)
4. *Object Data* : *Power* **450 W**, *Size* **0,8 m**. Cochez **Temperature** → **4500 K**.
   ✅ Le buste apparaît, éclairé de gauche, avec un côté droit dans l'ombre.

## Tutoriel 2 — La fill
1. Dupliquez la key (`Shift+D`, `Échap`), renommez `LGT_Fill`, *Location* (2,5 ; −2 ; 1,6).
2. *Power* **70 W**, *Size* **2 m** (source plus large = plus douce), *Temperature* **7000 K**.
   ✅ Les ombres du côté droit se débouchent légèrement (rapport 450/70 ≈ 6,4).

## Tutoriel 3 — Le rim
1. `Shift+A` → *Light* → **Spot**, `LGT_Rim`, *Location* (1 ; 2,5 ; 3), contrainte Track To vers `EMP_Target`.
2. *Power* **900 W**. ✅ Un liseré lumineux souligne le haut de la tête et les oreilles.

## Tutoriel 4 — Comparer
1. Masquez au rendu chaque lumière à tour de rôle (icône appareil photo dans l'Outliner)
   pour voir sa contribution.
2. Essayez une key ponctuelle (*Point*, Radius 0,05) : ombres dures. Revenez à l'Area.

## Tutoriel 5 — Vérifier
Enregistrez `ch01_13_bust_<prenom>_v001.blend`, puis :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch01_13_bust_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch01_13.py" --python-exit-code 1 -- --exercise threepoint --render
```
Référence : `COMPLETED_EXAMPLES/ch01_13_bust_reference.png`.
