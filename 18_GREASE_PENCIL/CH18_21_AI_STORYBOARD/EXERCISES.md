# CH18.21 — Exercices

## Exercice 1 — Facile : l'audit ⏱ 20 min
Sans ouvrir THEORY.md §3, listez toutes les erreurs de la `SHOTLIST` du starter et la règle violée
par chacune.

## Exercice 2 — Moyen : storyboard assisté contrôlé ⏱ 1 h 30
Corrigez la liste, lisez puis lancez `shot_prep.py`, vérifiez les plans, complétez `AI_LOG`.
Validation : `--exercise assist --render`.

## Exercice 3 — Difficile : votre propre assistance ⏱ 2 h
Si vous utilisez un assistant IA (avec votre accord sur ses conditions d'usage) : demandez-lui un
découpage de votre séquence (CH18.13) au format `code;valeur;sujet;côté;durée_s;note`, collez-le dans
`SHOTLIST`, contrôlez-le, générez les plans, puis dessinez les boards dans les caméras (CH18.20).
Sans IA : faites l'exercice avec votre propre découpage — le contrôle et le journal restent obligatoires.

### Grille d'auto-évaluation (sur 10)
| Critère | 0 | 1 | 2 |
|---|---|---|---|
| Erreurs repérées avec la règle correspondante | non | partiel | oui |
| Script lu avant exécution (vous savez ce qu'il supprime) | non | — | oui |
| Plans vérifiés par mesure, pas « à l'œil » | non | partiel | oui |
| Journal complet et honnête | non | partiel | oui |
| Décisions artistiques assumées (ce que vous avez changé) | non | partiel | oui |
**≥ 7/10** : acquis.

## Défis
- **Défi 1 :** ajoutez à `shot_prep.py` un mode « contrôle » qui refuse une liste contenant les erreurs
  du §3 (codes, côté, durées, total) — puis testez-le sur la proposition d'origine.
- **Défi 2 :** rédigez une « charte IA » d'une page pour votre projet (outils autorisés, données
  partagées, déclaration).

## Mini-projet — vers le projet obligatoire n° 7
Le storyboard + animatique d'un court de 3 à 5 min (projet n° 7, CH18.22) pourra utiliser une
assistance IA **contrôlée** : journal d'usage obligatoire dans le dossier du projet.
