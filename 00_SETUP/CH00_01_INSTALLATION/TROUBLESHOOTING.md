# CH00.01 — Dépannage

Identifiez le symptôme. Si Blender s’ouvre et qu’un rendu CPU fonctionne, vous pouvez réaliser le premier jalon. Le rapport système aide ensuite à diagnostiquer le matériel et les préférences.

## 1. Blender ne démarre pas / se ferme immédiatement
| Cause probable | Solution |
|---|---|
| Pilote graphique trop ancien ou défectueux | Mettre à jour le pilote depuis le site du fabricant (NVIDIA/AMD/Intel). Blender 5.3 utilise **Vulkan** par défaut sous Windows. |
| Problème avec le backend Vulkan | Lancer `blender_startup_opengl.cmd` (dans le dossier d'installation) pour démarrer avec OpenGL ; si cela fonctionne, choisir le backend dans *Preferences → System → Display Graphics → Backend* (redémarrage nécessaire) et signaler le problème. |
| Extension / add-on défectueux | Lancer `blender_factory_startup.cmd` (ou `blender --factory-startup`). Si Blender démarre, le problème vient de votre configuration. |
| Configuration corrompue | Renommer `%APPDATA%\Blender Foundation\Blender\5.3` en `5.3_bak` et relancer. |
| Processeur trop ancien | Blender requiert un CPU x86-64 avec des instructions récentes (le fichier `blender_cpu_check.dll` vérifie la compatibilité au démarrage et affiche un message explicite). |

Pour voir les messages d'erreur : `blender_debug_log.cmd` (dans le dossier d'installation)
écrit un journal détaillé ; ou lancer `blender.exe` depuis PowerShell.

## 2. Mon GPU n'apparaît pas dans *Cycles Render Devices*
| Cause probable | Solution |
|---|---|
| Mauvais onglet sélectionné | NVIDIA : onglets **CUDA** ou **OptiX** ; AMD : **HIP** ; Intel compatible : **oneAPI**. Apple compatible : **Metal**. |
| Pilote trop ancien | Mettre à jour ; les fonctions récentes (OptiX, DLSS) exigent des pilotes récents. |
| GPU non supporté (trop ancien) | Consulter la page *GPU Rendering* du manuel officiel ; rendre sur CPU. |
| PC portable avec deux GPU | Forcer Blender sur le GPU dédié (*Paramètres Windows → Affichage → Graphiques*). |
| Message `HIPEW initialization failed` dans la console sur une machine NVIDIA | **Normal** : Blender cherche aussi les bibliothèques AMD et n'en trouve pas. Ignorer. |

## 3. *Device → GPU Compute* est grisé ou absent
Le GPU n'est pas activé dans les **préférences** (tutoriel 3). Le menu *Device* n'existe
qu’avec le moteur **Cycles**. Pour la première mire, choisissez CPU et conservez le même objectif d’image.

## 4. Le rendu GPU est plus lent que prévu
- Premier rendu de la session : chargement des *kernels* → refaire la mesure.
- CPU coché en plus du GPU : sur certaines machines, le rendu hybride est plus lent. Mesurer.
- Scène trop lourde pour la VRAM : Cycles peut utiliser la mémoire système, plus lente.
  Surveiller la VRAM : *Preferences → Interface → Status Bar → Video Memory* l'affiche dans la barre d'état.
- Petite image / peu d'échantillons : les étapes fixes dominent (voir défi 2).

## 5. Le rendu est noir, vide ou minuscule
Appliquez la méthode des 5 suspects (THEORY.md §6) : clip caméra → visibilité au rendu
(objets **et** collections) → lumières et monde → *Resolution %* → caméra active / image /
sortie. Testez avec un rendu rapide (25 %, peu d'échantillons).

Autres causes fréquentes :
- **Aucune caméra active** : message *No camera found in scene*. Sélectionner une caméra,
  `Ctrl+Num 0` pour la rendre active.
- **Exposition** : *Render → Color Management → Exposure* très négative.
- Objet à **l'intérieur** d'un autre objet ou caméra **à l'intérieur** d'un mur.

## 6. La ligne de commande ne trouve pas `blender`
`blender` n'est pas dans le `PATH`. Utiliser le chemin complet entre guillemets avec
l'opérateur `&` dans PowerShell :
`& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" --version`
ou créer un alias (TUTORIAL.md, tutoriel 4).

## 7. La commande de rendu ne produit pas d'image
- L'ordre des arguments est faux : le fichier `.blend` doit précéder `-o` et `-f`, et
  `-o`/`-E` doivent précéder `-f`/`-a`.
- Chemin de sortie relatif sans `//` : il est alors interprété par rapport au dossier
  courant du terminal. Préférer `//…` (relatif au `.blend`) ou un chemin absolu.
- Le terminal affiche `Saved: '…'` : c'est là que se trouve l'image.

## 8. Le script Python échoue
- Lire la *traceback* (dernières lignes) : elle indique le fichier, la ligne et l'erreur.
- `AttributeError` : propriété renommée entre deux versions → vérifier la documentation
  de l'API de **votre** version (`docs.blender.org/api/<version>/`).
- `DeprecationWarning: 'Material.use_nodes' is expected to be removed in Blender 6.0` :
  avertissement (pas une erreur) ; depuis 5.0 les matériaux ont toujours des nœuds.
- Toujours ajouter `--python-exit-code 1` pour qu'un échec soit détectable.

## 9. Mes préférences « ont disparu » après une mise à jour
Normal : chaque version a son dossier. À l'écran d'accueil de la nouvelle version,
importer les préférences de la version précédente — ou copier manuellement le dossier
`config\` de l'ancienne version (en connaissance de cause).
