# Audit et mise en œuvre de la modélisation pratique

L’inventaire avant la dernière génération a couvert environ 4 000 fichiers, dont les supports Markdown, scènes Blender, ressources, quiz et spécifications de test. La revue de contenu a ciblé les fondamentaux, la modélisation, la sculpture et les exercices de rig qui mènent au personnage humain.

| Fonction existante | Intégration dans le parcours |
|---|---|
| Site HTML/CSS/JavaScript hors ligne et génération avec Python | Un sommaire et des routes d’atelier dans la même application. Le navigateur sert à lire, vérifier et reprendre le travail fait dans Blender. |
| Chapitres avec théorie, tutoriels, exercices, quiz, corrigés et dépannages | Les chapitres gardent leurs identifiants. Des liens relient les chapitres de modélisation et de sculpture aux nouveaux ateliers. |
| Acquis, scores et favoris dans `localStorage` sous `bcma.v1` | Ajout de cases par étape et d’un lien de reprise. Les anciennes données restent utilisables. |
| Scènes, rendus, schémas et quelques vidéos | Les ateliers distinguent schéma, rendu non interactif, gabarit et scène éditable. Les nouveaux exemples se contrôlent en filaire dans Blender. |
| Correcteurs Blender et tests de contre-exemples | Les tests de la refonte ciblent les livrables. Le projet humain demande aussi une revue visuelle et deux preuves de pose, qui relèvent de l’apprenant. |

Le parcours commence avec des manipulations sur une vraie cage, puis demande à l’élève de refaire un geste sur une variante. Les neuf projets introduisent progressivement des contraintes de forme et d’assemblage. Le module humain explique l’alignement photo, l’extrusion des régions, le flux des arêtes et une flexion vérifiable. Le dernier projet demande une livraison versionnée et un export réimporté.

Les nouvelles scènes sont générées avec `build_assets.py` et `build_human_cage.py`. Le navigateur se teste après `python TOOLS/build_site.py` avec `TOOLS/test_practical_site.cjs` et une installation Playwright existante. Les scènes, la déformation et la réimportation GLB se vérifient avec `test_assets.py` lancé depuis Blender 5.3 en arrière-plan.

Les [captures Blender 5.3](MEDIAS_A_PRODUIRE.md) sont intégrées aux tutoriels. Le [projet final](projet-humain.md) fournit le personnage avancé, son GLB animé et la scène réimportée. Le script de publication contrôle l’échelle, les maillages pondérés, l’animation et la texture réimportée. Le cours utilise une paire de gabarits synthétiques. L’élève peut les remplacer par des photographies autorisées en suivant la leçon de calibration. Le [protocole d’essai débutant](ESSAI_DEBUTANT.md) est prêt pour une séance.
