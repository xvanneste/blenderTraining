# CH10.07 — Cours théorique : Rendu distribué

## 1. La commande
`blender -b fichier.blend -o dossier/shot_#### -F PNG -s 1 -e 8 -a` : arrière-plan, sortie, format, plage, rendu d'animation.

## 2. L'ordre des arguments
Blender exécute les arguments dans l'ordre donné. Mesuré : « -a -s 1 -e 2 » rend les 6 images de la scène (plage ignorée) ; « -s 1 -e 2 -a » en rend 2.

## 3. Les sorties
-o : chemin avec ####. -F : format. -x : ajoute l'extension. Un dossier de sortie partagé impose des noms uniques par image.

## 4. Les morceaux
24 images sur 3 machines : 1–8, 9–16, 17–24. Pas de trou, pas de recouvrement (sinon une image est rendue deux fois ou jamais).

## 5. Les réglages de ferme
Output Properties > Output : Overwrite désactivé (ne pas écraser une image déjà là), Placeholders activé (réserver l'image dès le début du rendu pour qu'une autre machine la saute). Propriétés `use_overwrite` et `use_placeholder`.

## 6. L'exercice
Départ : -a avant -s dans la première commande, l'image 17 manque, mauvais réglages. Solution : trois commandes correctes, Overwrite off, Placeholders on.

## 7. Pièges
- « -a » au milieu de la ligne.
- Plages qui se chevauchent ou laissent un trou.
- Chemins de sortie relatifs à des machines différentes.
- Lancer sans --factory-startup une machine dont les préférences diffèrent (le correcteur l'ajoute).

## 8. Orchestration
À la main (une commande par machine), par script (CH13), ou avec un gestionnaire de ferme comme Flamenco : non testé ici.

Limites : une machine ; équilibrage non mesuré ; pas de réseau.
