# CH18.17 — Tutoriels pas à pas

## Tutoriel 1 — Appliquer une feuille d'exposition
1. Ouvrez `STARTER_FILES/ch18_17_xsheet_starter.blend` ; Text Editor : texte `XSHEET`.
2. Dope Sheet, mode *Grease Pencil* : 8 losanges aux images 1 à 8 sur `USER_Turn`.
3. Commencez par la **dernière** clé (H) : sélectionnez-la, **G**, tapez `4` (8 → 12), Entrée.
4. G : 7 → 10 (+3), F 6 → 9 (+3), E 5 → 8, D 4 → 7, C 3 → 6, B 2 → 4. A reste à 1.
5. Output Properties > *Frame Range* > *End* : 18. Lecture : comparez avec l'ancienne version.
6. Vérification : `-- --exercise xsheet`.

## Tutoriel 2 — Préparer le cycle
1. Ouvrez `STARTER_FILES/ch18_17_walk_starter.blend` (cycle 1–24, calque `USER_Walk`).
2. Object Data Properties > *Onion Skinning* > *Display* > cochez **Show Start Frame**.
3. Viewport Overlays > *Onion Skin* coché. Guides : sol, axe, hauteurs du bassin et de la tête.

## Tutoriel 3 — Les poses du premier pas
1. Image 1 — **contact** : jambe droite (proche, trait foncé) devant, talon au sol ; jambe gauche
   (lointaine, gris) derrière sur la pointe ; bras opposés. Bassin à hauteur du repère.
2. Image 7 — **passage** : jambe droite verticale sous le corps, jambe gauche pliée qui passe, pied levé.
3. Image 3 — **bas** : genou avant fléchi, tout le corps 3 à 5 cm plus bas.
4. Image 9 — **haut** : corps plus haut, pied arrière en poussée sur l'orteil.
5. Intervalles 5 et 11 : à mi-chemin, en suivant l'onion skin ; le pied d'appui recule régulièrement.
Insérer un dessin : *Draw > Animation > Insert Blank Keyframe (Active Layer)* (Shift+I), ou
*Duplicate Active Keyframe (Active Layer)* pour partir du précédent.

## Tutoriel 4 — Le second pas
1. Images 13 à 23 : mêmes poses que 1 à 11, **jambes et bras inversés** (la jambe gauche devant).
2. Lecture en boucle (Espace) : avec *Show Start Frame*, l'image 1 apparaît en onion après la 23 :
   la jonction doit être aussi fluide que le reste.
3. Types de clés (Dope Sheet, R) : contacts Keyframe, bas/passages/hauts Extreme, intervalles Breakdown.

## Tutoriel 5 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_17_walk_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch18_17.py" -- --exercise walk --render
```
Référence : `COMPLETED_EXAMPLES/ch18_17_walk_reference.png` (les 12 dessins, ligne 1 = pas droit).

## Variante de contrôle

Construisez un tableau d’exposition de deux sections, l’une régulière, l’autre avec accélération. Faites boucler les dessins et inspectez le raccord fin-début. **Preuve** Le cycle se répète sans double pose ambiguë et la cadence annoncée correspond à la lecture.
