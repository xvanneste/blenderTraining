# CURRICULUM — Blender Cinema Master Academy

> **Version du cursus :** 1.0 — novembre 2026
> **Version Blender cible :** 5.3.0 (vérifiée installée, build `02f0899d78e3`, 10/11/2026)
> **Durée totale estimée :** ~1 760 heures de pratique (estimation, pas une garantie)

Ce document est le **programme officiel** de l'académie. Il découpe la formation en
**19 phases** (0 à 18), chaque phase en **chapitres**, chaque chapitre en **leçons**, et
associe à chacun des **compétences mesurables** (codes `Cxx.yy.z`) reprises dans
[PROGRESS.md](PROGRESS.md).

## Comment lire ce programme

| Élément | Signification |
|---|---|
| `CH05.03` | Chapitre 3 de la phase 5. Dossier : `05_GEOMETRY_NODES/CH05_03_.../` |
| `L1, L2…` | Leçons du chapitre (chacune suit le modèle A→I de [TEMPLATES/LESSON_TEMPLATE.md](TEMPLATES/LESSON_TEMPLATE.md)) |
| `C05.03.a` | Compétence évaluable (cf. PROGRESS.md) |
| Niveau | D = débutant · I = intermédiaire · A = avancé · E = expert |
| ⏱ | Durée estimée du chapitre (théorie + pratique + mini-projet) |

### Règle d'or de la progression
Un chapitre est **validé** uniquement quand :
1. le quiz est réussi à **≥ 80 %** ;
2. l'exercice « difficile » est réalisé **sans tutoriel** ;
3. le mini-projet obtient **≥ 70 %** sur sa grille d'évaluation ;
4. le test de rapidité du chapitre est réussi (quand il existe).

### Répartition des heures par phase

| Phase | Titre | Niveau | Heures (est.) | Cumul |
|---|---|---|---|---|
| 0 | Préparation et installation | D | 14 | 14 |
| 1 | Fondamentaux absolus | D | 45 | 59 |
| 2 | Modélisation professionnelle | D→I | 85 | 144 |
| 3 | Sculpting et personnages | I | 95 | 239 |
| 4 | UV, textures et matériaux | I | 75 | 314 |
| 5 | Geometry Nodes | I→A | 65 | 379 |
| 6 | Rigging professionnel | I→A | 75 | 454 |
| 7 | Animation 3D | I→A | 150 | 604 |
| 8 | Physique et simulations | I→A | 60 | 664 |
| 9 | Lighting et cinématographie | I→A | 65 | 729 |
| 10 | Rendu et optimisation | A | 40 | 769 |
| 11 | Compositing et VFX | A | 60 | 829 |
| 12 | Montage, son et finition | I | 40 | 869 |
| 13 | Python et automatisation | I→A | 75 | 944 |
| 14 | IA appliquée à Blender et au cinéma | A | 60 | 1 004 |
| 15 | Réalisation de courts-métrages | A | 260 | 1 264 |
| 16 | Production de longs-métrages | E | 190 | 1 454 |
| 17 | Expertise et spécialisations | E | 200+ | 1 654+ |
| 18 | Grease Pencil : dessin 2D, storyboard, animatique, animation hybride | D→A | 110 | 1 764+ |

> ⚠️ Ces durées sont des **ordres de grandeur** issus de l'expérience pédagogique
> (débutant motivé, pratique régulière). La maîtrise réelle dépend de la régularité,
> du feedback reçu et de la quantité de projets terminés.

---

## PHASE 0 — PRÉPARATION ET INSTALLATION ⏱ 14 h · D
**But :** disposer d'un poste de travail Blender fiable, rapide, sauvegardé et organisé
comme dans un studio, et comprendre où chaque étape de la formation s'insère dans la
fabrication d'un film.

