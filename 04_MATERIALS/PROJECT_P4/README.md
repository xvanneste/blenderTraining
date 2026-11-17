# Projet de phase P4 — « La bibliothèque de matériaux »

**Phase :** 4 — UV, textures et matériaux · **Durée estimée :** 15 à 25 h · **Évalue :** C04.01 → C04.11

## Brief
Constituez une **bibliothèque de 25 matériaux cinématographiques** publiés comme **assets** dans l'Asset Browser,
rangés dans des catalogues, avec descriptions, tags, auteur, licence et aperçus, et une **planche contact** qui les
montre tous. Elle servira à habiller les décors et les personnages des phases suivantes (P2 « L'atelier », P3, courts-métrages).
Les matériaux sont **procéduraux** (aucune image) : la bibliothèque tient dans un seul `.blend` autonome.

## Livrables
1. `PROJECTS/p4_materials/p4_materials_<prenom>_v0NN.blend` : 25 matériaux marqués comme assets.
2. `PROJECTS/p4_materials/blender_assets.cats.txt` : le fichier de catalogues (écrit par Blender à l'enregistrement).
3. `PROJECTS/p4_materials/renders/p4_contact_sheet.png` : grille de sphères, ≥ 1600 px de large.
4. Une planche de 4 matériaux « avant / après » dans `PORTFOLIO/p4/` et 10 lignes : recettes, difficultés, temps.

## Contraintes techniques (vérifiées par `validate_p4.py`)
1. **≥ 25 matériaux asset**, nommés `MAT_<Catégorie>_<Nom>` (ex. `MAT_Metal_Gold`), noms uniques.
2. **≥ 5 catégories** de **≥ 3 matériaux** chacune (métal, pierre, bois, plastique, verre, organique/tissu…).
3. Chaque asset : **description**, **≥ 2 tags**, **auteur** et **licence**, un **catalogue** existant dans `blender_assets.cats.txt` ; aperçus générés (conseillé).
4. Chaque matériau : un **Principled BSDF relié à Surface**, **aucun nœud orphelin**, **≤ 30 nœuds**, **aucune image**.
5. PBR plausible : Metallic ≈ 0 ou 1 ; métaux de luminance ≥ 0,4 ; diélectriques opaques entre 0,02 et 0,9 ; verres avec Transmission Weight ≥ 0,9.
6. **Variété** : ≥ 15 matériaux avec une texture qui pilote la couleur, la rugosité ou le relief ; ≥ 20 signatures (couleur, rugosité, métal) différentes.
7. Planche contact non noire et contrastée.

## Vérification
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "PROJECTS\p4_materials\p4_materials_<prenom>_v001.blend" `
  --python-exit-code 1 --python "04_MATERIALS\PROJECT_P4\validate_p4.py" -- --debug
```
Le correcteur est testé par `python 04_MATERIALS/PROJECT_P4/test_p4.py` (référence acceptée ; huit variantes fausses refusées).

## Référence
`REFERENCE/p4_library_reference.blend` (+ `blender_assets.cats.txt`, `renders/p4_contact_sheet.png`) : 25 matériaux produits par `build_p4_reference.py`
(Metal 5, Stone 5, Wood 3, Plastic 4, Glass 3, Organic 5). Validée 58/58. **Ne la copiez pas** : construisez votre bibliothèque ;
servez-vous-en pour comparer vos rendus et vos recettes (CH04.03 à CH04.10).
Limites honnêtes : sphères en coordonnées Object (la brique forme des cercles sur une sphère : à tester sur un mur plat), plusieurs métaux paraissent pâles car l'environnement est très clair, et le correcteur ne juge pas l'esthétique.

## Grille d'évaluation (sur 100)
| Critère | Points | Comment l'évaluer |
|---|---|---|
| Contraintes techniques (score du correcteur) | 30 | Score ramené sur 30 |
| Crédibilité PBR (valeurs, métaux, diélectriques, verres, peau) | 15 | Rendus comparés à des photos |
| Variation et réalisme des textures procédurales | 15 | Gros plans, absence de répétition |
| Relief et détails (bump, displacement si utilisé) | 10 | Lumière rasante |
| Organisation de la bibliothèque (catalogues, tags, descriptions) | 10 | Asset Browser |
| Couleur (espaces, vue AgX, planche regardée) | 10 | CH04.11 |
| Performance (graphes courts, pas de doublons) | 5 | Nombre de nœuds, temps de rendu |
| Documentation (fiche, recettes, difficultés) | 5 | 10 lignes + planche |
**Phase 4 validée si ≥ 70/100** et tous les quiz de la phase ≥ 80 %.

## Conseils de méthode
1. Commencez par un matériau par famille, validez-le, puis déclinez (chêne → noyer → contreplaqué).
2. Rendez toujours une sphère ET un objet plat ; regardez avec AgX.
3. Nommez dès le départ `MAT_<Catégorie>_<Nom>` ; marquez en asset au fur et à mesure.
4. Un Node Group paramétrable pour les familles proches (bois) évite les doublons.
