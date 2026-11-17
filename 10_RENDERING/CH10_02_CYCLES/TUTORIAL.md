# CH10.02 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch10_02_cycles_starter.blend`. Sauvegardez sous `ch10_02_cycles_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Voir (5 min)
F12 : le plafond est noir, l'image est piquée de points clairs.

## Tutoriel 2 — Les rebonds (5 min)
Properties > Render > Light Paths > Max Bounces > Diffuse : 4.

## Tutoriel 3 — L'échantillonnage (10 min)
Sampling > Render : cochez la case de l'en-tête (Noise Threshold), seuil 0,02, Max Samples 64.

## Tutoriel 4 — Mesurer (10 min)
Lancez le correcteur : plafond, bruit, réglages.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch10_02_cycles_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch10_02.py" -- --exercise cycles --debug
```

Remarque d'honnêteté : les panneaux Sampling > Render (case Noise Threshold, Max Samples), Light Paths > Max Bounces > Diffuse et Sampling > Lights (Light Tree) ont été relus dans `addons_core/cycles/ui.py`, pas regardés dans l'interface 5.3 ; les valeurs (plafond 0,013 → 0,33 ; bruit 0,049 → 0,0097) sont mesurées sur cette pièce à 128 × 72 en Cycles CPU sans débruitage ; une première version avec une lampe de 400 W saturait le mur (0 de bruit mesuré) : la lampe a été ramenée à 20 W ; Light Tree et caustiques ne sont pas mesurés ; le temps de rendu n'est pas évalué.

## Variante de contrôle

Dans deux copies, modifiez un seul type de rebond. Comparez une zone directement éclairée à une zone qui reçoit la lumière indirecte. **Preuve** Les deux zones et le temps calculé vous permettent d’expliquer quel réglage retirer si le plan ne profite pas de ce rebond.