| Chapitre | Leçons | Compétences |
|---|---|---|
| **CH00.01 Installer, lancer et vérifier Blender** ⏱ 2 h | L1 Écosystème Blender (Fondation, cycles de release, LTS, licence GPL) · L2 Méthodes d'installation Windows (installeur, zip, portable, Store, Steam) · L3 Plusieurs versions côte à côte · L4 Lancement, ligne de commande et vérification GPU · L5 Rapport système automatique | C00.01.a installer/identifier sa version · C00.01.b choisir le bon mode d'installation · C00.01.c vérifier GPU/Cycles · C00.01.d lancer Blender en ligne de commande |
| **CH00.02 Préférences essentielles** ⏱ 2 h | L1 Interface, thème, échelle UI, langue · L2 Navigation (orbite autour de la sélection, zoom à la position souris, émulation pavé numérique) · L3 Édition (undo, duplication liée) · L4 Sauvegarde des préférences, réinitialisation, `--factory-startup` | C00.02.a configurer et sauvegarder ses préférences · C00.02.b restaurer une configuration d'usine |
| **CH00.03 Performances CPU, GPU, mémoire** ⏱ 2 h | L1 Comment Blender utilise CPU/GPU/RAM/VRAM · L2 Backend GPU (Vulkan/OpenGL) · L3 Périphériques Cycles (CUDA, OptiX) · L4 Benchmark maison et lecture des statistiques · L5 Limites mémoire et cache | C00.03.a choisir le périphérique de rendu · C00.03.b mesurer un temps de rendu comparatif |
| **CH00.04 Périphériques d'entrée** ⏱ 1 h | L1 Souris 3 boutons, trackpad · L2 Clavier sans pavé numérique · L3 Tablette graphique (pression) · L4 Souris 3D (NDOF) | C00.04.a configurer sa souris/tablette |
| **CH00.05 Extensions et add-ons** ⏱ 1,5 h | L1 Système d'extensions (plateforme extensions.blender.org) · L2 Accès en ligne et sécurité · L3 Installer depuis le disque · L4 Add-ons intégrés utiles | C00.05.a installer/désactiver une extension en sécurité |
| **CH00.06 Organisation de projet** ⏱ 2 h | L1 Arborescence de production · L2 Conventions de nommage · L3 Chemins relatifs · L4 Système de projet Blender 5.3 (File → Project) · L5 Bibliothèques d'assets | C00.06.a créer une arborescence conforme · C00.06.b utiliser des chemins relatifs |
| **CH00.07 Sauvegardes, récupération, versions** ⏱ 1,5 h | L1 Auto Save, fichiers `.blend1` · L2 Recover Last Session / Auto Save · L3 Incrémenter (`Ctrl+Alt+S`) · L4 Git/Git LFS et sauvegarde 3-2-1 · L5 Formats (blend, FBX, glTF, USD, Alembic, OBJ, EXR, PNG) | C00.07.a récupérer un travail perdu · C00.07.b appliquer une stratégie 3-2-1 |
| **CH00.08 Introduction au pipeline cinéma** ⏱ 2 h | L1 Préproduction / production / postproduction · L2 Départements et livrables · L3 Le plan (shot) comme unité de travail · L4 Où se place chaque phase de l'académie | C00.08.a expliquer le pipeline d'un plan |

**Projet de phase P0 :** *« Studio prêt »* — poste configuré, arborescence de projet
générée, rapport système, benchmark CPU/GPU, stratégie de sauvegarde documentée.

---

## PHASE 1 — FONDAMENTAUX ABSOLUS ⏱ 45 h · D
**But :** se déplacer, sélectionner, transformer, organiser et rendre une scène simple.

| Chapitre | Leçons | Compétences |
|---|---|---|
| CH01.01 L'interface | Zones, éditeurs, workspaces, en-têtes, barre d'outils, N-panel, menus contextuels, recherche F3 | C01.01.a nommer et réorganiser les éditeurs |
| CH01.02 Navigation 3D | Orbite/pan/zoom, vues numériques, perspective/ortho, frame selected, vues locales, fly/walk | C01.02.a naviguer sans hésitation (test chrono) |
| CH01.03 Sélection et manipulation | Clic, box, cercle, lasso, sélection active vs sélectionnée, Gizmos, G/R/S, contraintes d'axe, saisie numérique | C01.03.a transformer avec précision au clavier |
| CH01.04 Objets et meshes | Datablocks, Object vs Mesh, primitives, duplication `Shift+D` vs liée `Alt+D`, jointure/séparation | C01.04.a distinguer objet/donnée |
| CH01.05 Modes Object et Edit | Sommets, arêtes, faces, sélection en Edit, X-ray, proportional editing | C01.05.a éditer un mesh simple |
| CH01.06 Transformations avancées | Appliquer les transformations, espaces Global/Local/Normal, snapping | C01.06.a appliquer échelle et rotation à bon escient |
| CH01.07 Origines, pivots, curseur 3D | Set Origin, Pivot Point, curseur 3D, snapping du curseur | C01.07.a contrôler les pivots |
| CH01.08 Collections et Outliner | Collections, visibilité (œil, écran, appareil photo), exclusion, parentage, filtres | C01.08.a organiser une scène |
| CH01.09 Éditeur de propriétés | Onglets, datablocks, fake user, purge | C01.09.a retrouver un paramètre |
| CH01.10 Modificateurs essentiels | Pile, ordre, Mirror, Array, Bevel, Subdivision, Solidify, application | C01.10.a construire une pile non destructive |
| CH01.11 Matériaux simples | Slots, Principled BSDF (base), couleurs, assignation par face | C01.11.a créer et assigner des matériaux |
| CH01.12 Caméras | Caméra active, cadrage, focale, vue caméra, Lock Camera to View | C01.12.a cadrer un plan |
| CH01.13 Éclairage élémentaire | Point, Sun, Spot, Area, World, intensité en watts | C01.13.a éclairer une scène simple |
| CH01.14 Premiers rendus | EEVEE vs Cycles, résolution, échantillons, sortie PNG, F12, sauvegarde d'image | C01.14.a produire un rendu final propre |

**Projet P1 :** *« Nature morte »* — petite scène éclairée, cadrée et rendue (EEVEE + Cycles).

---

## PHASE 2 — MODÉLISATION PROFESSIONNELLE ⏱ 85 h · D→I

