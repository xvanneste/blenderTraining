# CH11.06 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch11_06_grading_starter.blend`. Sauvegardez sous `ch11_06_grading_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Voir (5 min)
Une rampe de gris neutre.

## Tutoriel 2 — Color Balance (10 min)
Ajoutez un nœud Color Balance (type Lift/Gamma/Gain) entre Render Layers et la sortie.

## Tutoriel 3 — Teinter (10 min)
Couleur de Lift : (0,96 ; 1 ; 1,04). Couleur de Gain : (1,08 ; 1 ; 0,92).

## Tutoriel 4 — Mesurer (10 min)
Lancez le correcteur : ombres, hautes lumières, exposition.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch11_06_grading_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch11_06.py" -- --exercise grading --debug
```

Remarque d'honnêteté : le nœud `CompositorNodeColorBalance` 5.3 (Type Lift/Gamma/Gain, prises dédoublées facteur + couleur, indices 3–8) a été vérifié par exécution ; les valeurs sont mesurées sur une rampe de gris émissive à 160 × 90 en Standard ; plusieurs contre-exemples ont été ajustés pour être chirurgicaux (un Gain neutre trop fort écrêtait la rampe et annulait aussi la teinte des hautes lumières : remplacé par un Gamma 2,0) ; le seuil de chaleur est bas (0,03) car le Gain ne peut pas teinter une rampe déjà écrêtée à 1,0 ; la marge de too_bright sur ce seuil est de 0,0006 (rendu déterministe à 1 échantillon) ; les menus de création des nœuds n'ont pas été regardés ; Offset/Power/Slope, courbes et LUT ne sont pas évalués.

## Variante de contrôle

Choisissez un témoin gris et une zone saturée. Modifiez un réglage de balance à la fois. **Preuve** Vous pouvez décrire l’effet sur les ombres, tons moyens et hautes lumières sans réduire toute la correction à la saturation.
