# Passerelles du pipeline — du scénario au montage final

Ce document décrit **ce que chaque étape reçoit, produit et transmet**, avec les
conventions de fichiers BCMA. Il est **obligatoire** pour les projets des phases 15
(courts A, B, C) et 16 (séquence pilote). Chaque étape renvoie aux chapitres qui
l'enseignent.

```
Scénario → Storyboard GP → Animatique → Layout 3D → Blocking → Animation
        → Lighting → Rendering → Compositing → Montage final
```

## 1. Scénario → Storyboard
| | |
|---|---|
| Entrée | Scénario (`01_preprod/script/<projet>_script_v001.md`), liste des séquences |
| Travail | Découper en plans, dessiner chaque plan (Grease Pencil, workspace 2D Animation ou *Storyboarding*) |
| Sortie | `01_preprod/storyboard/<projet>_board_v001.blend` : un objet GP par séquence, une **caméra par plan** nommée `CAM_sq010_sh0010`, marqueurs de timeline nommés comme les plans |
| Contrôle | Chaque plan du scénario a au moins une case ; shot list CSV à jour (`bcma_shotlist_check.py`) |
| Enseigné | CH18.10–CH18.13, CH15.02 |

## 2. Storyboard → Animatique
| | |
|---|---|
| Entrée | Fichier de board + shot list |
| Travail | Durée de chaque plan, dialogues temporaires, sons, mouvements de caméra simples, montage dans le VSE |
| Sortie | `01_preprod/animatic/<projet>_animatic_v001.blend` + export `…_animatic_v001.mp4` ; shot list mise à jour avec **les durées définitives** (colonne `duration_frames`) |
| Contrôle | Durée totale = durée visée ; projection à une personne extérieure ; notes de révision |
| Enseigné | CH18.14–CH18.15, CH12 |

## 3. Animatique → Layout 3D
| | |
|---|---|
| Entrée | Animatique validée, durées, caméras du board (CH18.20) |
| Travail | Un fichier par plan dans `03_shots/sqNNN/shNNNN/layout/` ; décors et personnages **liés** (*Link* + *Library Override*) depuis `02_assets/` ; caméra reprise du board ; plage d'images = durée de l'animatique |
| Sortie | `<projet>_sqNNN_shNNNN_layout_v001.blend` |
| Contrôle | Vue caméra = case de board ; `frame_start/frame_end` conformes ; `bcma_naming_check.py` |
| Enseigné | CH18.20, CH09.07–CH09.12, CH16.03 |

## 4. Layout → Blocking → Animation
| | |
|---|---|
| Entrée | Fichier de layout |
| Travail | Copie incrémentale en `anim/` ; poses clés (blocking, interpolation *Constant*), validation, puis *splining* et polish |
| Sortie | `…_anim_v0NN.blend` ; optionnel : cache Alembic/USD du personnage animé pour le lighting |
| Contrôle | Lecture en temps réel ; playblast : *View → Render Playblast* (libellé 5.3) comparée à l'animatique |
| Enseigné | Phase 7 |

## 5. Animation → Lighting → Rendering
| | |
|---|---|
| Entrée | Animation validée |
| Travail | Fichier `lighting/` qui **lie** l'animation (ou le cache) et le décor ; éclairage par séquence (réutilisé d'un plan à l'autre) ; view layers, passes, light groups |
| Sortie | Rendus EXR multicouches dans `03_shots/…/render/v0NN/<plan>_####.exr` |
| Contrôle | Temps/image dans le budget ; pas d'images noires (`bcma_lib.mean_luminance`) ; continuité de lumière entre plans |
| Enseigné | Phases 9, 10 |

## 6. Rendering → Compositing → Montage final
| | |
|---|---|
| Entrée | Séquences EXR |
| Travail | Compositing (Compositor) → images finales PNG/EXR ; dans le VSE de l'animatique, **remplacer plan par plan** les images du board par les images finales ; son définitif, mixage, étalonnage |
| Sortie | `06_deliveries/<projet>_master_v001.mov|mp4` + version web + sous-titres |
| Contrôle | Durée identique à l'animatique (sauf décision de montage) ; loudness ; checklist de livraison |
| Enseigné | Phases 11, 12 |

## Règles transversales
1. **La durée d'un plan est fixée par l'animatique.** Toute modification repasse par le montage.
2. **Une caméra par plan, nommée par son code** : elle voyage du board jusqu'au rendu.
3. **On lie, on ne copie pas** les assets dans les plans.
4. **Chaque étape incrémente sa version** et ne modifie jamais les fichiers de l'étape précédente.
5. **Le montage de l'animatique est le squelette du film** jusqu'à la livraison.