| Chapitre | Leçons | Compétences |
|---|---|---|
| CH02.01 Topologie | Quads/tris/n-gons, edge flow, pôles, densité | C02.01.a diagnostiquer une topologie |
| CH02.02 Outils polygonaux I | Extrude, Inset, Bevel, Loop Cut, Bridge, Fill | C02.02.a modéliser un prop simple |
| CH02.03 Outils polygonaux II | Knife, Bisect, Spin, Screw, Merge, Dissolve | C02.03.a découper et nettoyer |
| CH02.04 Normales | Orientation, recalculer, auto smooth / Smooth by Angle, Weighted Normal | C02.04.a corriger un ombrage |
| CH02.05 Hard Surface | Contrôle des arêtes, holding edges, bevels, chamfer, boolean propre | C02.05.a modéliser un objet mécanique |
| CH02.06 Subdivision Surface | Cage, crease, support loops | C02.06.a contrôler une subdivision |
| CH02.07 Booléens et non destructif | Boolean, ordre des modificateurs, cutters en collection | C02.07.a workflow non destructif |
| CH02.08 Modélisation organique | Blocking par volumes, box modeling, skin modifier | C02.08.a modéliser une forme organique |
| CH02.09 Retopologie | Snapping à la surface, Shrinkwrap, Poly Build, densité pour l'animation | C02.09.a retopologiser un sculpt simple |
| CH02.10 Optimisation | Decimate, LOD, nettoyage (Merge by Distance), statistiques | C02.10.a réduire un mesh sans perte visible |
| CH02.11 UV fondamentaux | Notion d'UV, seams, Unwrap, Smart UV Project, checker | C02.11.a déplier un objet simple |
| CH02.12 Modélisation pour l'animation | Boucles aux articulations, déformation, échelle réelle | C02.12.a préparer un mesh déformable |
| CH02.13 Assets réutilisables | Asset Browser, marquage, catalogues, prévisualisations, link/append | C02.13.a publier un asset |

**Projet P2 :** décor détaillé (pièce ou atelier) + collection de 10 props publiés comme assets.

---

## PHASE 3 — SCULPTING ET PERSONNAGES ⏱ 95 h · I

| Chapitre | Leçons | Compétences |
|---|---|---|
| CH03.01 Anatomie artistique | Proportions, têtes, masses, gesture | C03.01.a construire des proportions |
| CH03.02 Sculpt Mode | Brosses principales, rayon/force, symétrie, masques, Face Sets | C03.02.a sculpter un volume simple |
| CH03.03 Résolution dynamique | DynTopo, Voxel Remesh, Multiresolution | C03.03.a choisir la bonne méthode |
| CH03.04 Sculpture stylisée | Formes simples, silhouette, design | C03.04.a sculpter un buste stylisé |
| CH03.05 Sculpture réaliste | Plans, transitions, détails secondaires/tertiaires | C03.05.a sculpter un buste réaliste |
| CH03.06 Visages | Yeux, nez, bouche, oreilles, expressions de base | C03.06.a sculpter un visage |
| CH03.07 Mains et pieds | Structure, articulations | C03.07.a sculpter une main |
| CH03.08 Vêtements | Plis, tension, Cloth brush, workflow cloth sim | C03.08.a créer un vêtement |
| CH03.09 Retopologie personnage | Boucles faciales, articulations, densité | C03.09.a retopo d'un personnage |
| CH03.10 Préparation au rigging | Pose en A/T, échelle, origine, symétrie, nommage | C03.10.a livrer un perso « rig-ready » |

**Projet P3 :** personnage complet (sculpt + retopo + UV de base) destiné à l'animation.

---

## PHASE 4 — UV, TEXTURES ET MATÉRIAUX ⏱ 75 h · I

| Chapitre | Leçons | Compétences |
|---|---|---|
| CH04.01 UV Unwrapping avancé | Seams, îlots, distorsion, texel density | C04.01.a UV propres |
| CH04.02 Packing et UDIM | Pack Islands, marges, UDIM | C04.02.a packer pour la production |
| CH04.03 PBR et Principled BSDF | Albedo, metallic, roughness, specular, transmission, SSS, coat, sheen | C04.03.a matériau PBR crédible |
| CH04.04 Shader Editor | Nœuds, Node Wrangler, groupes, frames | C04.04.a lire et organiser un graphe |
| CH04.05 Textures procédurales | Noise, Voronoi, Wave, Gradient, Color Ramp, Mapping | C04.05.a matériau 100 % procédural |
| CH04.06 Texture Painting | Paint mode, stencils, couches | C04.06.a peindre une texture |
| CH04.07 Baking | Normal, AO, diffuse, high→low | C04.07.a baker un normal map |
| CH04.08 Relief | Bump, Normal Map, Displacement, adaptive subdivision | C04.08.a choisir la technique de relief |
| CH04.09 Matériaux types | Métaux, verres, bois, pierre, plastiques | C04.09.a bibliothèque de base |
| CH04.10 Matériaux de personnages | Peau (SSS), yeux, cheveux, tissus | C04.10.a peau et yeux crédibles |
| CH04.11 Gestion des couleurs | Espaces colorimétriques, AgX/Filmic/Standard, Non-Color, ACES (OCIO) | C04.11.a choisir le bon espace couleur |

**Projet P4 :** bibliothèque de 25 matériaux cinématographiques publiés dans l'Asset Browser.

---

## PHASE 5 — GEOMETRY NODES ⏱ 65 h · I→A

