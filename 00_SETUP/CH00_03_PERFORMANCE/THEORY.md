# CH00.03 — Cours théorique : performances CPU, GPU, mémoire

## 1. Le budget : la notion la plus importante de ce chapitre
Un ordinateur a des ressources **finies** : temps de calcul, mémoire vive (RAM), mémoire
graphique (VRAM), espace disque. Toute scène les consomme. En production, on ne demande
pas « est-ce que c'est beau ? » mais « est-ce que c'est beau **dans le budget** ? »
(ex. : 20 min de rendu par image maximum, 10 Go de VRAM).

**Analogie.** Une scène 3D, c'est un repas pour une tablée : la RAM est la taille de la
cuisine, la VRAM la taille du plan de travail du chef (le GPU), le CPU et le GPU sont les
cuisiniers. Si les ingrédients (géométrie, textures) ne tiennent pas sur le plan de
travail, le chef doit faire des allers-retours (ralentissement) ou abandonner (« out of
memory »).

## 2. Qui fait quoi dans Blender
| Tâche | CPU | GPU | RAM | VRAM |
|---|---|---|---|---|
| Affichage de l'interface et de la vue 3D | faible | **fort** | faible | moyen |
| Modificateurs, Geometry Nodes, déformations d'animation | **fort** (souvent 1 cœur par objet) | — (sauf *GPU Subdivision* au viewport) | moyen | — |
| Simulations (fluides, tissus, fumée) | **fort** | — | **fort** | — |
| Rendu EEVEE | faible | **fort** | moyen | **fort** |
| Rendu Cycles CPU | **fort** (tous les cœurs) | — | **fort** | — |
| Rendu Cycles GPU | faible (préparation) | **fort** | moyen | **fort** |
| Compositing, montage | moyen | moyen | **fort** | moyen |

Conséquence : un **viewport lent** ne se règle pas forcément avec un meilleur GPU ; s'il
vient de modificateurs lourds, c'est le CPU (et votre organisation de scène) qui compte.

## 3. Le backend graphique : Vulkan ou OpenGL
Le **backend** est la « langue » que Blender utilise pour parler à la carte graphique.
Depuis **Blender 5.3, Vulkan est le backend par défaut** sous Windows et Linux ; OpenGL
reste disponible.
- Où : *Preferences → System → Display Graphics → Backend* (redémarrage nécessaire).
- Quand changer : affichage corrompu, plantages au démarrage ou dans le viewport, pilote
  ancien → essayer OpenGL (`blender_startup_opengl.cmd` dans le dossier d'installation pour
  tester sans rien modifier).
- Ce que ça ne change pas : le rendu **Cycles** (qui utilise CUDA/OptiX/HIP/oneAPI).

## 4. Cycles : périphériques et mémoire
- CUDA / OptiX / HIP / oneAPI → CH00.01.
- **La scène doit tenir en VRAM** pour un rendu GPU efficace. Ce qui remplit la VRAM :
  la géométrie (faces après subdivision !), les textures (une texture 8K RGBA en 32 bits
  ≈ 1 Go), les volumes (fumée), les caches.
- Si la VRAM est insuffisante, Cycles peut utiliser la mémoire système (plus lent) ou
  échouer. Solution : optimiser la scène (§6) ou rendre sur CPU (la RAM est souvent plus
  grande que la VRAM).
- **CPU + GPU ensemble** (cocher les deux dans les préférences) : parfois plus rapide,
  parfois plus lent. Seule la mesure tranche (benchmark CH00.01).

## 5. Lire les statistiques
Barre d'état (*Interface → Status Bar → Scene Statistics*, CH00.02) ou overlay
*Statistics* de la vue 3D (menu *Overlays* → *Statistics*) :

| Indicateur | Signification | Ordre de grandeur « confortable » sur un poste comme le vôtre |
|---|---|---|
| Objects | objets (sélectionnés / total) | quelques milliers |
| Vertices / Faces / Triangles | géométrie **affichée** (niveaux viewport) | < 5–10 M triangles au viewport |
| Memory | RAM utilisée par Blender | < 50 % de la RAM |
| VRAM | mémoire graphique utilisée | < 80 % de la VRAM |

⚠️ Les statistiques montrent la géométrie **du viewport**. Une Subdivision « Levels
Viewport 1 / Render 5 » affiche peu… et rend 256 fois plus de faces (4⁴). Le script
`bcma_scene_cost.py` estime le coût **au rendu**.

## 6. Les cinq leviers d'optimisation (à connaître dès maintenant)
| Levier | Principe | Où |
|---|---|---|
| **1. Partager les données** | 200 copies d'un même galet peuvent partager **un seul** maillage (duplication liée, `Alt+D`, ou `Ctrl+L` → *Link Object Data*) : mémoire divisée, fichier plus léger | Object → Link/Transfer Data |
| **2. Subdivision raisonnable** | Chaque niveau multiplie les faces par 4. Niveau 5 = ×1024 | Modificateur *Subdivision* : Levels Viewport / Render |
| **3. Simplify** | Plafond global, sans toucher aux objets : *Max Subdivision*, limites de particules, de textures (Cycles) | Properties → Render → Simplify |
| **4. Instances** | Geometry Nodes / collections instanciées : 1 million d'arbres pour le coût de quelques-uns | Phase 5 |
| **5. Textures adaptées** | Résolution selon la taille à l'écran (2K suffit souvent) | Phase 4 et 10 |

**Mesure réelle (poste de référence, RTX 3080, OptiX, 50 %, 32 échantillons)** : la scène
lourde du chapitre (16,4 M de faces estimées) se rend en 8,1 s ; la version optimisée
(0,26 M) en 5,5 s, avec une image identique à l'œil. Le gain semble modeste ici, car une
RTX 3080 absorbe 16 M de faces, mais : (a) le fichier et la mémoire ont fondu ; (b) sur un
plan réel avec personnages, décors et textures, ces 16 M s'ajoutent à tout le reste ; (c)
multipliez par 2 000 images d'un court-métrage.

## 7. Autres réglages de performance (Preferences)
| Réglage | Où | Usage |
|---|---|---|
| GPU Subdivision | Viewport → Subdivision | Calcule la subdivision du viewport sur le GPU (laisser activé) |
| Limit Size (textures) | Viewport → Textures | Limite la taille des textures **dans le viewport** sur petite VRAM |
| Undo Memory Limit | System → Memory & Limits | Plafond de RAM pour l'historique d'annulation (0 = illimité) |
| Memory Cache Limit | System → Video Sequencer | Cache d'images du montage (phase 12) |
| Hardware Raytracing | Viewport → Quality | Ombres ray-tracées matérielles au viewport (selon GPU/backend) |

## 8. En production
- Chaque département a un **budget** (triangles par personnage, Go de textures par
  décor, minutes de rendu par image) vérifié par des scripts de contrôle (phase 13).
- Les scènes lourdes sont découpées en fichiers liés (*link*, phase 16) : on ne charge que
  ce dont on a besoin.
- Les mesures sont faites **sur la machine de rendu**, pas seulement sur le poste de l'artiste.
