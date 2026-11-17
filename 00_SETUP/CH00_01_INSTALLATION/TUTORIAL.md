# CH00.01 — Tutoriels pas à pas

> Notation : `LMB` = clic gauche, `RMB` = clic droit, `MMB` = clic molette.
> Les noms de menus sont en **anglais** (interface de référence), traduits entre
> parenthèses à la première occurrence. ✅ = vérification à faire avant de continuer.

---

## Premier jalon — Rendre et conserver une image

Si Blender est déjà installé, commencez ici. Sinon, faites les tutoriels 1 et 2, puis revenez à ce jalon. La mire est une scène préparée avec une caméra, des lumières et quelques formes. Votre premier geste consiste à obtenir l’image que voit cette caméra.

1. Téléchargez ou ouvrez la [mire de départ](STARTER_FILES/ch00_01_testcard_starter.blend). Dans Blender, utilisez **File → Save As** et enregistrez une copie dans votre dossier de travail sous ch00_01_testcard_prenom_v001.blend.
2. Dans **Render Properties** (propriétés de rendu), choisissez **Cycles** comme moteur et **CPU** comme périphérique. Dans **Sampling → Render**, réglez **Max Samples** sur 128 et activez **Denoise**. Dans **Output Properties → Format**, laissez l’échelle à 100 %. Sous **Output**, utilisez le chemin relatif //renders/mire_. Rouvrez les propriétés pour vérifier que vous avez réglé **Render** et non **Viewport** sous Sampling.
3. Enregistrez le .blend. Lancez **Render → Render Image** ou **F12**. Quand le calcul se termine, la fenêtre de rendu affiche **Render Result**. Comparez le cadre et la présence des formes au [rendu de référence](COMPLETED_EXAMPLES/ch00_01_testcard_reference_render.png). Le débruitage et le périphérique peuvent donner de petites différences.
4. Dans la fenêtre de rendu, ouvrez **Image → Save As**, choisissez **PNG**, saisissez mire_v001.png dans le dossier de travail, puis validez. Ouvrez le PNG dans un lecteur d’images. Rouvrez aussi votre copie .blend et retrouvez le moteur Cycles et le périphérique CPU.
5. **À refaire sans le pas-à-pas**. Dans une nouvelle copie v002, passez à 64 échantillons et enregistrez le second PNG sous mire_v002.png. Les deux PNG doivent rester distincts et cadrer la même scène. Si votre objectif est d’aller plus loin, le tutoriel 3 permet de comparer un GPU compatible, et le tutoriel 4 permet de refaire le rendu par le terminal.

**Réussite** Vous avez deux fichiers .blend versionnés et deux PNG lisibles. F12 calcule l’image courante. L’enregistrement du PNG depuis Image → Save As produit le fichier que vous pouvez partager.

## Tutoriel 1 — Installer Blender 5.3 (installeur ou zip)

