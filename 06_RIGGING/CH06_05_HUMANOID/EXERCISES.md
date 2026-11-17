# CH06.05 — Exercices

## Exercice 1 — Facile : classer ⏱ 15 min
Pour DEF-spine, ORG-spine, MCH-torso.parent, torso, hand_ik.L : déformant, origine, mécanisme ou contrôleur ? (Réponses : déformant ; origine ; mécanisme ; contrôleur ; contrôleur.)

## Exercice 2 — Moyen : le rig ⏱ 3 h
Partez du starter : ajustez, générez, liez. Validation : `--exercise humanoid`.

## Exercice 3 — Difficile : les bras ⏱ 4 h
Les bras sont ajustés (tutoriel 1 bis). Allez plus loin : ajustez aussi les doigts phalange par phalange, puis ajoutez au correcteur un test de la main (hand_ik.L déplacée de (0 ; −0,2 ; 0,3) : les sommets de la main suivent à ± 5 cm, le coude plie vers l'arrière).

### Grille d'auto-évaluation (sur 10)
| Critère | 0 | 1 | 2 |
|---|---|---|---|
| Méta-rig mis à l'échelle (taille du rig = taille du corps) | non | partiel | oui |
| Rig généré et nommé RIG_Hero | non | partiel | oui |
| Corps lié (modificateur, groupes DEF-, poids normalisés) | non | partiel | oui |
| La racine et le pied IK entraînent le bon côté | non | partiel | oui |
| Bras ajustés à la pose du personnage | non | partiel | oui |
**≥ 7/10** : acquis.

## Défis
- **Défi 1 :** ajoutez un doigt supplémentaire au méta-rig.
- **Défi 2 :** masquez par script toutes les collections sauf Torso, Arm.L (IK) et Leg.L (IK).

## Mini-projet
Le rig complet de votre personnage principal (projet P6).
