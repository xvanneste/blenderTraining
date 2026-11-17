# CH07.05 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch07_05_bounce_starter.blend`. Sauvegardez sous `ch07_05_bounce_starter_<prenom>_v001.blend`.

## Tutoriel 1 — Calculer (20 min)
Contacts aux images 19, 44, 62. Hauteur du sommet entre deux contacts séparés de T images : h = 9,81 × (T/24)² / 8. Entre 19 et 44 (T = 25) : 1,33 m, à l'image 31,5.

## Tutoriel 2 — Poser les clés (20 min)
Z : image 1 : 2,759 ; 19 : 0 ; 31,5 : 1,33 ; 44 : 0 ; 53 : 0,69 ; 62 : 0 ; 72 : 0.

## Tutoriel 3 — Les poignées (20 min)
Graph Editor, courbe Z Location : sommets en Auto Clamped ; clés de contact (images 19, 44, 62) : V > Vector.

## Tutoriel 4 — Regarder (15 min)
Activez l'affichage des fantômes (onion skin / motion paths) ou comptez les écarts : serrés au sommet, larges au contact.

## Tutoriel 5 — Le repos (5 min)
Image 72 : Z = 0 (clé déjà posée) ; vérifiez que la balle reste au sol de 62 à 72.

## Vérifier
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch07_05_bounce_starter_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch07_05.py" -- --exercise bounce --debug
```

Remarque d'honnêteté : la solution est générée par script avec des poignées exactes (`FREE`) ; la variante à poignées Vector aux contacts, que suivrait un apprenant, est acceptée par le correcteur (accélération médiane −0,0142). Les noms d'options d'affichage (fantômes, trajectoires) et menus du Graph Editor n'ont pas été relus dans l'interface 5.3 ; V (type de poignée) est vérifié dans la keymap par défaut. La chronophotographie (numpy) a été regardée : points serrés aux sommets, écartés aux contacts.

## Variante de contrôle

Choisissez deux arcs et marquez les moments où la vitesse apparente change. Gardez le même nombre total d’images et redistribuez trois clés intermédiaires. **Preuve** La lecture montre l’effet de l’espacement, même si la durée globale reste identique.
