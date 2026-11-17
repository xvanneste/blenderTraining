# Projet de phase P11 — « Intégrer un élément 3D dans une prise de vue »

**Phase :** 11 — Compositing et VFX · **Durée estimée :** 30 à 45 h · **Évalue :** C11.01 → C11.10

## Brief
Vous recevez une plaque (une image de décor avec un poteau dont l'ombre tombe à droite) et un cube 3D. Vous le **posez** dans la plaque : ombre du bon côté, sol 3D invisible. Vous le **raccordez** à la plaque : même exposition, même dominante de couleur, même grain. Vous rendez l'image finale et écrivez un **rapport de contrôle qualité** chiffré. L'objet est simple volontairement : c'est la méthode qui est évaluée, pas le modèle.

## Livrables
1. `PROJECTS/p11_integration/p11_scene_<prenom>_v0NN.blend` : la scène (Cube, Floor, SUN, CAM, plaque « plate », arbre de compositing).
2. `PROJECTS/p11_integration/renders/p11_final.png` : l'image finale (320 × 180 ou un multiple entier).
3. `PROJECTS/p11_integration/renders/p11_qc.json` : le rapport (`ratio`, `cast`, `noise`, `notes`).
4. `PORTFOLIO/p11/` : l'image finale, le rapport lisible (tableau avant/après des trois critères), 10 lignes sur ce qui trahissait l'incrustation.

## Contraintes techniques (vérifiées par `validate_p11.py`)
1. **Scène** : Cube en (0, 0, 0,5), caméra en (0, −8, 3) à 75° (35 mm) et SUN de 4 W/m² inchangés ; arbre relié à Group Output, aucun nœud orphelin ; compositing activé.
2. **Intégration** (CH11.09) : cube présent dans l'image composée ; sol lointain = plaque (± 0,03 de luminance) ; ombre à DROITE du cube (≤ −0,04 par rapport à la plaque), côté gauche inchangé (± 0,03).
3. **Cohérence** (CH11.10) : luminance du dessus du cube / sol de la plaque de 0,85 à 1,15 ; dominante (rouge − bleu du dessus moins celle du sol) à ± 0,04 ; grain (bruit du cube mesuré par deux rendus à graines différentes) de 0,008 à 0,025.
4. **Image finale** : `renders/p11_final.png` (320 × 180 ou multiple entier), luminance moyenne de 0,2 à 0,8, différente de la plaque dans la boîte du cube (≥ 0,008).
5. **Rapport** : `renders/p11_qc.json` avec `ratio`, `cast`, `noise` cohérents avec les mesures du correcteur (± 0,1 ; ± 0,03 ; ± 0,01) et `notes` : au moins 5 phrases de plus de 20 caractères.

## Vérification
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "PROJECTS\p11_integration\p11_scene_<prenom>_v001.blend" `
  --python-exit-code 1 --python "11_COMPOSITING_VFX\PROJECT_P11\validate_p11.py" -- --debug
```
Le correcteur est testé par `python 11_COMPOSITING_VFX/PROJECT_P11/test_p11.py` : la référence est acceptée (79/79) ; dix variantes fausses sont refusées, chacune par le contrôle visé (sol non catcher, film opaque, soleil du mauvais côté, exposition oubliée, cube neutre, cube trop propre, image finale absente, rapport mensonger, rapport absent, cube déplacé).

## Référence
`REFERENCE/p11_scene_reference.blend` (+ `renders/p11_final.png`, `renders/p11_qc.json`) produite par `build_p11_reference.py` en **assemblant** : Floor = Shadow Catcher et film transparent (CH11.09), SUN X 50°, Z −50° (CH11.09), Alpha Over sur la plaque (CH11.07, CH11.09), Exposure −2 puis Color Balance Gain (1,3 ; 1,0 ; 0,6) sur le cube seul (CH11.06, CH11.10), 2 échantillons Cycles sans débruitage (CH11.10). Mesures de la référence : ratio 1,012 (départ non raccordé : 1,86), dominante +0,007 (départ −0,20), bruit 0,0121 (plaque 0,011), ombre à droite −0,045, côté gauche −0,001, sol lointain 0,0.
**Limites honnêtes** : plaque et cube générés (plaque plate, un seul sol, un seul poteau) : une vraie plaque a de la perspective, des reflets et du mouvement ; la caméra est calée à la main, pas issue d'un tracking (CH11.08) ; le grain est le bruit de Cycles à 2 échantillons (pas de nœud de grain trouvé en 5.3) ; les trois critères sont mesurés sur le dessus du cube et un patch de sol en valeurs affichées ; la marge sur l'ombre est mince (−0,045 pour −0,04 exigé) ; les menus de création de nœuds n'ont pas été regardés dans l'interface ; HDRI capturé, keying et matchmoving ne sont pas mobilisés par ce projet.
Ne copiez pas la référence : changez l'objet, sa position, la direction du soleil de la plaque.

## Grille d'évaluation (sur 100)
| Critère | Points | Comment l'évaluer |
|---|---|---|
| Contraintes techniques (score du correcteur) | 30 | Score ramené sur 30 |
| Crédibilité à l'œil (l'objet « tient » dans la plaque) | 25 | Faire juger l'image par un tiers sans le prévenir |
| Qualité de l'ombre (direction, densité, contact) | 15 | Comparer à l'ombre du poteau |
| Qualité du raccord (exposition, couleur, grain) | 10 | Mesures du rapport |
| Rapport (mesures honnêtes, notes utiles) | 10 | Lecture critique |
| Documentation (10 lignes, limites dites) | 10 | PORTFOLIO |
**Phase 11 validée si ≥ 70/100** et tous les quiz de la phase ≥ 80 %.

## Conseils de méthode
1. Lisez la plaque d'abord : direction et longueur des ombres, dominante de couleur, grain.
2. Posez l'objet (ombre, sol) avant de le raccorder (couleur, exposition, grain).
3. Corrigez l'objet seul, jamais l'image composée.
4. Mesurez avant et après chaque correction : on ne règle que ce qu'on a mesuré.
5. Un tiers qui ne sait pas où est l'objet est le meilleur correcteur.
