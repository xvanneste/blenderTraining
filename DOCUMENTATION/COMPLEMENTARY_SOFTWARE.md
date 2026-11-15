# Logiciels complémentaires — guide et parcours

> **Règle** : rien n'est téléchargé ni installé par l'académie. Chaque logiciel ci-dessous s'installe
> **par vous**, depuis son **site officiel uniquement**, au moment où un chapitre en a besoin.
> État vérifié sur la machine de travail (14/11/2026) : **aucun** de ces logiciels n'est installé ;
> seuls Blender (3.6 → 5.3), Git, Node.js et Python sont présents. Pas de FFmpeg système (Blender
> embarque le sien pour l'export vidéo).
>
> Les licences indiquées sont celles connues à la rédaction ; **revérifiez-les sur le site officiel
> avant installation** (elles peuvent changer). Priorité : logiciel libre / gratuit ; un logiciel
> propriétaire gratuit est signalé comme tel.

## 1. Vue d'ensemble : que faire dans Blender, que faire ailleurs ?
| Domaine | Dans Blender (5.3) | Logiciel complémentaire recommandé | Licence | Quand (phase) |
|---|---|---|---|---|
| **Montage** | Video Sequencer (VSE) : suffisant pour animatiques et courts | **Kdenlive** ; alternative **Shotcut** | GPL (libres) | 12, 15–16 |
| **Étalonnage** | Compositor, Color Management (AgX, looks) | **DaVinci Resolve** (version gratuite) | Propriétaire gratuit | 11–12, 16 |
| **Audio** | VSE : placement de sons, volume, fondus | **Audacity** (édition) ; **Ardour** (mixage multipiste) | GPL | 12, 15 |
| **Textures peintes** | Texture Paint, nœuds procéduraux | **Krita** (peinture), **GIMP** (retouche) | GPL | 4 |
| **Textures procédurales** | Shader Editor, Geometry Nodes | **Material Maker** | MIT | 4 (option) |
| **Vectoriel / logos** | Grease Pencil, courbes (import SVG) | **Inkscape** | GPL | 18, 15 (titres) |
| **Dessin / storyboard** | **Grease Pencil** (phase 18) | **Krita** (peinture d'animatique, concept art) | GPL | 18 |
| **Animation 2D dédiée** | Grease Pencil | **OpenToonz** (pipeline 2D traditionnel) | BSD | 18 (comparaison) |
| **Compositing nodal externe** | Compositor | **Natron** (développement ralenti : à évaluer) | GPL | 11 (option) |
| **Photogrammétrie** | Import OBJ/glTF/PLY, nettoyage, retopo | **Meshroom** (AliceVision) — demande un GPU NVIDIA CUDA (présent : RTX 3080) | MPL 2.0 | 2–3 (option) |
| **Motion capture** | Import BVH/FBX, retargeting manuel | **FreeMoCap** (mocap par webcams) | AGPL | 7 (CH07.14, option) |
| **Gestion de production** | — | **Kitsu** (suivi de plans et validations) ; ou un simple tableur + `TOOLS/` de l'académie | AGPL | 13, 15–16 |
| **Versionnement** | Save Incremental, Projects 5.3 | **Git** (déjà installé) + Git LFS pour les gros fichiers | GPL | 13 |
| **Automatisation** | Python `bpy`, add-ons | Python système (installé), scripts `TOOLS/` | PSF | 13 |
| **Encodage vidéo** | Export FFmpeg intégré au rendu | **HandBrake** (ré-encodage de diffusion) | GPL | 16 (option) |
| **IA** | — | Voir phase 14 : chaque outil évalué (licence, données, droits) au moment du chapitre | variable | 14 |

**Principe directeur** : tout le parcours obligatoire peut être réalisé **dans Blender seul**. Les
logiciels complémentaires apportent du confort ou des standards de l'industrie ; ils sont **optionnels**
sauf mention contraire dans un chapitre.

## 2. Parcours complémentaires
Chaque parcours est un mini-cours autonome à suivre quand la phase indiquée est atteinte. Format :
objectif, prérequis, séances, livrable, pont vers le pipeline Blender. Les chapitres détaillés
(avec exercices et quiz) seront produits **après installation validée par vous** du logiciel concerné,
afin que chaque libellé de menu soit vérifié dans la vraie version (règle « ne jamais inventer »).

### 2.1 Montage — Kdenlive (ou VSE)
- **Objectif** : monter une animatique puis un court ; exporter un master.
- **Prérequis** : phase 12 (VSE), CH18.14–CH18.15 (animatique).
- **Séances** : (1) projet, profil 1920×1080 / 24 i/s, chutier ; (2) dérushage, points d'entrée/sortie ;
  (3) montage sur pistes, raccords, J-cut / L-cut ; (4) titres, fondus ; (5) export master + export
  web ; (6) aller-retour : remplacer un plan d'animatique par son rendu final (même durée, même nom).
- **Livrable** : animatique montée et sa version finale.
- **Pont pipeline** : nommage des plans `SQ010_SH0010` identique dans Blender et le montage
  (DOCUMENTATION/PIPELINE_BRIDGES.md) ; rendus en séquences d'images PNG/EXR, jamais en vidéo
  intermédiaire compressée.

### 2.2 Étalonnage — DaVinci Resolve (gratuit)
- **Objectif** : unifier la colorimétrie d'un court, créer un look.
- **Prérequis** : phase 9 (lighting), CH11.06 (color grading dans Blender), Color Management (AgX).
- **Séances** : (1) gestion des couleurs (espaces, transformations d'affichage) ; (2) corrections
  primaires (lift / gamma / gain), scopes ; (3) raccord colorimétrique entre plans ; (4) secondaires
  (masques, qualifieurs) ; (5) look et export.
- **Livrable** : avant/après sur 5 plans.
- **Pont** : rendre en EXR scène-linéaire (ou PNG 16 bits avec la vue AgX) ; documenter la vue
  utilisée pour éviter un double étalonnage.

### 2.3 Audio — Audacity / Ardour
- **Objectif** : enregistrer des voix témoins, nettoyer, mixer dialogues, bruitages, musique.
- **Séances** : (1) enregistrement, niveau, format WAV 48 kHz ; (2) nettoyage (réduction de bruit,
  normalisation) ; (3) découpe des répliques nommées par plan ; (4) mixage multipiste (Ardour) ;
  (5) export stems (dialogues / musique / effets) et mix stéréo.
- **Pont** : les répliques servent au lip-sync (CH07.11) et à l’animatique (CH18.15).
- **Sources sonores** : uniquement CC0 / CC-BY avec attribution notée dans ASSET_MANIFEST.json.

### 2.4 Textures — Krita / GIMP / Material Maker
- **Objectif** : peindre des textures, retoucher des photos sources, générer des matériaux tuilables.
- **Séances** : (1) résolution et espace colorimétrique (couleur = sRGB, données = Non-Color) ;
  (2) texture tuilable ; (3) peinture de masques ; (4) export PNG 16 bits ; (5) aller-retour avec
  Texture Paint de Blender.
- **Pont** : phase 4 (UV, textures, matériaux).

### 2.5 Dessin — Krita
- **Objectif** : concept art, peinture des fonds d'animatique, model sheets en couleur.
- **Pont** : phase 18 — un fond peint dans Krita s'importe comme image de référence ou plan d'image
  derrière un objet Grease Pencil.

### 2.6 Gestion de production — Kitsu ou tableur
- **Objectif** : suivre l'état de chaque plan (layout → anim → lighting → rendu → compo), les
  validations et le temps passé.
- **Version minimale sans logiciel** : un tableur avec une ligne par plan + `SCRIPTS/bcma_shotlist_check.py`.
- **Pont** : phases 13, 15, 16.

### 2.7 Motion capture — FreeMoCap
- **Objectif** : capturer un mouvement avec des webcams, l'importer et le nettoyer sur un rig.
- **Prérequis** : phase 6 (rigging), CH07.14 (motion capture dans Blender).
- **Limites** : précision inférieure à un système optique professionnel ; prévoir un nettoyage
  manuel important.

### 2.8 Photogrammétrie — Meshroom
- **Objectif** : numériser un objet ou un décor, puis nettoyer, retopologiser et texturer dans Blender.
- **Prérequis** : CH02.09 et CH03.09 (retopologie), phase 4 (textures).
- **Méthode de prise de vue** : 50–200 photos, recouvrement important, lumière diffuse, pas de surfaces
  réfléchissantes.

### 2.9 Automatisation — Python et Git
- Déjà disponibles. Couverts en phase 13 (scripts de pipeline, nommage, sauvegardes, rendus en lot) ;
  les outils `TOOLS/` de l'académie servent d'exemples réels et testés.

### 2.10 IA
- Traitée en **phase 14** : chaque outil (génération d'images de référence, storyboard assisté,
  voix, upscaling…) y est évalué **au moment de la rédaction** : disponibilité, licence, conditions
  d'utilisation des données, droits sur les résultats, coût. Aucun outil n'est recommandé sans cette
  vérification.

## 3. Procédure d'installation sûre (à faire vous-même)
1. Aller sur le **site officiel** (vérifier l'adresse), jamais sur un site miroir de téléchargement.
2. Télécharger l'installateur Windows ; vérifier la signature / l'empreinte si le site la publie.
3. Installer, puis noter version et date dans `DOCUMENTATION/VERSION_COMPATIBILITY.md`.
4. Prévenir l'assistant : le chapitre du parcours concerné pourra alors être rédigé et vérifié sur
   la version réellement installée.

## 4. Statut
| Parcours | Statut |
|---|---|
| Guide et plans de cours (ce document) | Terminé (non dépendant d'une installation) |
| Chapitres détaillés 2.1–2.8 | Non commencés — en attente d'installation des logiciels avec votre accord |
| 2.9 Automatisation | Couvert par la phase 13 (non commencée) |
| 2.10 IA | Couvert par la phase 14 (non commencée) |
