# CH00.02 — Cours théorique : les préférences

## 1. Deux fichiers, deux rôles
Blender sépare deux choses que les débutants confondent souvent :

| | **Préférences** | **Fichier de démarrage** |
|---|---|---|
| Fichier | `config\userpref.blend` | `config\startup.blend` |
| Contenu | Comportement du logiciel : navigation, thème, raccourcis, GPU, add-ons, chemins, sauvegardes | Une scène et une disposition d'interface : ce que vous voyez au lancement et avec *File → New* |
| Modifié par | *Edit → Preferences* (sauvegarde automatique par défaut) | *File → Defaults → Save Startup File* |
| Réinitialisé par | Menu ☰ → *Load Factory Preferences* | *File → Defaults → Load Factory Settings* (réinitialise **les deux**) |
| Concerne vos `.blend` ? | Non : les préférences vous suivent quel que soit le fichier ouvert | Non : il sert seulement de modèle pour les nouveaux fichiers |

**Analogie.** Les préférences sont les réglages de **votre** siège de voiture (position,
rétroviseurs) : ils restent quand vous changez de trajet. Le fichier de démarrage est
**l'itinéraire par défaut** chargé dans le GPS quand vous démarrez.

> ⚠️ Les réglages propres à une scène (moteur de rendu, résolution, unités, caméra active)
> sont enregistrés **dans le `.blend`**, pas dans les préférences. C'est pourquoi vous
> avez dû choisir *GPU Compute* dans chaque scène au chapitre précédent.

## 2. La fenêtre Preferences
*Edit → Preferences* ouvre une fenêtre séparée. À gauche, des catégories :

| Catégorie | Ce qu'on y règle (essentiel pour l'académie) |
|---|---|
| **Interface** | Resolution Scale, Splash Screen, langue (Translation), Status Bar, menus |
| **Themes** | Couleurs de l'interface (presets, export/import) |
| **Viewport** | Qualité d'affichage, anti-aliasing, limites de textures |
| **Lights** | Éclairages du mode Solid (MatCaps, studio lights) |
| **Editing** | Nouveaux objets, *Copy on Duplicate*, curseur 3D, Grease Pencil |
| **Animation** | Clés, courbes, auto-keying |
| **Get Extensions / Add-ons** | Extensions et add-ons (CH00.05) |
| **Input** | Clavier (Emulate Numpad), souris (Emulate 3 Button Mouse), tablette, NDOF |
| **Navigation** | Orbite, zoom, Fly & Walk |
| **Keymap** | Raccourcis clavier (presets, modification, export) |
| **System** | Cycles Render Devices, Display Graphics (backend), mémoire, Undo Steps, son |
| **Save & Load** | Save Versions, Auto-Save, chemins relatifs, compression |
| **File Paths** | Dossiers par défaut (polices, textures, rendus, temporaire, bibliothèques d'assets) |

Une **barre de recherche** en haut de la fenêtre filtre les réglages par nom : tapez
« undo » et seule la ligne *Undo Steps* reste visible.

### Le menu ☰ (en bas à gauche)
| Entrée | Effet |
|---|---|
| **Auto-Save Preferences** (case) | Si cochée (défaut), chaque changement est enregistré immédiatement |
| **Save Preferences** | Enregistre maintenant (utile si l'auto-save est décoché) |
| **Revert to Saved Preferences** | Annule les changements depuis la dernière sauvegarde |
| **Load Factory Preferences** | Revient aux réglages d'usine (pour la session ; ils seront enregistrés si l'auto-save est actif) |

## 3. Interface
- **Resolution Scale** (*Interface → Display*) : agrandit tout (texte, icônes). Indispensable
  sur écran 4K ou portable haute densité (1,25–1,5). Ne confondez pas avec l'échelle
  Windows : Blender a son propre réglage.
- **Langue** (*Interface → Translation*) : la traduction française existe, mais l'académie
  et la majorité des tutoriels, forums et studios utilisent l'interface **anglaise**.
  Conseil : restez en anglais. Si vous traduisez, gardez au moins *Tooltips* en anglais
  pour pouvoir chercher les noms officiels.
- **Barre d'état** (*Interface → Status Bar*) : affichez *Scene Statistics* (objets,
  sommets, faces, triangles), *System Memory*, *Video Memory* (VRAM) et *Blender Version*.
  Ces chiffres sont vos voyants de tableau de bord.
- **Thèmes** : purement esthétiques, mais un thème plus contrasté réduit la fatigue
  visuelle sur de longues séances.

