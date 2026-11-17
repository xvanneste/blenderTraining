# Audit pédagogique du 16 novembre 2026

Le cours dispose des exercices nécessaires pour aller jusqu'à un premier plan animé. Le [parcours du premier plan](PARCOURS_PREMIER_PLAN.md) les relie en quatre jalons. Chaque jalon associe un livrable court et une variante à refaire sans aide. Les estimations du parcours sont à mesurer avec un débutant.

| Constat | Correction ou contrôle suivant |
|---|---|
| Le démarrage demandait de choisir un rythme pour le cursus complet avant le premier exercice. | Le guide de démarrage ouvre désormais sur une première image, puis une scène, un mouvement et une vidéo. |
| Le suivi cumulait plusieurs évaluations à chaque chapitre. | Le tableau des jalons recueille le fichier produit, la variante réussie sans aide et le geste à réviser. Les critères du cursus complet restent indiqués pour les projets de phase. |
| Les 5 h de CH03.05 et son exercice de variation de 3 h se recoupaient dans le parcours conseillé. | Les 5 h couvrent le parcours essentiel avec les exercices 1 et 2. La variante a son propre temps. Le tutoriel donne un critère visuel pour arrêter le lissage avant de passer aux détails. |
| Les résultats techniques étaient parfois présentés comme preuve d'une reprise complète du tutoriel. | Le rapport généré précise la portée des tests. Le lanceur vérifie le verdict écrit du correcteur et le code de sortie de Blender. |
| La phase Python ouvre sur des exercices de fonctions, puis passe à des outils utilisables en production. | Les ressources officielles précisent quoi lire et quel résultat essayer pour chaque chapitre prévu. |

## Contrôles

- Inventaire de l'ensemble du cursus et contrôle automatisé des liens Markdown locaux, des métadonnées de chapitre, des quiz et des chemins des fichiers appelés par les tests.
- Quarante tests relancés dans Blender sans reconstruire les scènes, sur sept chapitres qui couvrent l'installation, le rendu, le rigging, l'animation, l'export, Python et Grease Pencil.
- Le contrôleur du manifeste a recensé zéro chemin ou champ obligatoire en erreur et 46 empreintes divergentes. Les fichiers signalés étaient déjà présents dans le dossier. Vérifier l'origine de leur régénération avant d'actualiser les empreintes.

La revue pédagogique porte sur le démarrage, le parcours du premier plan, le buste réaliste et la phase Python. Une séance observée reste nécessaire pour mesurer le temps du parcours, vérifier les commandes en interface et voir si la variante autonome révèle les blocages. Commencer par la première image, puis faire exporter un plan à une personne qui vient d'acquérir les bases de Blender.

[État de production](../FINAL_AUDIT.md) · [Ressources Python](../13_PYTHON_AUTOMATION/RESSOURCES_PHASE_13.md)
