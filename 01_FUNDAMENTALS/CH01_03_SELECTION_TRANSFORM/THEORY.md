# CH01.03 — Cours théorique : sélectionner et transformer

## 1. Sélectionné ≠ actif
- Plusieurs objets peuvent être **sélectionnés** (contour orange foncé).
- Un seul est **actif** (contour orange clair) : le dernier cliqué. C'est lui que montre
  l'éditeur Properties, et lui qui sert de référence pour beaucoup d'opérations
  (`Ctrl+L` Link, *Copy to Selected*, parentage…).
- `Shift`+clic sur un objet déjà sélectionné le rend actif ; un second `Shift`+clic le
  désélectionne.

## 2. Les outils de sélection (sélection au clic gauche)
| Méthode | Geste |
|---|---|
| Un objet | `LMB` |
| Ajouter / retirer | `Shift+LMB` |
| Tout / rien | `A` / `Alt+A` (ou double `A` rapide) |
| Inverser | `Ctrl+I` |
| Rectangle | `B` puis glisser (ou outil *Select Box* et glisser dans le vide) ; `Shift` pour retirer pendant le tracé… voir barre d'état |
| Cercle (pinceau) | `C`, molette = rayon, `LMB` peindre, `MMB` effacer, `Entrée`/`RMB` sortir |
| Lasso | `Ctrl+RMB` glissé |
| Par l'Outliner | clic, `Shift`/`Ctrl`+clic, `RMB` sur une collection → *Select Objects* |
| Par critère | menu *Select* : *All by Type*, *Grouped* (`Shift+G`), *Pattern…* (par nom, ex. `GEO_Pebble_*`) |

## 3. Transformer : les trois opérations
| Opération | Raccourci | Remise à zéro |
|---|---|---|
| **Déplacer** (*Grab/Move*) | `G` | `Alt+G` |
| **Tourner** (*Rotate*) | `R` (`R R` = rotation libre « trackball ») | `Alt+R` |
| **Mettre à l'échelle** (*Scale*) | `S` | `Alt+S` |

Pendant une transformation (après `G`, `R` ou `S`) :
| Touche | Effet |
|---|---|
| `X`, `Y`, `Z` | Contraindre à l'axe global ; une 2ᵉ pression = axe **local** ; une 3ᵉ = libre |
| `Shift+X`… | Exclure un axe (déplacer dans le plan YZ…) |
| Chiffres | Saisie numérique : `G X 2 Entrée` = 2 m sur X ; `-` pour négatif ; `R Z 45` ; `S 0.5` |
| `Ctrl` (maintenu) | Pas réguliers (snapping incrémental) |
| `Shift` (maintenu) | Précision (mouvement ralenti) |
| `LMB` / `Entrée` | Valider |
| `RMB` / `Échap` | Annuler |
| `MMB` | Choisir l'axe à la souris |

La **barre d'état** et l'en-tête de la vue affichent la valeur en cours (ex. `D: 2 m (2) along global X`).

## 4. Gizmos et outils
La barre d'outils (`T`) propose *Move*, *Rotate*, *Scale*, *Transform* : un **gizmo**
(poignées colorées) apparaît. Pratique pour débuter et pour la tablette. Les pros
utilisent surtout les raccourcis (plus rapides, précis au clavier). On peut aussi afficher
des gizmos en permanence via le menu *Gizmos* de l'en-tête.

## 5. Saisie dans la sidebar
`N` → onglet *Item* : *Location*, *Rotation*, *Scale*, *Dimensions*. Astuces :
- Cliquer-glisser verticalement sur plusieurs champs = les éditer ensemble.
- Taper une expression : `2*0.5`, `90` (degrés), `1.5m` ou `150cm` (unités).
- `Ctrl+C` / `Ctrl+V` sur un champ survolé = copier/coller la valeur.
- Clic droit sur un champ → *Copy to Selected* : copie la valeur sur toute la sélection ;
  maintenir `Alt` en glissant une valeur l'applique aussi à tous les objets sélectionnés.

## 6. Pourquoi la précision compte au cinéma
Une caméra qui doit refaire un mouvement, un accessoire qui doit être posé au même endroit
dans 20 plans, un décor monté à l'échelle : la précision numérique garantit la
**continuité** entre plans et entre artistes. « À peu près » se voit à l'image.