| Chapitre | Leçons | Compétences |
|---|---|---|
| CH05.01 Principes | Géométrie qui circule, champs, contexte, inspection | C05.01.a lire un arbre de nœuds |
| CH05.02 Géométrie procédurale | Primitives, transformations, Join, Mesh to Curve… | C05.02.a générer un objet |
| CH05.03 Instances | Instance on Points, Realize, Collection Info | C05.03.a disperser des instances |
| CH05.04 Distribution | Distribute Points on Faces, densité, masques | C05.04.a distribuer avec contrôle |
| CH05.05 Attributs | Named attributes, Store/Capture, transfert vers shader | C05.05.a piloter un shader par attribut |
| CH05.06 Paramètres et interfaces | Group inputs, panels, menus, exposition dans le modificateur | C05.06.a créer un outil paramétrable |
| CH05.07 Décors et végétation | Scattering, variations, contraintes de pente | C05.07.a générer une forêt |
| CH05.08 Architecture procédurale | Bâtiments modulaires, façades | C05.08.a générer un bâtiment |
| CH05.09 Boucles et simulation | Repeat zone, Simulation zone, For Each | C05.09.a utiliser une zone |
| CH05.10 Optimisation et outils | Performance, timings, publication en asset | C05.10.a publier un node tool |

**Projet P5 :** ville ou forêt procédurale paramétrable (seed, densité, style).

---

## PHASE 6 — RIGGING PROFESSIONNEL ⏱ 75 h · I→A

| Chapitre | Leçons | Compétences |
|---|---|---|
| CH06.01 Armatures et bones | Edit/Pose mode, roll, hiérarchie, nommage .L/.R | C06.01.a construire une armature |
| CH06.02 Contraintes | Copy Transforms, Track To, Damped Track, Child Of, Limit… | C06.02.a mécanisme par contraintes |
| CH06.03 Skinning | Automatic Weights, Weight Painting, normalisation | C06.03.a skinning propre |
| CH06.04 IK/FK | Chaînes IK, pole target, switch IK/FK | C06.04.a bras IK/FK |
| CH06.05 Rig humanoïde | Rigify (méta-rig, génération), personnalisation | C06.05.a rig humanoïde complet |
| CH06.06 Rig quadrupède | Méta-rig quadrupède, colonne, queue | C06.06.a rig quadrupède |
| CH06.07 Rig mécanique | Pistons, roues, chenilles, drivers | C06.07.a rig de véhicule |
| CH06.08 Shape Keys et drivers | Shape keys correctives, drivers | C06.08.a corrective shape keys |
| CH06.09 Rig facial | Bones vs shape keys, contrôleurs | C06.09.a rig facial simple |
| CH06.10 Contrôleurs et ergonomie | Custom shapes, bone collections, couleurs, sélecteurs | C06.10.a rig agréable pour l'animateur |
| CH06.11 Rigging avancé et réutilisation | Bendy bones, rig libraries, link/override | C06.11.a réutiliser un rig dans plusieurs plans |

**Projet P6 :** personnage de la phase 3 entièrement contrôlable (corps + visage).

---

## PHASE 7 — ANIMATION 3D ⏱ 150 h · I→A

| Chapitre | Leçons | Compétences |
|---|---|---|
| CH07.01 Les 12 principes | Squash & stretch, anticipation, staging, etc. | C07.01.a identifier les principes |
| CH07.02 Keyframes et timeline | Insertion, keying sets, auto-key, timeline | C07.02.a animer un objet |
| CH07.03 Dope Sheet et Action | Retiming, actions, slots | C07.03.a retimer une animation |
| CH07.04 Graph Editor | Courbes, interpolation, tangentes, modificateurs de F-curve | C07.04.a polir des courbes |
| CH07.05 Timing et spacing | Balle rebondissante, charge, poids | C07.05.a balle rebondissante crédible |
| CH07.06 Arcs, overlap, follow-through | Queue, pendule, antenne | C07.06.a overlap convaincant |
| CH07.07 Posing et silhouette | Ligne d'action, contrapposto | C07.07.a poses lisibles |
| CH07.08 Cycles de marche | Contact, down, passing, up | C07.08.a walk cycle |
| CH07.09 Course, saut, interactions | Run cycle, saut, pousser/tirer | C07.09.a saut crédible |
| CH07.10 Acting | Intention, sous-texte, pantomime | C07.10.a plan d'acting muet |
| CH07.11 Animation faciale et lip sync | Phonèmes/visèmes, yeux, clignements | C07.11.a lip sync de 5 s |
| CH07.12 Animation de caméra | Travelling, panoramique, handheld, rig de caméra | C07.12.a mouvement de caméra motivé |
| CH07.13 Animation non linéaire | NLA, strips, mélanges | C07.13.a réutiliser des actions |
| CH07.14 Motion capture | Import BVH/FBX, retargeting, nettoyage | C07.14.a nettoyer une mocap |
| CH07.15 Scène dialoguée | Blocking, splining, polish | C07.15.a scène dialoguée |

**Projet P7 :** scène de 15–25 s avec jeu d'acteur, dialogue et mouvements de caméra.

---

## PHASE 8 — PHYSIQUE ET SIMULATIONS ⏱ 60 h · I→A

