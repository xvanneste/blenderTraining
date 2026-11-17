# CH04.11 — Exercices

## Exercice 1 — Facile : classer ⏱ 15 min
Pour chaque image, sRGB ou Non-Color ? Peinture de visage, masque de rouille, normal map, carte de métal, texture de brique en couleur, HDRI d'éclairage. (Réponses : sRGB ; Non-Color ; Non-Color ; Non-Color ; sRGB ; linéaire — souvent déjà la valeur par défaut d'un .hdr.)

## Exercice 2 — Moyen : la planche ⏱ 1 h 30
Partez du starter et corrigez tous les réglages. Validation : `--exercise color --render`.

## Exercice 3 — Difficile : comparer les vues ⏱ 1 h 30
Rendez la scène en AgX, Filmic, ACES 2.0 et Khronos PBR Neutral ; mesurez les valeurs du panneau lumineux pour chacune et classez-les par conservation de la teinte. Le correcteur doit rester vert avec chacune.

### Grille d'auto-évaluation (sur 10)
| Critère | 0 | 1 | 2 |
|---|---|---|---|
| Espaces des trois images corrects | non | partiel | oui |
| View Transform tone-mapped et Look cohérent | non | partiel | oui |
| Exposure modérée, Gamma 1 | non | partiel | oui |
| Sortie maître EXR | non | partiel | oui |
| Rendu comparé et commenté | non | partiel | oui |
**≥ 7/10** : acquis.

## Défis
- **Défi 1 :** montrez l'effet d'un normal map en sRGB (relief faux) sur un cas réel de CH04.07.
- **Défi 2 :** configurez une vue False Color pour contrôler l'exposition d'un plan, puis revenez à la vue de livraison.

## Mini-projet
Une fiche « Couleur » de votre projet : View Transform, Look, formats, conventions d'espaces d'images.
