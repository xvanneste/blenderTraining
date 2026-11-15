# CH03.03 — Exercices

## Exercice 1 — Facile : un seul volume ⏱ 45 min
Starter « remesh » : ponts (cou, abdomen, épaules), jointure, Voxel Remesh 0,012 : un seul morceau
fermé, en quads, taille conservée. Validation : `--exercise remesh --render`.

## Exercice 2 — Moyen : Multiresolution ⏱ 45 min
Starter « multires » : 5 niveaux, Sculpt = Render = 5, Viewport plus bas, base intacte ; quelques
rides sculptées (non vérifiées). Validation : `--exercise multires`.

## Exercice 3 — Difficile : trois tailles de voxel ⏱ 1 h
Sur trois copies de votre `SCULPT_Body` : Voxel Size 0,03 / 0,012 / 0,005. Notez le nombre de faces,
la fluidité en Sculpt Mode, ce qui disparaît (doigts, détails fins). Remplissez `DECISIONS`
(`--exercise decide`) et justifiez par écrit votre choix de taille pour un blocage.

### Grille d'auto-évaluation (sur 10)
| Critère | 0 | 1 | 2 |
|---|---|---|---|
| Comprend pourquoi les masses doivent se chevaucher | non | partiel | oui |
| Taille de voxel adaptée à l'étape | non | partiel | oui |
| Multires réglé pour rester fluide | non | partiel | oui |
| Sait ce que DynTopo détruit | non | partiel | oui |
| Choix de méthode justifiés | non | partiel | oui |
**≥ 7/10** : acquis.

## Défis
- **Défi 1 :** ajoutez des oreilles avec DynTopo, puis régularisez avec Voxel Remesh.
- **Défi 2 :** QuadriFlow Remesh (bouton voisin) sur `SCULPT_Body` : comparez avec Voxel (topologie,
  temps de calcul).

## Mini-projet
Un personnage de votre invention : masses → remesh → grandes formes sculptées → sauvegardes par
étape. Il servira de base aux chapitres suivants (stylisé, CH03.04).