## 4. Navigation : ce que changent les réglages
| Réglage (Navigation) | Sans | Avec | Recommandé |
|---|---|---|---|
| **Orbit Around Selection** | L'orbite tourne autour du centre de la vue ; l'objet sélectionné « s'enfuit » | La vue tourne autour de la sélection | ✅ |
| **Zoom to Mouse Position** (*Zoom*) | Le zoom va vers le centre de l'écran | Le zoom va vers ce que pointe la souris | ✅ |
| **Auto → Depth** (*Auto Depth*) | La vitesse de navigation ignore la géométrie sous la souris | Blender lit la profondeur sous la souris : on ne « traverse » plus les objets en zoomant | ✅ |
| **Auto → Perspective** (*Auto Perspective*) | Les vues de face/côté restent en perspective | Les vues numériques (1, 3, 7) passent en orthographique, l'orbite repasse en perspective | ✅ (défaut) |
| **Orbit Method** | *Turntable* (défaut) : l'horizon reste horizontal | *Trackball* : rotation libre, utile en sculpture | Turntable |

**Émulations (catégorie Input)** :
- **Emulate 3 Button Mouse** : pour trackpad ou souris sans bouton central. `Alt` +
  clic gauche glissé = orbite ; `Shift+Alt` + clic gauche = panoramique ;
  `Ctrl+Alt` + clic gauche = zoom.
- **Emulate Numpad** : pour clavier sans pavé numérique. Les chiffres `1`–`9`, `0` de la
  rangée du haut se comportent comme le pavé. ⚠️ Effet secondaire : en Edit Mode, `1`/`2`/`3`
  ne changent plus le mode de sélection sommets/arêtes/faces (utilisez les boutons de
  l'en-tête).

### Les deux gestes qui remplacent 80 % des réglages
- **Frame Selected** — *View → Frame Selected*, touche `.` du pavé numérique : cadre la
  sélection.
- **Frame All** — *View → Frame All*, touche `Home` : cadre toute la scène.
Dans une scène de 400 bâtiments, *sélectionner dans l'Outliner + `.`* trouve un objet en
2 secondes. C'est l'objet de l'exercice 3.

### Clip Start / Clip End de la vue
La vue 3D (comme une caméra) n'affiche que ce qui se trouve entre *Clip Start* et
*Clip End* (sidebar `N` → onglet *View*). Défaut : 0,01 m – 1 000 m. Un objet à 1 km
disparaît ; un objet minuscule vu de très près est tranché. Réglage **de la vue**, enregistré
dans le `.blend` (pas dans les préférences).

## 5. Sécurité : annuler, versionner, sauvegarder
| Réglage | Où | Défaut 5.3 | Profil BCMA | Pourquoi |
|---|---|---|---|---|
| **Undo Steps** | System → Memory & Limits | 32 | 64 | Plus d'historique d'annulation (coût : RAM) |
| **Global Undo** | System → Memory & Limits | activé | activé | Annulation de tout (sinon seulement l'Edit Mode) |
| **Save Versions** | Save & Load → Blend Files | 1 | 2 | Garde `.blend1` et `.blend2` à chaque enregistrement |
| **Auto-Save** + **Timer** | Save & Load → Blend Files | activé, 2 min | activé, 2 min | Sauvegarde de secours dans le dossier temporaire |
| **Relative Paths** | Save & Load → Default To | activé | activé | Les textures restent trouvables si le projet est déplacé |
| **Save Prompt** | Save & Load | activé | activé | Demande confirmation avant de quitter sans enregistrer |

**Trois niveaux de protection, à ne pas confondre :**
1. **Annulation** (`Ctrl+Z` / `Shift+Ctrl+Z`) : en mémoire, perdue à la fermeture.
2. **`.blend1`, `.blend2`** : copies **écrasées** à chaque `Ctrl+S` ; elles protègent
   d'une mauvaise sauvegarde récente.
3. **Versions incrémentales** (`Ctrl+Alt+S` → `…_v002.blend`) : un historique **durable**,
   que vous décidez. C'est la règle en production (CH00.07 approfondit).

### Copy on Duplicate (Editing → Objects)
Quand vous dupliquez un objet (`Shift+D`), certaines données sont **copiées** (le mesh, par
défaut) et d'autres **partagées** (les matériaux, par défaut en 5.3). Comprendre ce
réglage évite des surprises : modifier le matériau d'une copie modifie aussi l'original.
On y revient en CH01.04.

## 6. Le fichier de démarrage
*File → Defaults → Save Startup File* enregistre la scène et l'interface **actuelles**
comme point de départ. Usage professionnel : supprimer le cube, régler les unités, la
résolution 1920×1080 à 24 i/s, ajouter vos workspaces préférés. **Attention** : tout ce
qui est dans la scène à ce moment devient le contenu de chaque *File → New*.
Pour revenir en arrière : *File → Defaults → Load Factory Settings*, puis à nouveau
*Save Startup File*.

## 7. Les préférences en production
- Un studio distribue souvent un **profil commun** (script ou dossier de configuration)
  pour que tous les postes se comportent pareil — c'est exactement ce que fait
  `bcma_prefs_profile.py`.
- On **sauvegarde** son dossier `config\` (zip daté ou dépôt Git) : réinstaller un poste
  prend alors quelques minutes.
- On ne change pas de préférences « structurelles » (raccourcis, keymap) au milieu d'un
  projet avec une équipe : tout le monde doit pouvoir s'aider.
