# CH18.06 — Exercices

## Exercice 1 — Facile : le tour des modes ⏱ 10 min
Dans un fichier **File → New → 2D Animation** : dessinez trois traits (Draw), déplacez un point
(Edit, `G`), lissez un trait (Sculpt, outil *Smooth*), puis revenez en Object Mode et déplacez
l'objet entier. Notez pour chaque mode ce qu'affiche l'en-tête du viewport.

## Exercice 2 — Moyen : remettre de l'ordre ⏱ 15 min
Ouvrez la solution `COMPLETED_EXAMPLES/ch18_06_gp_scene_solution.blend`, enregistrez une copie,
puis : sortez COLOR du groupe CHAR, renommez GP_Background en `Stroke.001`, déplacez-le dans la
collection SET. Enregistrez, lancez le correcteur (il doit refuser), puis réparez tout et relancez
(il doit valider). Objectif : savoir lire les messages du correcteur.

## Exercice 3 — Difficile : la scène complète (SANS procédure) ⏱ 40 min
À partir du starter, réalisez la consigne du bloc README_EXERCICE (collection DRAWINGS,
GP_Character devant la maison avec calques LINE/COLOR/SKETCH et groupe CHAR, SKETCH verrouillé,
GP_Background derrière la maison, passe Z). Validation : `--exercise organize --render`.

### Grille d'auto-évaluation (sur 20)
| Critère | 0 | 1 | 2 |
|---|---|---|---|
| Noms conformes (GP_, calques en majuscules) | non | partiel | oui |
| Collection DRAWINGS, rien en vrac | non | partiel | oui |
| Calques à rôle clair (SKETCH / LINE / COLOR) | non | partiel | oui |
| Groupe CHAR utilisé | non | — | oui |
| SKETCH verrouillé et pâle | non | un des deux | oui |
| Personnage devant la maison | non | — | oui |
| Fond derrière la maison | non | — | oui |
| Rendu F12 : occlusion correcte (passe Z) | non | — | oui |
| Tout dans le cadre de CAM_Shot | non | partiel | oui |
| Temps < 40 min | > 60 | 40–60 | < 40 |
**≥ 14/20** : acquis.

## Défis
- **Défi 1 :** Add → Grease Pencil → **Object Line Art** sur la maison : observez le contour
  généré automatiquement (approfondi en CH18.08).
- **Défi 2 :** dessinez un nuage avec **Stroke Placement : Surface** directement sur la maison :
  le trait épouse le mur.

## Mini-projet — Un plan en trois profondeurs ⏱ 1 h
Dans le starter (ou votre propre décor de la phase 1), trois objets GP à trois profondeurs :
premier plan (feuillage qui encadre), plan moyen (personnage), fond (montagnes). Orbitez pour
montrer la profondeur, puis un rendu F12 avec passe Z. Réutilisez la composition de CH18.05.
Livrable : `PORTFOLIO/drawing/ch18_06_trois_profondeurs.png`.
