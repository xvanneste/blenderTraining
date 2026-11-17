# CH04.10 — Exercices

## Exercice 1 — Facile : diagnostiquer ⏱ 15 min
Une peau rendue « en plastique », un œil « mort », des cheveux « en plastique ». Cause pour chacun ? (Réponses : pas de sous-surface ; pas de Coat ; Principled BSDF au lieu du Hair BSDF.)

## Exercice 2 — Moyen : les quatre matériaux ⏱ 3 h
Partez du starter et construisez-les. Validation : `--exercise character --render`.

## Exercice 3 — Difficile : une peau plus foncée ⏱ 2 h
Réglez la peau pour un teint plus foncé (luminance ≥ 0,3) en gardant R > V > B et un rayon de sous-surface plausible ; comparez les rendus.

### Grille d'auto-évaluation (sur 10)
| Critère | 0 | 1 | 2 |
|---|---|---|---|
| Peau : sous-surface, rayon coloré, pores | non | partiel | oui |
| Œil : iris, sclère, Coat net | non | partiel | oui |
| Cheveux : Principled Hair BSDF | non | partiel | oui |
| Tissu : Sheen, rugosité, trame | non | partiel | oui |
| Rendus regardés et commentés | non | partiel | oui |
**≥ 7/10** : acquis.

## Défis
- **Défi 1 :** ajoutez une pupille noire (second seuil de la Color Ramp).
- **Défi 2 :** appliquez le matériau de cheveux à des courbes (Curves).

## Mini-projet
Les matériaux de peau, d'œil et de vêtement de votre personnage principal.
