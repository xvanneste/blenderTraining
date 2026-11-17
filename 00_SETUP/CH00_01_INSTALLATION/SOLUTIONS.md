# CH00.01 — Solutions

> ⚠️ Pour l'exercice 3, lisez cette page **après** avoir tenté seul. Le correcteur
> automatique (`validate_ch00_01.py`) vous donne déjà des pistes sans tout dévoiler.

## Quiz
| Q | Réponse | Explication |
|---|---|---|
| 1 | **b** | GNU GPL (v2 ou ultérieure). |
| 2 | **b** | La GPL couvre le logiciel, pas vos créations. Attention en revanche aux licences des assets tiers. |
| 3 | **b** | Correctif (*patch*) : corrections de bugs, pas de nouvelles fonctions. |
| 4 | **c** | 2 ans. |
| 5 | — | Elle n'est pas complètement testée : plantages possibles, et des fichiers enregistrés avec une version en développement peuvent poser problème une fois revenus sur une version stable. |
| 6 | **c** | Le zip : pas d'admin, un dossier par version. |
| 7 | — | Créer un dossier nommé `portable` à côté de `blender.exe`. |
| 8 | — | Les mises à jour automatiques peuvent changer la version en cours de projet. |
| 9 | — | *Preferences → System → Register* (bouton d'association) ou `blender -r` en ligne de commande. |
| 10 | — | `%APPDATA%\Blender Foundation\Blender\5.3\` (soit `C:\Users\<vous>\AppData\Roaming\…`), sous-dossier `config\`. |
| 11 | — | `userpref.blend` = préférences (thème, raccourcis, GPU, add-ons). `startup.blend` = scène et disposition de l'interface au démarrage / *File → New*. |
| 12 | **c** | Démarre avec les réglages d'usine, sans rien supprimer. |
| 13 | — | Le GPU doit aussi être choisi **dans la scène** : *Render → Device → GPU Compute*. |
| 14 | — | OptiX (cœurs RT) ou CUDA ; on teste OptiX en premier sur une RTX, puis on **mesure**. |
| 15 | — | Cycles charge (et parfois compile) ses *kernels* GPU au premier rendu. |
| 16 | — | Sans interface, ouvre `scene.blend`, règle la sortie sur `out/img_####` à côté du fichier, rend l'image 10 → `out/img_0010.png` (format défini dans la scène). |
| 17 | — | Faire renvoyer un code d'erreur au système si le script Python lève une exception, pour qu'un script d'automatisation détecte l'échec. |
| 18 | — | 1) Clip Start/End de la caméra · 2) visibilité au rendu (objets et collections) · 3) lumières et monde · 4) résolution (%) · 5) caméra active / numéro d'image / chemin de sortie. |
| 19 | — | L'icône appareil photo (*Disable in Renders*) de la **collection** dans l'Outliner (à afficher via le filtre de l'Outliner si elle est masquée), et l'exclusion de la collection du View Layer (case à cocher). |
| 20 | — | Il prend quelques secondes au lieu de minutes : on peut tester une hypothèse après l'autre. Le diagnostic n'a pas besoin de qualité, seulement de « noir ou pas noir ». |

## Exercice 1
Fichier de référence : `COMPLETED_EXAMPLES/ch00_01_testcard_solution.blend`
(Cycles, GPU Compute, 128 échantillons, échantillonnage adaptatif seuil 0,02, Denoise,
100 %, sortie `//renders/ch00_01_testcard_`). Rendu de référence :
`COMPLETED_EXAMPLES/ch00_01_testcard_reference_render.png`.

Point de vigilance : le starter est en **EEVEE** et, une fois passé en Cycles, Cycles
propose **4096** échantillons max par défaut : bien trop pour un test.

## Exercice 2
```powershell
$B = "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe"
& $B -b "ch00_01_testcard_prenom_v002.blend" -o "//renders/ex2_cpu_####" -f 1 -- --cycles-device CPU
& $B -b "ch00_01_testcard_prenom_v002.blend" -o "//renders/ex2_gpu_####" -f 1 -- --cycles-device OPTIX
```
Le cas CPU conserve les autres réglages et se valide avec --exercise testcard_cpu. Rejouer le rendu et rouvrir le PNG fait partie du jalon. Si les deux périphériques sont disponibles, calculez temps CPU ÷ temps GPU avec la même scène et les mêmes échantillons. La mesure historique du poste de référence donnait environ ×9.
`Ctrl+Alt+S` (*Save Incremental*) transforme `…_v001.blend` en `…_v002.blend`.

## Exercice 3 — les cinq pannes
| # | Panne | Où la voir | Correction |
|---|---|---|---|
| 1 | **Clip End** de la caméra à 0,5 m : rien n'est visible au-delà | Caméra sélectionnée → *Object Data* (icône caméra verte) → *Lens* → *Clip End* | 100 m |
| 2 | **LGT_Key** désactivée au rendu | Outliner : icône appareil photo de l'objet (activer l'affichage via le filtre ⏷ → *Restriction Toggles*) | Réactiver |
| 3 | **World** à intensité 0 | *Properties → World → Surface → Strength* | 1,0 |
| 4 | Collection **PROPS** désactivée au rendu | Outliner : icône appareil photo de la collection | Réactiver |
| 5 | **Resolution %** à 10 % | *Properties → Output → Format* | 100 % |

Ordre de diagnostic conseillé : la vue caméra (`Num 0`) en mode *Rendered* (`Z` → Rendered)
montre immédiatement que rien n'apparaît ⇒ suspect n°1 (clipping). Une fois corrigé, le
sujet reste absent ⇒ visibilité de collection. L'image reste sombre ⇒ lumières et monde.
Le rendu final est minuscule ⇒ résolution.

Fichier corrigé : `COMPLETED_EXAMPLES/ch00_01_broken_render_solution.blend`.

## Exercices de leçon (rappels)
- **L1 difficile :** oui, le film peut être vendu (GPL ≠ restriction sur les œuvres) ; chaque
  asset téléchargé doit autoriser l'usage commercial (CC0, CC-BY avec crédit… ; une licence
  *NC* — non commerciale — l'interdit). Garder la trace des licences (`ASSET_MANIFEST.json`).
- **L2 difficile :** *Preferences → System → Register* (ou `blender -r`) depuis la copie zip.
- **L3 difficile :** 1) lancer `blender --factory-startup` ; 2) renommer temporairement
  `%APPDATA%\Blender Foundation\Blender\5.3` (par ex. en `5.3_bak`) : Blender redémarre
  comme au premier lancement. Puis réimporter progressivement vos réglages.

## Défi 2 — éléments de réponse
L'accélération GPU **n'est pas constante** : à faible résolution ou faible nombre
d'échantillons, les étapes fixes (chargement de la scène, construction du BVH, transfert
vers la carte) pèsent proportionnellement plus ; plus la charge de calcul augmente, plus
l'avantage GPU se rapproche de sa valeur « pure ».
