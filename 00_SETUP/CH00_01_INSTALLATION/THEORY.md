# CH00.01 — Cours théorique

> Ce document est la version longue de la partie **A. Comprendre** de chaque leçon.
> Lisez-le une fois en entier, puis revenez-y quand une leçon y renvoie.

---

## 1. Qu'est-ce que Blender ?

Blender est une **suite de création 3D complète** : modélisation, sculpture, textures,
rigging, animation, simulations, rendu, compositing, montage vidéo, et même dessin 2D
animé (Grease Pencil). La plupart des logiciels du cinéma d'animation ne couvrent qu'une
partie de cette chaîne ; Blender peut, à lui seul, produire un film du storyboard au
master final.

**Analogie.** Imaginez un studio de cinéma entier rangé dans une seule boîte à outils :
l'atelier de décors, la loge maquillage, les costumes, les projecteurs, la caméra, la
salle de montage. Chaque « pièce » de ce studio est un **éditeur** de Blender, et vous
passez de l'un à l'autre sans changer de logiciel.

### 1.1 Qui fait Blender ?
- La **Blender Foundation**, une fondation néerlandaise à but non lucratif, gère le projet.
- Le **Blender Institute** et le **Blender Studio** emploient des développeurs et
  réalisent des films ouverts (« Open Movies ») qui servent à tester Blender en
  conditions réelles de production.
