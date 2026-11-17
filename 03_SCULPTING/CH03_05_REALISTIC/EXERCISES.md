# CH03.05 — Exercices

## Exercice 1 — Facile : mesurer une tête ⏱ 45 min
Sur une photo de face ET de profil (la vôtre ou une photo libre de droits), tracez : couronne, racine des
cheveux, sourcils, base du nez, menton, ligne des yeux. Notez en pourcentage de la hauteur de tête : position
des yeux, pointe du nez. Comparez au tableau de THEORY.md §2 : de combien ce visage s'écarte-t-il ?

## Exercice 2 — Moyen : le buste réaliste ⏱ 3 h
Votre buste `SCULPT_Bust` + `EYE_L` / `EYE_R` : un volume fermé, socle plat, échelle réelle (buste 38–70 cm,
tête 19–27 cm), yeux à mi-hauteur de la tête, nez en saillie (≈ 2–5 cm devant la joue), symétrie X, plis
secondaires visibles, grain de peau. Validation : `--exercise bust --render`.

## Exercice 3 — Variante autonome : deux âges ⏱ 3 h supplémentaires
À partir de votre buste, deux variantes en ne changeant que les proportions et les secondaires : « 25 ans »
(plis légers) et « 70 ans » (poches, plis naso-géniens profonds, front ridé). Les deux doivent passer le
correcteur. Question : qu'est-ce qui, dans la **forme** (pas dans les plis), change avec l'âge ?

### Grille d'auto-évaluation (sur 10)
| Critère | 0 | 1 | 2 |
|---|---|---|---|
| Proportions justes (yeux à mi-hauteur, tiers du visage) | non | partiel | oui |
| Plans et transitions de face, de profil et de trois-quarts | Les volumes se lisent comme des blocs collés. | Les raccords passent de face, mais un bourrelet reste net en lumière rasante. | Les raccords sont continus dans les trois vues et les pommettes restent lisibles. |
| Détails secondaires lisibles | non | partiel | oui |
| Détails tertiaires (grain) présents sans bruit parasite | non | partiel | oui |
| Un caractère se lit sans texture ni couleur | non | partiel | oui |
**≥ 7/10** : acquis.

## Défis
- **Défi 1 :** un buste de profil « à la médaille » : nez, lèvres, menton justes, sans la vue de face.
- **Défi 2 :** introduire une légère asymétrie volontaire (sourcil, coin de bouche) et garder le correcteur vert.

## Mini-projet
Un portrait d'un personnage de votre mini-court : buste réaliste rendu de face et de trois-quarts, éclairage
latéral (CH09.*) pour révéler les plans, et une fiche des mesures (yeux, nez, tiers) en une page.
