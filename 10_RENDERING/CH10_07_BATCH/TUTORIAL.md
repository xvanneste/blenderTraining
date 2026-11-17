# CH10.07 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch10_07_batch_starter.blend`. Sauvegardez sous `ch10_07_batch_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Lire le plan (5 min)
Text Editor : ouvrez le texte BATCH : trois commandes.

## Tutoriel 2 — Corriger les commandes (15 min)
Mettez « -a » en dernier sur chaque ligne ; remplacez la dernière plage par 17–24.

## Tutoriel 3 — Les réglages de ferme (5 min)
Properties > Output > Output : décochez Overwrite, cochez Placeholders.

## Tutoriel 4 — Mesurer (10 min)
Lancez le correcteur : il lance les trois commandes et compte les images.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch10_07_batch_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch10_07.py" -- --exercise batch --debug
```

Remarque d'honnêteté : le correcteur EXÉCUTE vos commandes avec le vrai Blender (liste blanche : -b -o -F -s -e -a -x -t, rien d'autre ; --factory-startup ajouté), une commande à la fois, dans un dossier temporaire ; la règle « -a en dernier » est mesurée (« -a -s 1 -e 2 » rend 6 images, « -s 1 -e 2 -a » en rend 2) ; Overwrite et Placeholders sont des propriétés vérifiées par l'API ; les libellés de l'interface (Output > Overwrite, Placeholders) n'ont pas été regardés à l'écran ; Flamenco n'a été ni installé ni testé : le chapitre ne traite que la ligne de commande ; une seule machine.

## Variante de contrôle

Rendez d’abord une image clé, puis un lot de trois ou quatre images. Faites un inventaire trié et retirez une image dans une copie du lot pour essayer la reprise. **Preuve** La commande place les images dans le bon dossier, et une image manquante reste détectable même si Blender s’est fermé sans erreur.