### Option A : installeur Windows (recommandé pour le poste principal)
1. Ouvrez un navigateur sur [la page Blender 5.3](https://www.blender.org/releases/5-3/).
2. Le site détecte Windows : vérifiez que la version proposée est **5.3.x** et
   l'architecture **x64** (ou ARM64 si vous avez un PC ARM).
3. Téléchargez le fichier **Windows Installer** (`blender-5.3.x-windows-x64.msi`).
4. Double-cliquez sur le `.msi`, acceptez la licence (GPL), gardez le dossier proposé :
   `C:\Program Files\Blender Foundation\Blender 5.3\`.
5. Terminez l'installation.
   ✅ Une entrée **Blender 5.3** apparaît dans le menu Démarrer.

### Option B : zip (sans droits administrateur, ou pour une 2ᵉ version)
1. Sur la même page, choisissez **Windows – Portable (.zip)**.
2. Décompressez l'archive dans un dossier à vous, par exemple
   `G:\Apps\Blender\blender-5.3.0-windows-x64\`.
3. Double-cliquez sur `blender.exe`.
   ✅ Blender démarre, sans rien installer dans Windows.
4. *(Facultatif)* Pour rendre l'installation **portable** : fermez Blender, créez un
   dossier nommé `portable` à côté de `blender.exe`, relancez Blender.
   ✅ Après avoir modifié une préférence, un sous-dossier `config\` apparaît dans `portable\`.

> 💡 Vérifiez toujours que vous téléchargez depuis **blender.org** (ou le Microsoft Store /
> Steam officiels). Des sites tiers proposent des « Blender » modifiés : ne les utilisez pas.

---

## Tutoriel 2 — Premier lancement et écran d'accueil

1. Lancez Blender 5.3.
2. Au tout premier lancement d'une version, l'écran d'accueil (*splash screen*) affiche les
   **réglages initiaux** :
   - **Language** (langue) : choisissez **English** pour suivre l'académie à l'identique.
     (Vous pourrez traduire l'interface plus tard dans *Preferences → Interface → Translation*.)
   - **Theme** : *Dark* ou *Light*, selon votre confort.
   - **Keymap** : **Blender** (la configuration par défaut utilisée dans tous les cours).
   - **Mouse Select** : **Left** (sélection au clic gauche, par défaut).
   - **Spacebar Action** : **Play** (lecture de l'animation, par défaut).
3. Si une version précédente est installée, l'écran propose d'**importer les préférences
   de la version précédente** (*Import Preferences From Previous Version*, bouton libellé
   avec le numéro de l'ancienne version). Pour suivre l'académie, préférez des
   préférences neuves : bouton **Save New Preferences**.
4. Cliquez n'importe où hors de l'écran d'accueil pour le fermer.
   ✅ Vous voyez un cube gris, une caméra et une lumière dans la vue 3D.

### Retrouver sa version exacte (3 méthodes)
- Menu **Help → About Blender** (ou le logo Blender en haut à gauche → *About Blender*) :
  version et *hash* du build.
- **Barre d'état** (en bas) : `RMB` → cochez **Blender Version**.
- Ligne de commande (tutoriel 4) : `blender --version`.
✅ Vous lisez **5.3.0** (ou 5.3.x).

---

## Tutoriel 3 — Activer le GPU pour Cycles (approfondissement)

1. Menu **Edit → Preferences** (Édition → Préférences).
2. Onglet **System** (à gauche).
3. Section **Cycles Render Devices** : des onglets *None, CUDA, OptiX, HIP, oneAPI*
   s'affichent (selon votre plateforme).
   - Carte **NVIDIA RTX** : choisissez **OptiX**.
   - Autre carte NVIDIA : **CUDA**.
   - **AMD compatible** : **HIP**. **Intel compatible** : **oneAPI**. Sur macOS, vérifiez **Metal** si le matériel est compatible.
   - Si aucun périphérique compatible n’apparaît, gardez **CPU** sur la mire.
4. Cochez votre carte graphique dans la liste. **Décochez le CPU** sauf si vous savez que
   le rendu hybride est plus rapide sur votre machine (à mesurer avec le benchmark).
   ✅ Votre GPU est listé et coché. S'il n'apparaît pas, voir TROUBLESHOOTING.md §2.
5. Les préférences se sauvegardent automatiquement (*Auto-Save Preferences*, bouton en bas
   à gauche ☰). Si l'option est désactivée, cliquez **Save Preferences**.
6. Fermez la fenêtre des préférences.

### Dire à la scène d'utiliser le GPU
Les préférences disent **quel** GPU est disponible ; c'est **chaque scène** qui décide de
l'utiliser.

1. Ouvrez `STARTER_FILES/ch00_01_testcard_starter.blend` (**File → Open**, `Ctrl+O`).
2. Éditeur **Properties** (à droite) → onglet **Render** (icône appareil photo arrière).
3. **Render Engine** : **Cycles**.
4. **Device** : **GPU Compute**.
   ✅ Le menu Device propose *GPU Compute* (s'il est grisé, l'étape 3 précédente n'est pas faite).

---

## Tutoriel 4 — Lancer Blender en ligne de commande

1. Ouvrez **PowerShell** (touche Windows, tapez `powershell`, Entrée).
2. Affichez la version :
   ```powershell
   & "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" --version
   ```
   ✅ La première ligne indique `Blender 5.3.0`, suivie de la date et du *hash* du build.
3. Dans PowerShell, placez-vous dans le dossier qui contient votre copie de la mire. Le chemin de Blender ci-dessous correspond à l’installeur Windows par défaut. Remplacez-le par le chemin de votre exécutable si vous utilisez l’archive portable.
4. Rendez l’image 1 en CPU. Conservez le nom de fichier appliqué à votre copie.

```powershell
$blender = "C:/Program Files/Blender Foundation/Blender 5.3/blender.exe"
$scene = (Resolve-Path "./ch00_01_testcard_prenom_v001.blend").Path
& $blender -b $scene -o "//renders/cli_cpu_####" -F PNG -f 1 -- --cycles-device CPU
```

Le terminal indique le chemin effectivement écrit. Ouvrez renders/cli_cpu_0001.png à côté de votre .blend. Placez les options de sortie avant -f, qui déclenche le calcul. Le suffixe #### indique quatre positions réservées au numéro de l’image. Sur un poste compatible, remplacez CPU par le périphérique validé au tutoriel 3 et utilisez un préfixe différent pour garder les deux mesures.

> 💡 Astuce : créez un alias PowerShell pour ne plus taper le chemin complet. Dans votre
> profil PowerShell (`notepad $PROFILE`) ajoutez :
> `Set-Alias blender53 "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe"`

---

## Tutoriel 5 — Générer votre rapport système et votre benchmark

### Rapport système
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b `
  --python "SCRIPTS\bcma_system_report.py" -- --out "$PWD\MES_RESULTATS"
```
✅ Le terminal affiche des lignes `[BCMA][OK] …` puis `Rapport écrit : …`.
Ouvrez le fichier `.md` généré dans `MES_RESULTATS\`.

> Sans `--factory-startup`, le script lit **vos** préférences (GPU sélectionné, Auto Save…).
> Avec `--factory-startup`, il montre les réglages d'usine : comparez les deux !

### Benchmark CPU / GPU
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  --python "SCRIPTS\bcma_render_benchmark.py" -- --out "$PWD\MES_RESULTATS\benchmark"
```
✅ Une ligne par périphérique (`CPU`, `CUDA`, `OPTIX`…) avec un temps en secondes, puis un
tableau `benchmark_<date>.md`. Comparez avec `COMPLETED_EXAMPLES/benchmark_reference/`.

### Depuis l'interface (sans terminal)
1. Workspace **Scripting** (onglet en haut de la fenêtre).
2. Dans l'éditeur de texte : **Open** → `SCRIPTS/bcma_system_report.py`.
3. Bouton ▶ **Run Script** (`Alt+P` avec la souris au-dessus du texte).
4. Le rapport est écrit dans `SCRIPTS/reports/`. Les messages s'affichent dans la console
   système (**Window → Toggle System Console**).

---

## Tutoriel 6 — Utiliser le correcteur automatique

Depuis le dossier du chapitre, indiquez le chemin de votre copie. Pour un fichier réglé sur CPU, utilisez testcard_cpu. Pour évaluer le réglage GPU, utilisez testcard. Le mini-rendu du correcteur utilise le CPU.
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch00_01_testcard_prenom_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch00_01.py" -- --exercise testcard_cpu --render
```
- Pour les exercices 1–2, choisissez testcard_cpu ou testcard selon le périphérique configuré. Utilisez broken pour l’exercice 3.
- `--render` ajoute un petit rendu de contrôle (CPU, 25 %, 8 échantillons).

✅ Le correcteur affiche ✔ / ✘ pour chaque critère, une **piste** pour chaque erreur, un
score et `RÉSULTAT : VALIDÉ` ou `À CORRIGER`.
