# CH00.06 — Exercices

## Exercice 1 — Facile : créer le projet ⏱ 5 min
Tutoriel 1, puis ouvrez le projet dans Blender (tutoriel 2) et enregistrez le premier
fichier de layout au bon endroit avec le bon nom.

## Exercice 2 — Moyen : le projet déménage ⏱ 15 min
1. Copiez `STARTER_FILES/ch00_06_messy_scene_starter.blend` **et** le dossier
   `ASSETS/textures/` dans un dossier temporaire (ex. `C:\temp\demenagement\`), en gardant
   la même structure relative (`STARTER_FILES\` et `ASSETS\textures\` côte à côte).
2. Renommez le dossier d'origine `ASSETS\textures` en `textures_cache` (pour simuler la perte).
3. Ouvrez la copie : la texture est-elle trouvée ? (rendu Material Preview `Z` → *Material Preview*).
4. Réparez avec *File → External Data → Find Missing Files* (pointez le dossier copié), puis
   *Make Paths Relative*. Remettez le nom `textures` d'origine.
5. Expliquez en 3 phrases pourquoi le problème n'existerait pas avec des chemins relatifs.

## Exercice 3 — Difficile : remise aux normes complète (SANS procédure) ⏱ 15 min
Rendez `ch00_06_messy_scene_starter.blend` conforme : objets préfixés et parlants, aucun
`.001`, collections `SET/PROPS/LIGHTS/CAMERAS`, matériaux `MAT_`, texture en relatif.
Enregistrez `ch00_06_messy_scene_<prenom>_v001.blend` et validez :
`… --python-exit-code 1 --python "SCRIPTS\validate_ch00_06.py" -- --exercise naming`
Barème (15 pts) : objets conservés 1 · objets 3 · collections 3 · matériaux 3 · images 3 ·
collections requises 2.

## Défis
- **Défi 1 :** modifiez `bcma_create_project.py` pour ajouter un dossier `01_preprod/sound_design`.
- **Défi 2 :** créez dans les paramètres du projet une bibliothèque d'assets pointant sur
  `02_assets` ; vérifiez qu'elle apparaît dans l'Asset Browser.

## Mini-projet — Projet P0, partie « arborescence » ⏱ 20 min
Créez le projet de votre futur court-métrage A (phase 15) : nom définitif, 3 séquences,
4 plans par séquence, README complété (logline provisoire, liste des dossiers, règles de
nommage). Grille : structure 30 · nommage 30 · README 20 · projet Blender ouvert et
fichier v001 enregistré 20.

## Tests chronométrés
| Test | Cible |
|---|---|
| Renommer 10 objets avec Batch Rename | 1 min |
| Rendre relatifs tous les chemins d'un fichier | 15 s |
| Créer un projet complet par script | 30 s |