| Chapitre | Leçons | Compétences |
|---|---|---|
| CH08.01 Rigid Bodies | Actif/passif, formes de collision, contraintes | C08.01.a effondrement |
| CH08.02 Soft Bodies | Paramètres, goal | C08.02.a objet mou |
| CH08.03 Cloth | Pin, collisions, tissus | C08.03.a drapé et vêtement |
| CH08.04 Particules et distribution | Émetteur, hair, alternatives Geometry Nodes | C08.04.a émission de particules |
| CH08.05 Fluides (Mantaflow) | Domaine, flow, effector, résolution | C08.05.a liquide simple |
| CH08.06 Fumée et feu | Gas domain, shader volume | C08.06.a feu et fumée |
| CH08.07 Destruction | Fracture (Cell Fracture), rigid bodies, débris | C08.07.a destruction |
| CH08.08 Cheveux et fourrure | Curves hair, node tools, dynamique | C08.08.a coiffure |
| CH08.09 Forces | Vent, turbulence, force fields | C08.09.a utiliser les forces |
| CH08.10 Caches et baking | Cache disque, bake, gestion du stockage | C08.10.a pipeline de cache |

**Projet P8 :** séquence d'action de 10 s mêlant au moins 3 simulations.

---

## PHASE 9 — LIGHTING ET CINÉMATOGRAPHIE ⏱ 65 h · I→A

| Chapitre | Leçons | Compétences |
|---|---|---|
| CH09.01 Théorie de la lumière | Intensité, direction, dureté, couleur, inverse-carré | C09.01.a analyser un éclairage |
| CH09.02 Trois points et variantes | Key, fill, rim, ratio | C09.02.a éclairage portrait |
| CH09.03 Naturel et HDRI | Soleil/ciel, HDRI, exposition | C09.03.a extérieur crédible |
| CH09.04 Dramatique et stylisé | Low-key, high-key, couleurs | C09.04.a éclairage d'intention |
| CH09.05 Volumétrie | Brouillard, god rays | C09.05.a atmosphère |
| CH09.06 Exposition et contraste | Exposure, Look AgX, histogrammes | C09.06.a exposer juste |
| CH09.07 Composition | Règle des tiers, lignes, masses, profondeur | C09.07.a composer un plan |
| CH09.08 Objectifs et focales | Focale, capteur, déformation de perspective | C09.08.a choisir une focale |
| CH09.09 Profondeur de champ | Ouverture, point de focus | C09.09.a DoF motivée |
| CH09.10 Mouvements et grammaire | Échelle de plans, axes, règle des 180° | C09.10.a découpage cohérent |
| CH09.11 Couleur et émotion | Palettes, color script | C09.11.a color script |
| CH09.12 Mise en scène | Blocking acteurs/caméra, continuité | C09.12.a mise en scène |

**Projet P9 :** cinq plans exprimant cinq émotions différentes (joie, peur, solitude, tension, émerveillement).

---

## PHASE 10 — RENDU ET OPTIMISATION ⏱ 40 h · A

| Chapitre | Leçons | Compétences |
|---|---|---|
| CH10.01 EEVEE en profondeur | Ray tracing, ombres, GI, volumes | C10.01.a régler EEVEE |
| CH10.02 Cycles en profondeur | Sampling adaptatif, rebonds, caustiques, light tree | C10.02.a régler Cycles |
| CH10.03 Bruit et débruitage | OpenImageDenoise, OptiX, passes de débruitage | C10.03.a débruiter sans perte |
| CH10.04 Passes, AOV, View Layers | Passes, Light groups, AOV, Cryptomatte | C10.04.a rendu multi-passes |
| CH10.05 Mémoire et optimisation | Instances, simplification, textures, LOD | C10.05.a rendre une scène lourde |
| CH10.06 EXR et couleur | OpenEXR multicouche, profondeur de bits | C10.06.a sortie EXR correcte |
| CH10.07 Rendu distribué | Ligne de commande, batch, farms (Flamenco) | C10.07.a rendre en batch |

**Projet P10 :** scène complexe optimisée, rendue en EXR multicouche, avec rapport de temps.

---

## PHASE 11 — COMPOSITING ET VFX ⏱ 60 h · A

| Chapitre | Leçons | Compétences |
|---|---|---|
| CH11.01 Compositor | Nœuds, viewer, backdrop | C11.01.a arbre de compositing |
| CH11.02 Compositing multipasse | Recomposer diffuse/glossy/…; relighting par light groups | C11.02.a recomposer un rendu |
| CH11.03 Masques et Cryptomatte | Masques, ID, Cryptomatte | C11.03.a isoler un objet |
| CH11.04 Depth, defocus, motion blur | Z pass, Defocus, Vector blur | C11.04.a effets optiques en post |
| CH11.05 Glare et effets | Glare, lens distortion, grain | C11.05.a finition optique |
| CH11.06 Color grading | Color Balance, courbes, look | C11.06.a étalonnage |
| CH11.07 Keying | Keying, nettoyage, spill | C11.07.a incrustation |
| CH11.08 Tracking et matchmoving | Movie Clip Editor, solve caméra | C11.08.a résoudre un tracking |
| CH11.09 Intégration 3D/réel | Shadow catcher, éclairage HDRI capturé, grain | C11.09.a intégrer un objet |
| CH11.10 Cohérence visuelle | Atmosphère, contrôle qualité | C11.10.a vérifier une intégration |