- Le **Development Fund** (dons individuels et d'entreprises) finance le développement.
- Des contributeurs bénévoles et des entreprises ajoutent du code.

### 1.2 La licence : GNU GPL
Blender est un **logiciel libre** sous licence **GNU GPL (version 2 ou ultérieure)**.
Concrètement, pour vous :

| Question | Réponse |
|---|---|
| Blender est-il gratuit ? | Oui, pour tout usage, y compris commercial. |
| Mes images, films et modèles m'appartiennent-ils ? | **Oui.** La GPL s'applique au *logiciel*, pas à ce que vous créez avec. |
| Puis-je vendre un film fait avec Blender ? | Oui. |
| Et les scripts / add-ons que j'écris ? | Un add-on qui utilise l'API Python de Blender et que vous **distribuez** doit être compatible GPL. Pour un usage interne, aucune obligation. |
| Les assets téléchargés sur Internet ? | Ils ont **leur propre licence** (CC0, CC-BY, propriétaire…). Toujours vérifier — voir `ASSET_MANIFEST.json`. |

### 1.3 Le cycle des versions
Blender suit une numérotation `MAJEUR.MINEUR.CORRECTIF`, par exemple **5.3.0**.

| Type | Rythme | Pour qui ? |
|---|---|---|
| **Stable** | une nouvelle version environ tous les 3–4 mois | Usage quotidien, formation, projets courts |
| **LTS** (*Long-Term Support*) | une par an, maintenue **2 ans** (corrections uniquement, pas de nouvelles fonctions) | Productions longues qui ne doivent pas changer de version |
| **Daily builds** (Alpha, Beta, RC) | chaque jour | Tester les nouveautés — **jamais pour un vrai projet** |

Dans chaque version, le **chiffre correctif** (5.3.**1**, 5.3.**2**…) corrige des bugs sans
changer les fonctions : on peut le mettre à jour sans risque.

> **En production** : on choisit une version au début du projet et on la **gèle**
> jusqu'à la livraison. Changer de version au milieu d'un film, c'est risquer que des
> rigs, des simulations ou des scripts se comportent différemment d'un plan à l'autre.

### 1.4 Ce que Blender 5.3 apporte (vue d'ensemble)
Vous n'avez pas besoin de comprendre ces notions maintenant ; elles seront enseignées dans
leurs phases respectives. Elles sont listées pour que vous sachiez pourquoi l'académie
cible cette version :
- **Vulkan** est désormais le *backend* graphique par défaut sous Windows et Linux
  (le moteur qui dessine l'interface et le viewport).
- Un **système de projet** optionnel (*File → Project*) permet à Blender de connaître la
  racine d'un projet au-delà du fichier ouvert — utile pour organiser un film (CH00.06).
- **Gaussian splats** : import de captures 3D « splats » (PLY, SPZ) et rendu dans
  Workbench, EEVEE et Cycles ; l'export n'est pas encore possible.
- **DLSS 4.5 Ray Reconstruction** (NVIDIA) comme débruiteur du viewport.
- **Montage (VSE)** : édition *ripple* et premier support d'OpenTimelineIO.
- **EEVEE** : nœuds *Material Lighting*.

---

## 2. Les méthodes d'installation sous Windows

| Méthode | Droits admin | Menu Démarrer + association `.blend` | Mises à jour | Plusieurs versions | Usage conseillé |
|---|---|---|---|---|---|
| **Installeur `.msi`** | Oui | Oui (automatique) | Manuelle (nouvel installeur) | Oui (un dossier par version) | Poste principal |
| **Archive `.zip`** | Non | Non (association possible via *Preferences → System → Register* ou `blender -r`) | Manuelle (nouveau zip) | Oui, très facile | Tester une version, poste sans droits admin |
| **Zip + dossier `portable`** | Non | Non | Manuelle | Oui | Clé USB, disque externe, environnement de projet figé |
| **Microsoft Store** | Non | Oui | **Automatiques** | Une seule | Débutant qui veut « que ça marche » |
| **Steam** | Non | Via Steam | Automatiques (branches possibles) | Limité | Utilisateurs Steam |

### Pourquoi les mises à jour automatiques sont un piège en production
Une mise à jour automatique peut changer votre version **un matin, au milieu d'un projet**.
Pour la formation, ce n'est pas grave. Pour un court-métrage de 3 mois, c'est un risque.
**Recommandation de l'académie :** installeur ou zip, avec mises à jour **décidées**.

### L'installation portable
Si vous créez un dossier nommé exactement **`portable`** à côté de `blender.exe` (dans le
dossier décompressé d'un zip), Blender y stockera ses préférences, son fichier de
démarrage, ses extensions et ses presets, **au lieu** du dossier utilisateur Windows.
Tout devient transportable et isolé : idéal pour figer l'environnement d'un projet.

---

## 3. Où Blender range-t-il ses fichiers ?

Blender sépare **ce qui est livré avec le logiciel** (*system*) de **ce qui vous appartient**
(*user*).

```
C:\Program Files\Blender Foundation\Blender 5.3\        ← installation (programme)
├── blender.exe                                          ← l'exécutable
├── blender-launcher.exe                                 ← lanceur (sans console)
└── 5.3\                                                 ← fichiers système (scripts, datafiles…)

%APPDATA%\Blender Foundation\Blender\5.3\                ← VOS réglages (user)
├── config\
│   ├── userpref.blend      ← vos préférences
│   ├── startup.blend       ← votre scène de démarrage (File > Defaults > Save Startup File)
│   ├── recent-files.txt    ← fichiers récents
│   └── bookmarks.txt       ← favoris du navigateur de fichiers
├── extensions\             ← extensions installées
├── scripts\                ← add-ons, presets, scripts de démarrage
└── autosave\               ← sauvegardes automatiques (Windows uniquement)
```
(`%APPDATA%` = `C:\Users\<vous>\AppData\Roaming`.)

**Point clé : un dossier de réglages par version.** Blender 5.2 et 5.3 ont chacun leur
dossier `5.2\` et `5.3\`. C'est ce qui permet de les faire cohabiter. Au premier
lancement d'une nouvelle version, l'écran d'accueil propose d'**importer les préférences
de la version précédente** (*Import Preferences From Previous Version*) ou d'en créer de
nouvelles (*Save New Preferences*).

> Les add-ons et extensions importés depuis une ancienne version peuvent être
> incompatibles ; en cas d'erreurs au démarrage, la première chose à faire est
> *File → Defaults → Load Factory Settings*.

---

## 4. Comment Blender utilise votre matériel

| Composant | Rôle dans Blender | Ce qui se passe s'il est faible |
|---|---|---|
| **CPU** (processeur) | Modificateurs, simulations, Geometry Nodes, animation, rendu Cycles CPU | Viewport lent sur les scènes lourdes, simulations longues |
| **GPU** (carte graphique) | Affichage de l'interface et du viewport (Vulkan/OpenGL), EEVEE, rendu Cycles GPU | Viewport saccadé, EEVEE lent, rendus Cycles longs |
| **VRAM** (mémoire du GPU) | Doit contenir la scène entière pour un rendu GPU | « Out of memory » au rendu GPU → retour au CPU |
| **RAM** | Fichiers ouverts, undo, simulations, compositing | Ralentissements, plantages sur gros fichiers |
| **Disque (SSD)** | Ouverture/sauvegarde, caches de simulation, textures | Chargements lents, caches interminables |

### 4.1 Les deux moteurs de rendu principaux
- **EEVEE** : moteur temps réel (rastérisation + ray tracing écran). Très rapide,
  idéal pour la prévisualisation, l'animation stylisée, le *look development*. Il
  **utilise toujours le GPU**.
- **Cycles** : moteur de *path tracing* (il simule le trajet de la lumière). Physiquement
  plus juste, plus lent. Il peut tourner **sur le CPU ou sur le GPU**.
- (*Workbench* : moteur d'affichage technique, pour le viewport et les prévisualisations.)

### 4.2 Les API de calcul GPU de Cycles
| API | Matériel | Remarque |
|---|---|---|
| **CUDA** | NVIDIA | Compatible avec la plupart des GPU NVIDIA récents |
| **OptiX** | NVIDIA RTX (et certaines GTX récentes) | Utilise les cœurs RT ; permet aussi le débruiteur OptiX |
| **HIP** | AMD | Cartes AMD Radeon récentes |
| **oneAPI** | Intel Arc | |
| **Metal** | Apple Silicon / macOS | |

**Mesure réelle sur le poste de référence** (mire du chapitre, 960×540, 64 échantillons,
sans débruitage) :

| API | Temps | Accélération |
|---|---|---|
| CPU i9-10900 (20 threads) | 7,41 s | ×1 |
| CUDA RTX 3080 | 0,83 s | ×8,9 |
| OptiX RTX 3080 | 0,84 s | ×8,8 |

Sur cette scène simple, CUDA et OptiX sont équivalents ; OptiX prend généralement
l'avantage sur des scènes plus lourdes (beaucoup de géométrie, ray tracing complexe).
**La seule façon de savoir, c'est de mesurer sur VOS scènes** — c'est l'objet du benchmark.

> ⚠️ Le **premier** rendu GPU d'une session est souvent plus lent : Cycles charge ses
> *kernels* (programmes GPU). Le script de benchmark fait donc un petit rendu de
> « chauffe » avant chaque mesure GPU.

---

## 5. La ligne de commande : pourquoi un artiste devrait s'y intéresser

En studio, la majorité des rendus ne sont **pas** lancés en cliquant sur *Render* : ils
sont lancés par des scripts, sur des machines sans écran (*render farm*), la nuit.
Blender sait fonctionner **sans interface** : c'est le **mode arrière-plan** (*background*).

| Argument | Effet |
|---|---|
| `--version` | Affiche la version et le build, puis quitte |
| `-b` / `--background` | Lance Blender sans interface |
| `--factory-startup` | Ignore vos préférences et votre `startup.blend` (réglages d'usine) |
| `fichier.blend` | Ouvre ce fichier (à placer **avant** les options de rendu) |
| `-f 1` | Rend l'image n° 1 |
| `-a` | Rend toute l'animation |
| `-o //renders/img_####` | Chemin de sortie (`####` = numéro d'image) |
| `-E CYCLES` | Choisit le moteur |
| `--python script.py` (`-P`) | Exécute un script Python |
| `--python-expr "..."` | Exécute une expression Python |
| `--python-exit-code 1` | Renvoie un code d'erreur si le script Python plante (indispensable pour l'automatisation) |
| `-- --cycles-device OPTIX` | Après `--` : choisit le périphérique Cycles |
| `-r` / `--register` | Associe les fichiers `.blend` à cet exécutable |

**L'ordre compte** : Blender lit les arguments de gauche à droite. Le fichier doit être
ouvert **avant** de demander un rendu (`-f`), et `-o`/`-E` doivent précéder `-f`/`-a`.

Exemple complet : rendre l'image 1 de la mire avec OptiX, sans interface :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b `
  "COMPLETED_EXAMPLES\ch00_01_testcard_solution.blend" `
  -o "//renders/cli_####" -f 1 -- --cycles-device OPTIX
```

---

## 6. Pourquoi un rendu sort noir ou vide : les 5 suspects

C'est la panne la plus fréquente du débutant… et elle arrive aussi en studio. Retenez
la méthode **« de la caméra vers la lumière »** :

1. **La caméra voit-elle les objets ?** *Clip Start / Clip End* : tout ce qui est hors de
   cet intervalle de distance est invisible.
2. **Les objets sont-ils rendus ?** Icône *appareil photo* (Disable in Renders) sur l'objet
   **ou sur sa collection** dans l'Outliner.
3. **Y a-t-il de la lumière ?** Lumières masquées au rendu, puissance à 0, monde (*World*)
   à intensité 0.
4. **L'image a-t-elle la bonne taille ?** *Resolution %* très bas = image minuscule.
5. **Le bon fichier, la bonne caméra, la bonne image ?** Caméra active, numéro d'image,
   chemin de sortie.

C'est exactement ce que vous ferez dans l'exercice 3, sur une scène qui contient ces
5 pannes à la fois.
