# Projet de phase P10 — « Une scène optimisée, rendue en EXR multicouche »

**Phase :** 10 — Rendu et optimisation · **Durée estimée :** 25 à 40 h · **Évalue :** C10.01 → C10.07

## Brief
Vous recevez une scène lourde : un champ de 200 accessoires (rochers) qui évalue 384 000 triangles, 200 maillages différents et une texture de 4 096 pixels (64 Mo). Vous la rendez **légère** sans perdre un seul accessoire, vous réglez **Cycles** pour qu'elle reste propre à peu d'échantillons, vous la rendez en **EXR multicouche 32 bits** avec les passes utiles au compositing, et vous livrez un **rapport de temps** (avant / après, notes).

## Livrables
1. `PROJECTS/p10_optimise/p10_scene_<prenom>_v0NN.blend` : la scène optimisée (Prop_000…Prop_199, Floor, SUN, CAM).
2. `PROJECTS/p10_optimise/renders/p10_master.exr` : l'EXR multicouche.
3. `PROJECTS/p10_optimise/renders/p10_report.json` : le rapport (`before`, `after`, `notes`).
4. `PORTFOLIO/p10/` : le rapport lisible (tableau avant/après, vos 10 lignes sur ce qui a coûté, un aperçu PNG).

## Contraintes techniques (vérifiées par `validate_p10.py`)
1. **Accessoires** : au moins 200 objets dont le nom commence par `Prop` dans le rendu (instances de collection comprises).
2. **Géométrie** : au plus 5 maillages différents ; au plus 150 000 triangles évalués (un objet source n'est évalué qu'une fois) ; textures de matériaux : au plus 16 Mo effectifs (Render Properties > Simplify > Texture Limit pris en compte).
3. **Cycles** : moteur Cycles, 4 à 64 échantillons, débruitage activé, échantillonnage adaptatif activé (seuil ≤ 0,05).
4. **Qualité mesurée** : un rendu de 160 × 90 avec vos réglages (graine 0) comparé à une référence de 256 échantillons sans débruitage : EQM de la luminance ≤ 0,025.
5. **EXR** : `renders/p10_master.exr` multicouche, canal Combined en 32 bits flottants, canaux Depth.Z, Normal.X, Object Index.X, CryptoObject00.r et Combined_sun.R (un light group `sun` pour la lampe SUN), aucun codec à perte (B44, B44A, DWAA, DWAB).
6. **Rapport** : `renders/p10_report.json` avec `before` et `after` (triangles, meshes, texture_mb, seconds_per_frame) ; `after` cohérent avec la scène (triangles et Mo à 5 % près, maillages exacts) ; `after.seconds_per_frame` ≤ 0,8 × `before.seconds_per_frame` (vos mesures : non vérifiables, seule la cohérence l'est) ; `notes` : au moins 5 phrases de plus de 20 caractères.

## Vérification
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "PROJECTS\p10_optimise\p10_scene_<prenom>_v001.blend" `
  --python-exit-code 1 --python "10_RENDERING\PROJECT_P10\validate_p10.py" -- --debug
```
Le correcteur est testé par `python 10_RENDERING/PROJECT_P10/test_p10.py` : la référence est acceptée (70/70) ; dix variantes fausses sont refusées par le contrôle visé (200 maillages, Subdivision Surface sur 200 objets, texture sans limite, 4 échantillons bruts, EXR absent, EXR en 16 bits, EXR sans Cryptomatte, rapport mensonger, rapport absent, accessoires supprimés).

## Référence
`REFERENCE/p10_scene_reference.blend` (+ `renders/p10_master.exr`, `renders/p10_report.json`, `renders/p10_preview.png`) produite par `build_p10_reference.py` en **assemblant** les chapitres : instances de collection (CH10.05), Texture Limit 1024 (CH10.05), 32 échantillons + OpenImageDenoise + adaptatif 0,02 (CH10.02, CH10.03), passes Z, Normal, Object Index, Cryptomatte Object et light group sun (CH10.04), EXR multicouche 32 bits ZIP (CH10.06). Mesures de la référence (160 × 90, Cycles CPU, machine de développement) :

| | Avant | Après |
|---|---|---|
| Maillages de rochers | 200 | 1 |
| Triangles évalués | 384 000 | 1 920 |
| Textures effectives | 64 Mo | 4 Mo |
| Temps par image (160 × 90) | 2,38 s | 0,29 s |
| EQM contre 256 échantillons | — | 0,011 |

**Limites honnêtes** : les temps sont mesurés sur une machine, à très petite résolution, et ne se comparent qu'entre eux ; le correcteur ne les vérifie pas (seule leur cohérence interne est contrôlée) ; l'EQM est calculée sur une scène facile (4 échantillons bruts : 0,040 : le seuil de 0,025 les refuse mais la marge est mince) ; la lecture du contenu de pixels de l'EXR multicouche n'est pas faite (seuls les noms et types de canaux sont lus) ; l'espace colorimétrique de l'EXR n'est pas évalué ; Flamenco et le rendu en ferme ne sont pas testés (voir CH10.07).
Ne copiez pas la référence : changez la scène (autre accessoire, autre densité, éclairage d'intérieur) et justifiez vos propres seuils.

## Grille d'évaluation (sur 100)
| Critère | Points | Comment l'évaluer |
|---|---|---|
| Contraintes techniques (score du correcteur) | 30 | Score ramené sur 30 |
| Qualité visuelle à budget réduit (propreté, détail, absence de lucioles) | 20 | Comparer l'aperçu à une référence de 256 échantillons |
| Qualité de l'EXR (passes utiles, lisibilité dans le compositeur) | 15 | Ouvrir l'EXR dans le compositeur (phase 11) |
| Rapport (mesures honnêtes, notes utiles) | 20 | Lecture critique |
| Reproductibilité (commandes de rendu CH10.07) | 5 | Plan de rendu |
| Documentation (10 lignes, limites dites) | 10 | PORTFOLIO |
**Phase 10 validée si ≥ 70/100** et tous les quiz de la phase ≥ 80 %.

## Conseils de méthode
1. Mesurez d'abord (maillages, triangles, Mo) avant d'optimiser : on ne corrige que ce qu'on a compté.
2. Un changement à la fois, un rendu après chaque changement.
3. Instanciez avant de simplifier : l'instance de collection supprime le travail, pas la qualité.
4. Gardez une copie du fichier avant la limite de texture : vous pouvez avoir besoin du gros fichier pour un plan serré.
5. Écrivez le rapport pendant le travail, pas à la fin.
