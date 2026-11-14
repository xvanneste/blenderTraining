# CH01.08 — Cours théorique : collections, Outliner, parentage

## 1. Les collections
Une **collection** est un dossier d'objets. Elle sert à **organiser**, **masquer/afficher**,
**exclure du rendu**, **lier** dans d'autres fichiers (phase 16) et **instancier** (une
collection peut être réutilisée comme un seul objet).
- Un objet peut appartenir à **plusieurs** collections (`Shift+M` → *Link to Collection*) —
  à utiliser avec parcimonie.
- Les collections peuvent être imbriquées (`PROPS > FURNITURE > CHAIRS`).
- La **Scene Collection** est la racine : idéalement, aucun objet n'y reste « en vrac ».

| Action | Raccourci / geste |
|---|---|
| Déplacer vers une collection | `M` (menu : collections existantes, *+ New Collection*) |
| Lier à une collection supplémentaire | `Shift+M` |
| Nouvelle collection | Outliner : `RMB` → *New Collection* (ou icône en haut à droite) |
| Déplacer | Glisser-déposer dans l'Outliner (`Ctrl` pendant le dépôt = lier au lieu de déplacer) |
| Sélectionner le contenu | Outliner : `RMB` sur la collection → *Select Objects* |

## 2. La visibilité : cinq interrupteurs à ne pas confondre
Outliner → filtre (entonnoir) → *Restriction Toggles* permet d'afficher toutes les colonnes :
| Icône | Nom | Portée | Effet |
|---|---|---|---|
| ☑ case | *Exclude from View Layer* | View layer | La collection n'existe plus pour ce view layer (ni viewport, ni rendu) |
| ↖ flèche | *Disable Selection* | Global | Visible mais non sélectionnable (décor de fond, références) |
| 👁 œil | *Hide in Viewport* (`H`, `Alt+H`, `Shift+H`) | Temporaire, par view layer | Masque à l'affichage seulement ; **n'affecte pas le rendu** |
| 🖥 écran | *Disable in Viewports* | Global | Désactive dans tous les viewports (plus « fort » que l'œil) |
| 📷 appareil photo | *Disable in Renders* | Global | N'apparaît pas au rendu (mais reste visible pour travailler) |
Piège classique (CH00.01) : un objet visible dans la vue mais absent du rendu → icône
appareil photo de l'objet **ou de sa collection**.
`Ctrl`+clic sur l'œil d'une collection = l'isoler ; `Shift`+clic = agir aussi sur les enfants.

## 3. L'Outliner
- **Display Modes** : *View Layer* (défaut), *Scenes*, *Video Sequencer*, *Blender File*
  (tous les datablocks), *Data API*, *Library Overrides*, *Unused Data* (les données sans
  utilisateur, à purger ; appelé *Orphan Data* dans d'anciennes versions).
- Recherche (champ en haut) : filtre par nom.
- Double-clic : renommer ; `F2` aussi.
- Les icônes à droite d'un objet (triangle vert, clé à molette, sphère rouge…) sont ses
  données, modificateurs, matériaux : cliquables.

## 4. Le parentage
Un **enfant** suit les transformations de son **parent** (mais garde sa propre
transformation relative). Exemples : abat-jour → pied de lampe ; roues → voiture ;
caméra → chariot de travelling.
| Action | Raccourci |
|---|---|
| Parenter | sélectionner le(s) enfant(s), puis le parent **en dernier** (actif), `Ctrl+P` → *Object* |
| Parenter sans décalage visuel | `Ctrl+P` → *Object (Keep Transform)* |
| Retirer le parent | `Alt+P` → *Clear Parent* (l'enfant revient à sa transformation locale) ou *Clear and Keep Transformation* |
| Dans l'Outliner | glisser un objet sur un autre (`Shift` pendant le dépôt selon la version : suivre l'indication affichée) |
Parentage ≠ collection : la **collection** organise, le **parent** crée une relation de
mouvement.

## 5. En production
Chaque fichier suit la même structure de collections (convention d'équipe) : un layout
artist ouvre un plan et sait que les personnages sont dans `CHARACTERS`, les repères dans
`HELPERS` (désactivée au rendu). Les outils de pipeline s'appuient sur ces noms. Les assets
sont publiés **comme collections** pour être liés dans les plans.
