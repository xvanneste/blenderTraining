# Plan d’amélioration du cours Blender

Le [diagnostic](AUDIT_COURS_BLENDER.md) fixe le périmètre et la provenance des preuves. La cible reste Blender 5.3.0. Les identifiants, fichiers utiles et entrées de progression sont les références de travail.

| Ordre | Priorité | Périmètre | Travail | Critères de sortie |
|---|---|---|---|---|
| 1 | Critique | A01–A03, A15 · CH00.01, guide d’entrée et fiche de version | Première image portable, voie CPU et commandes de contrôle. | Une mire CPU sauvegardée, PNG rouvert, branches CPU et GPU testées au niveau de la scène. Sources officielles rattachées à 5.3. |
| 2 | Haute | A06, A09–A14 · CH00.02–08, CH01.01–14 | Expliciter les choix clavier, mode, prérequis, gestes et preuves autonomes. | Un débutant situe le geste et la sortie. Méthode de secours documentée. Essai humain identifié. |
| 3 | Haute | A04, A09–A12 · Outils, application et gabarits | Séparer les classes de validation et vérifier la concordance des spécifications. Ajouter charte, glossaire et index. | Couverture et test réels visibles. Liens et ancres vérifiés. La progression existante se recharge. |
| 4 | Haute | A07–A08 · CH02–08 | Contrôler maillages, UV, matériaux, instances, déformations, NLA et caches. | Valeurs, menus, limites, exemples et formats vérifiés dans leur contexte. |
| 5 | Haute | A07–A08 · CH09–12 et CH18 | Rejouer lumière, moteur, compositing, Grease Pencil et export. | Plan refait et résultat rouvert. Cas propres aux systèmes et périphériques documentés. |
| 6 | Haute | A05, A08 · CH13–17 | Développer les procédures courtes, rendre les décisions testables, préciser la revue des projets. | Cas nominal, cas fautif et variantes comparables. Exercices IA et pilote indiquent la provenance et la portée de la preuve. |
| 7 | Haute | A04–A12 · Cursus entier | Relecture croisée, contrôle des liens et ressources, réexécution des tests, revue pédagogique et plan d’entretien. | Couverture par chapitre traçable, preuve humaine ou absence explicite. Créer RAPPORT_QUALITE_FINAL.md à la clôture. |

## Critère de revue d’un chapitre

1. Lire le chapitre, ses dépendances, ses renvois et son exercice autonome. Noter la preuve existante.
2. Référencer les affirmations sensibles ou les rejouer. Distinguer fait technique, pratique recommandée et décision artistique.
3. Expliquer le concept avant la manipulation. Indiquer le départ, le mode, l’éditeur, l’action, la valeur et le résultat quand ils sont déterminants.
4. Vérifier le cas guidé, un défaut reproductible et une application autonome. Pour une décision de production, demander un livrable et une preuve de réussite.
5. Contrôler la source, l’affichage dans le site et les ressources. Consigner les points ouverts dans le suivi.

**Convention éditoriale** Le français explique le concept. L’intitulé anglais de l’interface reste identifiable. Employer Numpad 1 pour le pavé numérique et préciser le contexte de l’éditeur. Les durées restent indicatives jusqu’à observation.

## Critères encore ouverts

- Rejouer les gestes à la souris depuis les starters, en priorité pour les réglages de caméra, les outils de modélisation et la retopologie du visage. Les vérifications automatiques ciblent les fichiers déclarés et quelques opérations reproduites en mémoire.
- Observer la première heure avec le [protocole débutant](DOCUMENTATION/ESSAI_PREMIERE_SEANCE.md). Consigner l’autonomie, les erreurs de navigation et la durée observée.
- Examiner avec le [journal de refonte](SUIVI_REFONTE_BLENDER.md) la provenance des binaires divergents et les chemins des ressources distantes lors de la revue de chaque lot.