**Projet P11 :** intégration d'un élément 3D réaliste dans une prise de vue réelle.

---

## PHASE 12 — MONTAGE, SON ET FINITION ⏱ 40 h · I

| Chapitre | Leçons | Compétences |
|---|---|---|
| CH12.01 Video Sequencer | Strips, canaux, proxies, ripple editing (5.3) | C12.01.a monter dans le VSE |
| CH12.02 Montage narratif | Rythme, coupes, continuité, transitions | C12.02.a monter une séquence |
| CH12.03 Son | Voix, bruitages, ambiances, musique, synchronisation | C12.03.a habiller une séquence |
| CH12.04 Mixage | Niveaux, panoramique, loudness | C12.04.a mixer |
| CH12.05 Titres et sous-titres | Text strips, génériques, SRT | C12.05.a titrer |
| CH12.06 Export et livraison | Codecs, conteneurs, résolutions, OpenTimelineIO, outils complémentaires (DaVinci Resolve, Audacity/Reaper, FFmpeg) | C12.06.a livrer un master |

**Projet P12 :** séquence finalisée (image, montage, son, titres, export master + web).

---

## PHASE 13 — PYTHON ET AUTOMATISATION ⏱ 75 h · I→A

| Chapitre | Leçons | Compétences |
|---|---|---|
| CH13.01 Python pour artistes | Variables, listes, boucles, fonctions | C13.01.a écrire un script simple |
| CH13.02 L'API bpy | `bpy.data`, `bpy.context`, `bpy.ops`, console, Info editor | C13.02.a manipuler la scène |
| CH13.03 Génération d'objets et matériaux | Meshes, bmesh, nœuds par script | C13.03.a générer une scène |
| CH13.04 Collections, caméras, rendus | Automatiser la mise en place des plans | C13.04.a setup de plan automatique |
| CH13.05 Batch rendering | Ligne de commande, files d'attente | C13.05.a rendu batch |
| CH13.06 Validation | Scripts de QC (noms, échelles, textures manquantes) | C13.06.a script de QC |
| CH13.07 Opérateurs et UI | Operators, panels, properties | C13.07.a panneau personnalisé |
| CH13.08 Extensions | Manifest, packaging, distribution | C13.08.a publier une extension |
| CH13.09 Debugging et performance | Tracebacks, profiling | C13.09.a déboguer un script |

**Projet P13 :** boîte à outils de production personnalisée (extension).

---

