# Modèle de chapitre et de leçon

Chaque chapitre vit dans `NN_PHASE/CHNN_MM_NOM/` et contient au minimum :

```
CHNN_MM_NOM/
├── README.md            Fiche d'identité : intro, prérequis, objectifs, durée, plan, livrables
├── LESSON.md            Les leçons au format A→I (voir ci-dessous)
├── THEORY.md            Le cours théorique détaillé (A. Comprendre, version longue)
├── TUTORIAL.md          Démonstrations guidées pas à pas (B. Observer + C. Reproduire)
├── EXERCISES.md         Facile / moyen / difficile / défis / mini-projet / tests chronométrés
├── QUIZ.md              Questions (sans réponses)
├── SOLUTIONS.md         Corrigés des exercices et du quiz
├── TROUBLESHOOTING.md   Erreurs courantes → causes → solutions
├── RESOURCES.md         Sources vérifiées, documentation officielle, licences
├── STARTER_FILES/       .blend et fichiers de départ des exercices
├── COMPLETED_EXAMPLES/  Versions corrigées distinctes (+ rendus de référence)
├── ASSETS/              Ressources propres au chapitre
└── SCRIPTS/             Scripts Python du chapitre (testés)
```

## Format d'une leçon

```markdown
## Leçon X — Titre
**Niveau :** débutant | intermédiaire | avancé | expert
**Durée estimée :** X h
**Prérequis :** …
**Compétences visées :** CNN.MM.x

### A. Comprendre
Ce que c'est · à quoi ça sert · pourquoi ça existe · quand l'utiliser · analogies · schéma.

### B. Observer
Démonstration complète, commentée.

### C. Reproduire
Étapes numérotées : où cliquer · raccourci · paramètre · résultat attendu · ✅ vérification.

### D. Pratiquer
- Facile — appliquer
- Moyen — combiner
- Difficile — résoudre sans procédure complète

### E. Produire
Mini-projet à visée cinématographique.

### F. Optimiser
Méthode manuelle → méthode pro → méthode automatisée/IA (avec compromis).

### G. Évaluer
Renvoi vers QUIZ.md, grille de notation, test pratique.

### H. Consolider
Résumé · raccourcis · erreurs fréquentes · révision.

### I. Livrables
Fichiers attendus, nommés selon DOCUMENTATION/CONVENTIONS.md.
```

## Grille d'évaluation standard (sur 100)

| Critère | Points |
|---|---|
| Résultat conforme à la consigne | 30 |
| Propreté technique (nommage, organisation, absence d'erreurs) | 20 |
| Qualité artistique / lisibilité | 20 |
| Autonomie (sans tutoriel, problèmes résolus seul) | 15 |
| Vitesse (temps cible respecté) | 15 |

Seuils : < 50 à refaire · 50–69 à consolider · 70–84 acquis · ≥ 85 maîtrisé.
