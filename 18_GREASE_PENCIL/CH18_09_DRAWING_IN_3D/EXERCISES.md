# CH18.09 — Exercices

## Exercice 1 — Facile : un cube de traits ⏱ 15 min
Nouveau fichier General, objet GP Blank. Dessinez les 6 faces d'un cube de 2 m en utilisant
**seulement** Drawing Plane (Front / Side / Top) et le curseur 3D déplacé à ±1 m. Orbitez : les
traits doivent former un cube fermé.

## Exercice 2 — Moyen : la parallaxe ⏱ 20 min
Dans la solution (copie), animez la caméra : image 1 X = −2, image 48 X = +2 (`I` sur Location).
Lisez l'animation : le premier plan défile plus vite que le fond. Expliquez en deux phrases
pourquoi un dessin plat ne produirait pas cet effet.

## Exercice 3 — Difficile : le décor complet (SANS procédure) ⏱ 60 min
Réalisez la consigne du bloc README_EXERCICE du starter : 4 calques (BG loin, MID, FG proche,
GROUND à plat sur ≥ 6 m), passe Z, tout visible dans CAM_Layout.
Validation : `--exercise set --render`.

### Grille d'auto-évaluation (sur 20)
| Critère | 0 | 1 | 2 |
|---|---|---|---|
| 4 plans de profondeur distincts | < 3 | 3 | 4 |
| Taille cohérente avec la distance | non | partiel | oui |
| Sol dessiné à plat (Top) | non | partiel | oui |
| Composition en vue caméra (CH18.05) | non | moyenne | bonne |
| Premier plan qui encadre sans masquer | non | partiel | oui |
| Parallaxe visible en orbitant | non | faible | nette |
| Passe Z, occlusion correcte au rendu | non | — | oui |
| Calques bien nommés et utilisés | non | partiel | oui |
| Référence utilisée puis rangée | non | — | oui |
| Temps < 60 min | > 90 | 60–90 | < 60 |
**≥ 14/20** : acquis.

## Défis
- **Défi 1 :** **Stroke Placement : Surface** — dessinez une fissure sur le sol et un graffiti sur
  la façade d'un cube ; réglez l'*Offset* pour éviter que le trait ne disparaisse dans la surface.
- **Défi 2 :** dupliquez la scène (*New Scene → Linked Copy*) et changez seulement la caméra :
  deux plans du même décor.

## Mini-projet — Travelling dans un décor dessiné ⏱ 2 h
Décor de 5 profondeurs (dont sol et ciel), caméra animée sur 96 images (travelling latéral ou
avant), un personnage GP au plan moyen. Rendu en séquence PNG puis lecture (*View → Render
Playblast* pour un aperçu rapide). Livrable : `PORTFOLIO/drawing/ch18_09_travelling/`.