## PHASE 14 — IA APPLIQUÉE À BLENDER ET AU CINÉMA ⏱ 60 h · A
**Principe :** l'IA accélère, l'artiste décide. Chaque workflow est documenté avec outils,
étapes, prompts, scripts, limites, gain de temps estimé et contrôle qualité. Les outils
sont **revérifiés** (disponibilité, licence, conditions d'usage) au moment de la rédaction
de chaque chapitre.

| Chapitre | Leçons | Compétences |
|---|---|---|
| CH14.01 Cadre, éthique et droits | Licences, données d'entraînement, droits d'auteur, crédits, confidentialité | C14.01.a évaluer un outil IA |
| CH14.02 IA en préproduction | Brainstorming, scénario, personnages, moodboards, storyboards, shot lists | C14.02.a dossier de préproduction |
| CH14.03 IA pour les assets | Références, textures, image-to-3D, text-to-3D, QC et retopo | C14.03.a intégrer un asset IA conforme |
| CH14.04 IA pour l'animation | Video-to-motion, retargeting, nettoyage, lip sync | C14.04.a animation assistée nettoyée |
| CH14.05 IA pour la mise en scène | Layout, variations de caméra, prévisualisation | C14.05.a previz assistée |
| CH14.06 Claude Code et Blender | Génération de scripts, outils, tests, diagnostic, MCP Blender | C14.06.a outil généré et testé |
| CH14.07 Pipeline hybride | Idée → scène, cohérence artistique, coûts, fiabilité | C14.07.a pipeline hybride documenté |

**Projet P14 :** scène cinématographique complète via un pipeline hybride IA + Blender, avec journal des gains et des limites.

---

## PHASE 15 — RÉALISATION DE COURTS-MÉTRAGES ⏱ 260 h · A

| Chapitre | Leçons |
|---|---|
| CH15.01 De l'idée au scénario | Logline, structure, personnages |
| CH15.02 Storyboard et animatique | Storyboard, Grease Pencil, animatique sonore |
| CH15.03 Direction artistique | Style, color script, bibles |
| CH15.04 Planification | Asset list, shot list, planning, budget en heures |
| CH15.05 Fabrication | Layout → blocking → animation → lighting → rendu |
| CH15.06 Finition | Compositing, son, montage, étalonnage, export |

> **Pipeline obligatoire** : chaque court suit la chaîne Scénario → Storyboard GP →
> Animatique → Layout → Blocking → Animation → Lighting → Rendu → Compositing → Montage
> (voir *Passerelles du pipeline*). La phase 18 (modules A–D) est un prérequis.

**Projet A :** court de 15–30 s (≈ 40 h). **Projet B :** 1–3 min (≈ 90 h).
**Projet C :** 5–10 min (≈ 130 h+, à ajuster selon le style). Chaque projet a ses jalons,
livrables, critères qualité et budget (détails dans `15_SHORT_FILMS/`).

---

## PHASE 16 — PRODUCTION DE LONGS-MÉTRAGES ⏱ 190 h · E

| Chapitre | Leçons |
|---|---|
| CH16.01 Développement d'un film | Scénario long, bible, animatique complète |
| CH16.02 Séquences et plans | Découpage, codification, shot tracking |
| CH16.03 Asset management | Versioning, nommage, dépendances, linking, library overrides |
| CH16.04 Pipelines de rendu | Farms, gestion des versions de rendu, QC |
| CH16.05 Équipes et départements | Rôles, revues, retours (notes), outils de suivi |
| CH16.06 Budget, planning, risques | Estimation de charge, chemins critiques, plans B |
| CH16.07 Solo vs indé vs studio | Arbitrages réalistes qualité / durée / budget / ressources |
| CH16.08 Livraison | Masters, sous-titres, archives |

> **Pipeline obligatoire** : la séquence pilote est produite selon les *Passerelles du
> pipeline*, avec storyboard et animatique Grease Pencil validés avant tout layout 3D.

**Projet final :** pipeline d'un long-métrage de 70–100 min, bible de production complète, séquence pilote de 2–5 min.
> Un long-métrage de qualité studio mobilise habituellement des dizaines à des centaines
> de personnes pendant plusieurs années. Cette phase enseigne comment **concevoir** et
> **piloter** un tel projet, et comment réduire l'ambition (style, durée, équipe) pour le
> rendre faisable.

---

## PHASE 17 — EXPERTISE ET SPÉCIALISATIONS ⏱ 200 h+ · E
Parcours au choix (chacun ≈ 40–80 h). Chaque parcours contient études de cas, projets
complexes, exercices de résolution de problèmes et optimisation avancée.

| Chapitre | Contenu | Compétences |
|---|---|---|
| CH17.01 Character Artist | Sculpt avancé, cheveux, vêtements, présentation turntable | C17.01.a personnage portfolio |
| CH17.02 Environment Artist | Kits modulaires, scattering, storytelling environnemental, optimisation | C17.02.a environnement portfolio |
| CH17.03 Technical Artist | Shaders avancés, Geometry Nodes outils, performance | C17.03.a outil technique |
| CH17.04 Animator | Acting avancé, body mechanics, reel | C17.04.a reel d'animation |
| CH17.05 Lighting Artist | Lighting par séquence, look dev, continuité | C17.05.a séquence éclairée |
| CH17.06 VFX Artist | Simulations complexes, intégration, FX pipeline | C17.06.a plan VFX |
| CH17.07 Technical Director | Rigs de production, résolution de problèmes, outils | C17.07.a diagnostic de production |
| CH17.08 Pipeline Developer | Outils Python, asset management, automatisation à l'échelle | C17.08.a mini-pipeline |
| CH17.09 CG Supervisor | Revue technique, standards, planification, qualité | C17.09.a plan de supervision |
| CH17.10 Réalisateur d'animation | Vision, direction d'équipe, notes, présentation d'un projet | C17.10.a dossier de réalisation |
---

## PHASE 18 — GREASE PENCIL : DESSIN 2D, STORYBOARD, ANIMATIQUE ET ANIMATION HYBRIDE ⏱ 110 h · D→A
**But :** savoir dessiner suffisamment (même en partant de zéro) pour storyboarder,
construire des animatiques, animer en 2D et marier 2D et 3D. **Phase transversale** :
les modules A–D se suivent idéalement **en parallèle des phases 1 à 9** (voir ROADMAP) et
sont **obligatoires avant la phase 15**.

| Chapitre | Module | Leçons | Compétences |
|---|---|---|---|
| CH18.01 Formes et volumes | A | Formes primaires, construction en volumes, ombre propre/portée, exercices quotidiens | C18.01.a construire un objet en volumes |
| CH18.02 Perspective | A | Ligne d'horizon, points de fuite 1/2/3, perspective atmosphérique, focales | C18.02.a dessiner un décor en perspective |
| CH18.03 Proportions, silhouettes, gestuelle | A | Mannequin, ligne d'action, silhouettes lisibles, poses | C18.03.a croquis gestuel en 30 s |
| CH18.04 Expressions et personnages | A | Construction de la tête, 6 émotions de base, feuilles de modèle (model sheets) | C18.04.a model sheet d'un personnage |
| CH18.05 Composition et dessin cinématographique | A | Cadre, tiers, lignes directrices, valeurs, décors en 3 plans | C18.05.a vignette lisible en 3 valeurs |
| CH18.06 Grease Pencil : interface et objets | B | Objet GP, modes (Object/Draw/Edit/Sculpt/Weight), workspace 2D Animation, placement des traits | C18.06.a créer et organiser un objet GP |
| CH18.07 Brushes, traits, remplissages, matériaux | B | Brushes, pression, matériaux Stroke/Fill, outil Fill, gomme | C18.07.a dessin propre trait + aplat |
| CH18.08 Calques, modificateurs, transformations | B | Layers, masques, ordre, modificateurs (Noise, Thickness, Tint, Build, Line Art…) | C18.08.a dessin multi-calques non destructif |
| CH18.09 Dessin dans l'espace 3D et organisation | B | Canvas, plans de dessin, Stroke Placement, images de référence, scènes, optimisation | C18.09.a décor dessiné en profondeur |
| CH18.10 Langage cinématographique | C | Valeurs de plans, angles, axes, règle des 180°, focales | C18.10.a nommer et dessiner 8 valeurs de plans |
| CH18.11 Continuité et dialogue | C | Champ/contrechamp, direction des regards, entrées/sorties de champ, raccords | C18.11.a découpage de dialogue sans faux raccord |
| CH18.12 Cadrage, composition, découpage technique | C | Cadres, mouvements, flèches, annotations, numérotation, gabarit de planche | C18.12.a planche de storyboard normée |
| CH18.13 Storyboards d'action, d'émotion, complexes | C | Clarté de l'action, rythme, plans émotionnels, séquences multi-personnages | C18.13.a storyboard d'action lisible |
| CH18.14 Du scénario à l'animatique | D | Découpage, liste de plans, durées, Story Pencil / marqueurs, caméras multiples | C18.14.a animatique image par image |
| CH18.15 Son, rythme, transitions, export, révision | D | Dialogues temporaires, sync, rythme, transitions, export, notes de révision | C18.15.a animatique sonore exportée |
| CH18.16 Animation 2D : principes et image par image | E | Keyframes GP, onion skinning, poses clés, intervalles | C18.16.a balle rebondissante 2D |
| CH18.17 Timing, spacing, cycles | E | Feuilles d'exposition, doubles/simples images, cycles de marche 2D | C18.17.a cycle de marche 2D |
| CH18.18 Personnages, expressions, effets, caméra | E | Acting 2D, expressions, effets (fumée, éclairs, impacts), caméra 2D | C18.18.a plan animé de 5 s |
| CH18.19 Dessiner dans et sur la 3D | F | Dessiner sur des surfaces, perspective 3D de référence, Line Art, personnages 2D dans décors 3D | C18.19.a personnage 2D dans un décor 3D |
| CH18.20 Workflow 2D → 3D | F | Storyboard dans le décor 3D, réutilisation des caméras, blocking 3D à partir du board, styles hybrides | C18.20.a caméras de board réutilisées en layout |
| CH18.21 IA pour le storyboard | G | Références, propositions de cadrage, model sheets assistées, scripts de préparation de plans, cohérence et continuité | C18.21.a storyboard assisté contrôlé |
| CH18.22 Projets de la phase | — | Les 7 projets obligatoires (voir ci-dessous) | — |

**Projets obligatoires :** 1) planche de 12 cases · 2) séquence de dialogue storyboardée ·
3) scène d'action de 30 s · 4) animatique complète de 1 min · 5) animation Grease Pencil de
15–30 s · 6) scène hybride 2D/3D · 7) storyboard + animatique d'un court de 3–5 min
(réutilisé en phase 15, projet B).

