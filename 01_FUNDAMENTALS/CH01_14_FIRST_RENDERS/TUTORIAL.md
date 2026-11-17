# CH01.14 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch01_14_final_render_starter.blend` et enregistrez-le tout de suite
sous `ch01_14_final_render_<prenom>_v001.blend`.

## Tutoriel 1 — Un premier rendu EEVEE
1. `F12`. Une fenêtre de rendu s'ouvre. Lisez *Time* en haut.
2. Fermez la fenêtre (ou `Échap`).

## Tutoriel 2 — Passer en Cycles et régler la qualité
1. *Render → Render Engine* : **Cycles** ; *Device* : **CPU**, ou **GPU Compute** si votre GPU est configuré et compatible.
2. *Sampling → Render* : *Noise Threshold* **0.02**, *Max Samples* **128**, **Denoise** coché.
3. *Output → Format* : 1920 × 1080, **100 %**.
4. *Output → Output* : chemin `//renders/ch01_14_final_`, *File Format* **PNG**, *Color*
   **RGB**, *Color Depth* **8**.

## Tutoriel 3 — Gestion des couleurs
1. *Render → Color Management* : *View Transform* **AgX** ; *Look* **AgX - Medium High Contrast**.
2. Essayez *False Color* en mode Rendered : les zones rouges/blanches sont surexposées, bleues
   sous-exposées. Revenez à AgX.

## Tutoriel 4 — Rendre et enregistrer
1. `F12`. Attendez la fin (le compteur d'échantillons s'arrête).
2. Fenêtre de rendu : *Image → Save As* (`Shift+Alt+S`) → naviguez dans le dossier du
   `.blend`, créez le dossier `renders` si nécessaire, nommez `ch01_14_final.png` → *Save As Image*.
3. Bonus : *Render Engine* → EEVEE, `F12`, enregistrez `renders/ch01_14_eevee.png`, puis
   remettez Cycles. Comparez les deux images (*Slot* 1 et 2, touche `J`).
4. `Ctrl+S`.

## Tutoriel 5 — Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch01_14_final_render_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch01_14.py" -- --exercise final
```
Référence : `COMPLETED_EXAMPLES/renders/ch01_14_final.png` (et `ch01_14_eevee.png`).

## Contrôle de transfert

Rendez une image de comparaison à résolution réduite avant la sortie 1920 × 1080. L’option Noise Threshold agit sur l’arrêt adaptatif et Max Samples est un plafond. Comparez les bruits dans une ombre avant et après débruitage. Après F12, enregistrez le PNG et rouvrez-le, puis rouvrez le fichier .blend. **Réussite** Nom exact, cadre, résolution, moteur, échantillons et périphérique sont vérifiables. Le mode CPU convient si le GPU Cycles est indisponible.