---

## PASSERELLES DU PIPELINE (obligatoires en phases 15 et 16)
```
Scénario → Storyboard GP → Animatique → Layout 3D → Blocking → Animation
        → Lighting → Rendering → Compositing → Montage final
```
| Étape | Appris en | Livrable transmis à l'étape suivante |
|---|---|---|
| Scénario | CH15.01, CH14.02 | Script + liste des séquences |
| Storyboard Grease Pencil | CH18.10–13 | Planches + caméras de board (fichier .blend) |
| Animatique | CH18.14–15, CH12 | Vidéo minutée + **durées de plans de référence** |
| Layout 3D | CH18.20, CH09, CH16.02 | Un fichier par plan, caméra reprise du board, décors en link |
| Blocking | CH07 | Poses clés validées sur la durée de l'animatique |
| Animation | CH07 | Animation finale (cache Alembic éventuel) |
| Lighting | CH09 | Éclairage par séquence + light groups |
| Rendering | CH10 | EXR multicouches |
| Compositing | CH11 | Images finales |
| Montage final | CH12 | Remplacement plan par plan de l'animatique → master |

Le détail (conventions de fichiers, scripts de passage d'une étape à l'autre) est dans
[DOCUMENTATION/PIPELINE_BRIDGES.md](DOCUMENTATION/PIPELINE_BRIDGES.md).

---

## Annexes
- Modèle de leçon : [TEMPLATES/LESSON_TEMPLATE.md](TEMPLATES/LESSON_TEMPLATE.md)
- Conventions : [DOCUMENTATION/CONVENTIONS.md](DOCUMENTATION/CONVENTIONS.md)
- Compatibilité de version : [DOCUMENTATION/VERSION_COMPATIBILITY.md](DOCUMENTATION/VERSION_COMPATIBILITY.md)
- Calendriers : [ROADMAP.md](ROADMAP.md)
- Logiciels complémentaires : [DOCUMENTATION/COMPLEMENTARY_SOFTWARE.md](DOCUMENTATION/COMPLEMENTARY_SOFTWARE.md)
- Passerelles du pipeline : [DOCUMENTATION/PIPELINE_BRIDGES.md](DOCUMENTATION/PIPELINE_BRIDGES.md)
