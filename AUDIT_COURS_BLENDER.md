# Audit du cours Blender

## Périmètre et preuves au 17 novembre 2026

Le [programme](CURRICULUM.md) fournit 199 chapitres répartis en 19 phases. L’inventaire a recensé 4 589 fichiers sous la racine, hors métadonnées Git, caches Python et fichiers de sauvegarde Blender. Il comprend 2 075 fichiers Markdown, 926 fichiers .blend repérés sur disque, 334 PNG, des scripts, des vidéos, des projets et des propositions. Le manifeste contient 1 777 entrées. Des ressources sont mutualisées.

Les contrôles ont chargé les neuf documents et le quiz de chaque chapitre. Ils ont vérifié les cibles locales des liens Markdown reconnus, l’existence des ressources dans le manifeste et des fichiers déclarés pour les tests, la structure des quiz et l’identité textuelle stricte des tutoriels et théories après normalisation des blancs. Ces contrôles n’ont signalé aucune anomalie. Les ancres, liens distants et chemins en prose demandent un contrôle séparé. CH00.01 et CH13.03 n’ont pas de fichier chapter.json. Les 197 autres chapitres déclarent des prérequis.

L’historique enregistre 959 contrôles réussis. 177 chapitres ont une spécification et des résultats, dont 159 avec cas accepté et refusé. 22 chapitres sont documentaires. Un test de résultat final ne démontre pas le rejeu des étapes guidées. Un rejeu de tutoriel est identifiable par son nom dans les spécifications. D’autres essais consignés dans le journal nécessitent de retrouver leur trace.

Le tableau nominatif est un triage des 199 chapitres. Il prend en compte la structure, les preuves, les prérequis, les occasions de pratique et la profondeur repérable. La relecture ligne à ligne, le rejeu contextuel, la précision de toutes les opérations, la revue de clarté et l’observation de la difficulté réelle restent à mener par lot. Aucun tutoriel ou chapitre théorique entier n’est identique après normalisation. Les répétitions partielles n’ont pas encore été départagées entre rappels et doublons.

## Version et public

La cible reste **Blender 5.3.0**, build Windows Release 02f0899d78e3. Le binaire local a donné Python 3.13.13, le moteur de démarrage BLENDER_EEVEE, AgX et une sortie IMAGE/PNG. La version 5.3 est stable depuis le 10 novembre 2026. La 5.2 LTS constitue une branche de maintenance distincte. L’accès direct à plusieurs pages anglaises du manuel via l’outil web a renvoyé HTTP 402. Les extraits indexés orientent les recherches. Les libellés concernés nécessitent une preuve d’interface ou d’API quand le texte officiel est inaccessible. [Publication officielle 5.3](https://www.blender.org/releases/5-3/) · [Publication 5.2 LTS](https://www.blender.org/releases/5-2/)

Le lecteur entre en débutant absolu avec l’interface anglaise et la keymap Blender par défaut. Certains premiers chapitres supposent Windows, le terminal, le clic gauche, le pavé numérique ou un GPU Cycles. Expliciter ces hypothèses à chaque point d’usage rend le parcours autonome. Les temps d’apprentissage et plusieurs variantes matérielles nécessitent des essais séparés.

## Architecture, progression et domaines

- Le programme et les codes structurent les README de phase, les leçons et le site. Les neuf documents séparent théorie, procédure, exercices, corrigé, dépannage et ressources. Les quiz JSON alimentent la version interactive. Les fiches soutiennent la consultation ponctuelle.
- Le [premier plan](DOCUMENTATION/PARCOURS_PREMIER_PLAN.md) propose quatre livrables. Le [parcours pratique de modélisation](02_MODELING/PARCOURS_PRATIQUE/README.md) ajoute suivi, quiz, scènes et variantes. Le storyboard de la phase 18 est un prérequis de production dès les phases 15–16, malgré son numéro. Les dépendances de phase figurent dans le [suivi de production](TASKS.md). Le graphe de prérequis pédagogiques fin reste à expliciter.
- Les projets P1 à P12 ont chacun leur dossier. Les phases suivantes mutualisent le présentoir, le dossier hybride, le court et le pilote. Les propositions humaines et la cage apportent des référents de pratique. Un artefact, une manipulation contrôlée et une revue de production donnent des preuves complémentaires.
- Fondamentaux, modelling, sculpt, UV, matériaux, lumière, rendu, compositing, animation, NLA, Geometry Nodes, simulations, Python et production sont représentés. L’interopérabilité est répartie entre sauvegarde, mocap, humain et livraison. Il reste à vérifier les procédures USD, Alembic, FBX et glTF, leur aller-retour et la séparation des systèmes de particules historiques et actuels.

## Problèmes et corrections envisagées

| ID | Gravité | Localisation | Constat | Correction envisagée |
|---|---|---|---|---|
| A01 | Critique | CH00.01 exercices 1–2 et correcteur testcard | Le parcours impose GPU Compute. Le rendu de contrôle utilise déjà le CPU. | Créer une voie CPU explicite, préserver l’exigence GPU du cas GPU et tester les deux. |
| A02 | Haute | CH00.01 tutoriel et exercices | Le tutoriel donne un chemin du poste auteur. Le premier F12 produit un Render Result et l’exercice ne demande aucun PNG enregistré. Le GPU et le terminal arrivent tôt. | Commencer par un PNG et un .blend rouvert. Tester une commande portable et donner une voie GPU en approfondissement. |
| A03 | Haute | Fiche de compatibilité, CH00.01 et CH12.06 | La fiche cite FFMPEG parmi les formats d’image et fonde la publication sur des sources secondaires. | Relever les réglages par RNA, distinguer image et vidéo, citer la Foundation et le manuel versionné. |
| A04 | Haute | academy_status.py, FINAL_AUDIT.md et site | Le même libellé couvre des contrôles automatiques et documentaires. Les résultats sont agrégés par nom de dossier. | Afficher portée et dates. Vérifier la correspondance entre spécification actuelle et preuves. Séparer couverture, tests et validation pédagogique. |
| A05 | Haute | CH13.04–CH17.10 | Les sections théoriques comptent moins de 110 mots au repérage. Des actions avancées demandent d’expliciter décisions, gestes et preuves comparées. | Mesurer la profondeur par l’utilité. Ajouter des cas limites et procédures rejouables là où les étapes manquent. |
| A06 | Haute | START_HERE, CH00–01, phases 7, 15 et 18 | Le démarrage promet un correcteur partout. Des parcours accélérés atteignent caméra ou export sans expliciter ce qu’on reprend d’une scène fournie. | Donner le premier geste, sa preuve et une variante. Lier les dépendances au moment d’usage. |
| A07 | Haute | CH08.04, CH08.08, CH10.01–03, CH12.05–06 et CH18.06–09 | Zones sensibles aux versions et au matériel. Les tests de fichiers ne démontrent pas tous les menus et leurs effets. | Comparer au manuel 5.3, rejouer les manipulations et exposer les configurations vérifiées. |
| A08 | Haute | CH02, CH07.14, CH12.06 et CH16.08 | Les échanges sont répartis. Certains exemples sont vérifiés, dont le GLB humain. Les limites transverses sont difficiles à retrouver. | Créer un guide de choix par usage et une preuve par format réellement testé. |
| A09 | Moyenne | Conventions, génération du site et métadonnées | Num 1 et Numpad 1 alternent. Les liens Markdown renvoient souvent à la source. Les en-têtes HTML générés n’ont pas d’identifiants. | Définir une notation et vérifier les ancres, liens et renvois contextuels. |
| A10 | Moyenne | Démarrage, leçons et exercices | Plusieurs chronos arrivent tôt. Les durées n’ont pas été observées avec des débutants. Certains exercices autonomes sont difficiles à retrouver par repérage. | Évaluer d’abord un résultat et sa reprise autonome. Revoir les durées après observation. |
| A11 | Moyenne | Ressources et glossaire | Le repérage des liens Markdown externes dans les neuf documents ne trouve que cinq chapitres. Les références en texte libre demandent une vérification. | Ajouter les références versionnées près des affirmations sensibles et indexer les noms d’outils. |
| A12 | Moyenne | Gabarits, leçons et rappel des acquis | Beaucoup de récurrences tiennent au format commun. Le repérage ne trouve pas de synthèse sous les titres ciblés. | Donner un rappel utile au point d’usage et créer une synthèse propre à la compétence quand elle apporte une preuve supplémentaire. |

## Constats confirmés pendant le premier lot

| ID | Gravité | Localisation | Constat vérifié | Correction ou suivi |
|---|---|---|---|---|
| A13 | Haute | CH00.02, profil de préférences | En arrière-plan avec un profil neuf, Blender 5.3 expose show_statusbar_vram en lecture seule. Le profil interrompait l’enregistrement au lieu d’appliquer les réglages disponibles. | Ignorer explicitement l’option facultative dans ce contexte. Tester sauvegarde, relecture et restauration en profil isolé. |
| A14 | Haute | CH00.03, théorie, estimateur et correcteur | La docstring prétendait évaluer d’autres modificateurs. Le contrôle des 200 galets ignorait leur activation au rendu. | Définir le périmètre de l’estimation. Vérifier les flags et l’inclusion des collections du calque évalué. Tester les objets masqués. |
| A15 | Haute | Fiche de compatibilité, wrapper PowerShell | La procédure de migration pointait vers un lanceur qui reconstruit les scènes puis recalcule les empreintes. | Exécuter d’abord les tests sans reconstruire, puis isoler tout essai génératif sur une copie de travail. |

## Constats confirmés lors de la reprise

| ID | Gravité | Localisation | Constat vérifié | Correction ou suivi |
|---|---|---|---|---|
| A16 | Haute | Commandes Blender des leçons, projets, gabarits et scripts | `--python-exit-code` placé après le script laissait au processus un code 0 lors d’une exception. L’option placée avant le script a produit le code 7 demandé par l’essai. | Corriger l’ordre des options et contrôler les commandes restantes. |
| A17 | Haute | CH01.05, tutoriel et scène corrigée | Le pli du toit produisait une face de surface nulle et quatre arêtes hors variété. Le correcteur acceptait la scène. | Fusionner les sommets superposés dans la procédure, contrôler le maillage et conserver l’ancien corrigé comme cas refusé. |
| A18 | Moyenne | CH01.14, correcteur du premier rendu | Le réglage CPU valide était refusé. | Contrôler les deux réglages avec la même scène. Conserver un essai réel de rendu CPU et signaler la vérification matérielle GPU ouverte. |
| A19 | Moyenne | CH00.05 et CH00.07, installation et restauration | Les procédures mélangeaient parfois les ressources du cours et les préférences de l’utilisateur. Le test de récupération était difficile à isoler. | Utiliser un profil temporaire pour les essais d’installation et une copie de travail pour la récupération. |
| A20 | Haute | Projet P1, brief et correcteur | Le dossier ne fournissait aucun corrigé. Le correcteur confondait certains emplacements matériau avec des matériaux réellement assignés. | Livrer une référence éditable et deux rendus. Vérifier les matériaux assignés aux faces et tester deux variantes fautives. |
| A21 | Haute | ASSET_MANIFEST.json, scènes de CH00, CH01 et CH06.05 | Après mise à jour des empreintes des scripts, 42 binaires diffèrent encore. Dans 33 cas, l’empreinte enregistrée correspond exactement à HEAD. Les neuf autres fichiers sont absents de HEAD. | Préserver les deux états. Rechercher la provenance des versions locales et vérifier leur usage dans chaque leçon avant d’adopter leur empreinte. |
| A22 | Haute | CH02.01 et CH02.02, diagnostic et raccord | La sélection *Non Manifold* était proposée depuis le mode Faces. Le raccord du tabouret n’explicitait pas la sélection des deux faces intérieures. | Distinguer les modes de sélection, rejouer le diagnostic et la réparation sur le starter, cadrer les deux extrémités de la traverse. |
| A23 | Haute | CH03.09 et CH03.10, axes et préparation du personnage | Le tutoriel faisait tourner la grille avant une projection suivant son Y local. Il demandait également un déplacement du mannequin dont les pieds étaient déjà au sol. | Appliquer la rotation avant la projection. Rejouer *All Transforms* sur le mannequin et contrôler les positions mondiales et l’origine avant le rig. |
| A24 | Haute | CH04.05, relief des joints | Le masque Brick vaut 1 sur le mortier. Relié directement à Height sans inversion, il donnait des joints saillants. | Corriger la scène et le rendu de référence. Contrôler le sens dans le cas d’un branchement direct et garder l’ancien fichier comme contre-exemple. |
| A25 | Haute | CH07.01, CH07.02 et CH07.12, insertion de clés | Les tutoriels supposaient que `I` dans la vue 3D ouvrait toujours un choix de canaux. En 5.3, la commande dépend du jeu de clés ou des préférences. | Insérer au survol du champ à animer et vérifier les courbes créées. |
| A26 | Moyenne | CH07.09, trajectoire de saut | Les poignées Vector étaient présentées comme une façon d’obtenir une parabole exacte. | Donner une formule et des positions intermédiaires. Indiquer la portée du réglage manuel par rapport au corrigé calculé. |
| A27 | Moyenne | CH16.08, exercice de livraison | Le contrôle ouvrait toujours le fichier de démonstration même lorsque l’apprenant préparait une variante. | Accepter une archive explicite et vérifier séparément une erreur d’empreinte et un dépassement de timecode. |

## Répartition des preuves

Scènes locales et PNG locaux comptent les chapitres contenant ces ressources. Les chapitres avancés peuvent réutiliser des fichiers à l’échelle de la phase.


| Phase | Chapitres | Spécifications | Documentaires | Scènes locales | PNG locaux | Mots médians du tutoriel |
|---|---:|---:|---:|---:|---:|---:|
| 00 | 8 | 8 | 0 | 5 | 2 | 431 |
| 01 | 14 | 14 | 0 | 14 | 5 | 294 |
| 02 | 13 | 13 | 0 | 13 | 13 | 276 |
| 03 | 10 | 10 | 0 | 10 | 10 | 386 |
| 04 | 11 | 11 | 0 | 11 | 11 | 303 |
| 05 | 10 | 10 | 0 | 10 | 10 | 270 |
| 06 | 11 | 11 | 0 | 11 | 11 | 297 |
| 07 | 15 | 15 | 0 | 15 | 15 | 251 |
| 08 | 10 | 10 | 0 | 10 | 10 | 204 |
| 09 | 12 | 12 | 0 | 12 | 12 | 212 |
| 10 | 7 | 7 | 0 | 7 | 7 | 221 |
| 11 | 10 | 10 | 0 | 10 | 10 | 238 |
| 12 | 6 | 6 | 0 | 6 | 6 | 228 |
| 13 | 9 | 9 | 0 | 3 | 3 | 228 |
| 14 | 7 | 0 | 7 | 0 | 0 | 210 |
| 15 | 6 | 3 | 3 | 0 | 0 | 194 |
| 16 | 8 | 5 | 3 | 0 | 0 | 233 |
| 17 | 10 | 1 | 9 | 0 | 0 | 226 |
| 18 | 22 | 22 | 0 | 22 | 21 | 330 |


## Inventaire et triage des 199 chapitres

La colonne « preuve » indique le type de contrôle repéré. La prochaine revue évalue aussi la précision, l’actualité, la clarté, la difficulté, les redites et l’utilité des consignes propres au chapitre.


### Phase 00

| Chapitre | Preuve repérée | À confirmer |
|---|---|---|
| [CH00.01 — Installer, lancer et vérifier Blender](00_SETUP/CH00_01_INSTALLATION/README.md) | 5 contrôles enregistrés · 2 accepté / 2 refusé | A01–A02 CPU, PNG et CLI · A06 expliciter prérequis et métadonnées |
| [CH00.02 — Préférences essentielles](00_SETUP/CH00_02_PREFERENCES/README.md) | 4 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH00.03 — Performances CPU, GPU, mémoire](00_SETUP/CH00_03_PERFORMANCE/README.md) | 3 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH00.04 — Périphériques d'entrée](00_SETUP/CH00_04_INPUT_DEVICES/README.md) | 3 contrôles enregistrés | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH00.05 — Extensions et add-ons](00_SETUP/CH00_05_EXTENSIONS/README.md) | 2 contrôles enregistrés | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH00.06 — Organisation de projet](00_SETUP/CH00_06_PROJECT_ORGANIZATION/README.md) | 3 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH00.07 — Sauvegardes, récupération, versions](00_SETUP/CH00_07_BACKUP_VERSIONS/README.md) | 3 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH00.08 — Introduction au pipeline cinéma](00_SETUP/CH00_08_PIPELINE_INTRO/README.md) | 1 contrôles enregistrés | Comparer tutoriel, exercice autonome et preuve de réussite |

### Phase 01

| Chapitre | Preuve repérée | À confirmer |
|---|---|---|
| [CH01.01 — L'interface](01_FUNDAMENTALS/CH01_01_INTERFACE/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH01.02 — Navigation 3D](01_FUNDAMENTALS/CH01_02_NAVIGATION/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH01.03 — Sélection et manipulation](01_FUNDAMENTALS/CH01_03_SELECTION_TRANSFORM/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH01.04 — Objets et meshes](01_FUNDAMENTALS/CH01_04_OBJECTS_DATA/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH01.05 — Modes Object et Edit](01_FUNDAMENTALS/CH01_05_EDIT_MODE/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH01.06 — Transformations avancées](01_FUNDAMENTALS/CH01_06_TRANSFORMS_ADVANCED/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH01.07 — Origines, pivots, curseur 3D](01_FUNDAMENTALS/CH01_07_ORIGINS_PIVOTS/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH01.08 — Collections et Outliner](01_FUNDAMENTALS/CH01_08_COLLECTIONS_OUTLINER/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH01.09 — Éditeur de propriétés](01_FUNDAMENTALS/CH01_09_PROPERTIES_EDITOR/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH01.10 — Modificateurs essentiels](01_FUNDAMENTALS/CH01_10_MODIFIERS/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH01.11 — Matériaux simples](01_FUNDAMENTALS/CH01_11_MATERIALS_BASICS/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH01.12 — Caméras](01_FUNDAMENTALS/CH01_12_CAMERAS/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH01.13 — Éclairage élémentaire](01_FUNDAMENTALS/CH01_13_LIGHTING_BASICS/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH01.14 — Premiers rendus](01_FUNDAMENTALS/CH01_14_FIRST_RENDERS/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |

### Phase 02

| Chapitre | Preuve repérée | À confirmer |
|---|---|---|
| [CH02.01 — Topologie](02_MODELING/CH02_01_TOPOLOGY/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH02.02 — Outils polygonaux I](02_MODELING/CH02_02_POLY_TOOLS_1/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH02.03 — Outils polygonaux II](02_MODELING/CH02_03_POLY_TOOLS_2/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH02.04 — Normales](02_MODELING/CH02_04_NORMALS/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH02.05 — Hard Surface](02_MODELING/CH02_05_HARD_SURFACE/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH02.06 — Subdivision Surface](02_MODELING/CH02_06_SUBDIVISION/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH02.07 — Booléens et non destructif](02_MODELING/CH02_07_BOOLEANS/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH02.08 — Modélisation organique](02_MODELING/CH02_08_ORGANIC/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH02.09 — Retopologie](02_MODELING/CH02_09_RETOPOLOGY/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH02.10 — Optimisation](02_MODELING/CH02_10_OPTIMIZATION/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH02.11 — UV fondamentaux](02_MODELING/CH02_11_UV_BASICS/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH02.12 — Modélisation pour l'animation](02_MODELING/CH02_12_ANIMATION_READY/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | A08 échange et réouverture |
| [CH02.13 — Assets réutilisables](02_MODELING/CH02_13_ASSETS/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |

### Phase 03

| Chapitre | Preuve repérée | À confirmer |
|---|---|---|
| [CH03.01 — Anatomie artistique](03_SCULPTING/CH03_01_ARTISTIC_ANATOMY/README.md) | 6 contrôles enregistrés · 3 accepté / 3 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH03.02 — Sculpt Mode](03_SCULPTING/CH03_02_SCULPT_MODE/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH03.03 — Résolution dynamique](03_SCULPTING/CH03_03_DYNAMIC_RESOLUTION/README.md) | 7 contrôles enregistrés · 3 accepté / 4 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH03.04 — Sculpture stylisée](03_SCULPTING/CH03_04_STYLIZED/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH03.05 — Sculpture réaliste](03_SCULPTING/CH03_05_REALISTIC/README.md) | 10 contrôles enregistrés · 2 accepté / 8 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH03.06 — Visages](03_SCULPTING/CH03_06_FACES/README.md) | 11 contrôles enregistrés · 3 accepté / 8 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH03.07 — Mains et pieds](03_SCULPTING/CH03_07_HANDS_FEET/README.md) | 16 contrôles enregistrés · 2 accepté / 14 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH03.08 — Vêtements](03_SCULPTING/CH03_08_CLOTHING/README.md) | 6 contrôles enregistrés · 1 accepté / 5 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH03.09 — Retopologie personnage](03_SCULPTING/CH03_09_RETOPOLOGY/README.md) | 7 contrôles enregistrés · 1 accepté / 6 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH03.10 — Préparation au rigging](03_SCULPTING/CH03_10_RIG_READY/README.md) | 9 contrôles enregistrés · 2 accepté / 7 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |

### Phase 04

| Chapitre | Preuve repérée | À confirmer |
|---|---|---|
| [CH04.01 — UV Unwrapping avancé](04_MATERIALS/CH04_01_UV_UNWRAP/README.md) | 6 contrôles enregistrés · 1 accepté / 5 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH04.02 — Packing et UDIM](04_MATERIALS/CH04_02_PACKING_UDIM/README.md) | 6 contrôles enregistrés · 1 accepté / 5 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH04.03 — PBR et Principled BSDF](04_MATERIALS/CH04_03_PBR_PRINCIPLED/README.md) | 7 contrôles enregistrés · 1 accepté / 6 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH04.04 — Shader Editor](04_MATERIALS/CH04_04_SHADER_EDITOR/README.md) | 8 contrôles enregistrés · 1 accepté / 7 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH04.05 — Textures procédurales](04_MATERIALS/CH04_05_PROCEDURAL_TEXTURES/README.md) | 8 contrôles enregistrés · 1 accepté / 7 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH04.06 — Texture Painting](04_MATERIALS/CH04_06_TEXTURE_PAINTING/README.md) | 7 contrôles enregistrés · 1 accepté / 6 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH04.07 — Baking](04_MATERIALS/CH04_07_BAKING/README.md) | 7 contrôles enregistrés · 1 accepté / 6 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH04.08 — Relief](04_MATERIALS/CH04_08_RELIEF/README.md) | 8 contrôles enregistrés · 1 accepté / 7 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH04.09 — Matériaux types](04_MATERIALS/CH04_09_TYPICAL_MATERIALS/README.md) | 7 contrôles enregistrés · 1 accepté / 6 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH04.10 — Matériaux de personnages](04_MATERIALS/CH04_10_CHARACTER_MATERIALS/README.md) | 7 contrôles enregistrés · 1 accepté / 6 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH04.11 — Gestion des couleurs](04_MATERIALS/CH04_11_COLOR_MANAGEMENT/README.md) | 9 contrôles enregistrés · 1 accepté / 8 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |

### Phase 05

| Chapitre | Preuve repérée | À confirmer |
|---|---|---|
| [CH05.01 — Principes](05_GEOMETRY_NODES/CH05_01_PRINCIPLES/README.md) | 8 contrôles enregistrés · 1 accepté / 7 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH05.02 — Géométrie procédurale](05_GEOMETRY_NODES/CH05_02_PROCEDURAL_GEOMETRY/README.md) | 7 contrôles enregistrés · 1 accepté / 6 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH05.03 — Instances](05_GEOMETRY_NODES/CH05_03_INSTANCES/README.md) | 8 contrôles enregistrés · 1 accepté / 7 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH05.04 — Distribution](05_GEOMETRY_NODES/CH05_04_DISTRIBUTION/README.md) | 7 contrôles enregistrés · 1 accepté / 6 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH05.05 — Attributs](05_GEOMETRY_NODES/CH05_05_ATTRIBUTES/README.md) | 8 contrôles enregistrés · 1 accepté / 7 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH05.06 — Paramètres et interfaces](05_GEOMETRY_NODES/CH05_06_PARAMETERS/README.md) | 7 contrôles enregistrés · 1 accepté / 6 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH05.07 — Décors et végétation](05_GEOMETRY_NODES/CH05_07_SCATTERING/README.md) | 7 contrôles enregistrés · 1 accepté / 6 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH05.08 — Architecture procédurale](05_GEOMETRY_NODES/CH05_08_ARCHITECTURE/README.md) | 6 contrôles enregistrés · 1 accepté / 5 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH05.09 — Boucles et simulation](05_GEOMETRY_NODES/CH05_09_LOOPS/README.md) | 7 contrôles enregistrés · 1 accepté / 6 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH05.10 — Optimisation et outils](05_GEOMETRY_NODES/CH05_10_TOOLS/README.md) | 9 contrôles enregistrés · 1 accepté / 8 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |

### Phase 06

| Chapitre | Preuve repérée | À confirmer |
|---|---|---|
| [CH06.01 — Armatures et bones](06_RIGGING/CH06_01_ARMATURES/README.md) | 9 contrôles enregistrés · 1 accepté / 8 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH06.02 — Contraintes](06_RIGGING/CH06_02_CONSTRAINTS/README.md) | 8 contrôles enregistrés · 1 accepté / 7 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH06.03 — Skinning](06_RIGGING/CH06_03_SKINNING/README.md) | 8 contrôles enregistrés · 1 accepté / 7 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH06.04 — IK/FK](06_RIGGING/CH06_04_IK_FK/README.md) | 7 contrôles enregistrés · 1 accepté / 6 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH06.05 — Rig humanoïde](06_RIGGING/CH06_05_HUMANOID/README.md) | 9 contrôles enregistrés · 1 accepté / 8 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH06.06 — Rig quadrupède](06_RIGGING/CH06_06_QUADRUPED/README.md) | 8 contrôles enregistrés · 1 accepté / 7 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH06.07 — Rig mécanique](06_RIGGING/CH06_07_MECHANICAL/README.md) | 8 contrôles enregistrés · 1 accepté / 7 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH06.08 — Shape Keys et drivers](06_RIGGING/CH06_08_SHAPEKEYS/README.md) | 8 contrôles enregistrés · 1 accepté / 7 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH06.09 — Rig facial](06_RIGGING/CH06_09_FACIAL/README.md) | 8 contrôles enregistrés · 1 accepté / 7 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH06.10 — Contrôleurs et ergonomie](06_RIGGING/CH06_10_CONTROLS/README.md) | 9 contrôles enregistrés · 1 accepté / 8 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH06.11 — Rigging avancé et réutilisation](06_RIGGING/CH06_11_ADVANCED/README.md) | 12 contrôles enregistrés · 2 accepté / 10 refusé | A10 retrouver la preuve autonome |

### Phase 07

| Chapitre | Preuve repérée | À confirmer |
|---|---|---|
| [CH07.01 — Les 12 principes](07_ANIMATION/CH07_01_PRINCIPLES/README.md) | 8 contrôles enregistrés · 1 accepté / 7 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH07.02 — Keyframes et timeline](07_ANIMATION/CH07_02_KEYFRAMES/README.md) | 8 contrôles enregistrés · 1 accepté / 7 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH07.03 — Dope Sheet et Action](07_ANIMATION/CH07_03_DOPESHEET/README.md) | 8 contrôles enregistrés · 1 accepté / 7 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH07.04 — Graph Editor](07_ANIMATION/CH07_04_GRAPHEDITOR/README.md) | 8 contrôles enregistrés · 1 accepté / 7 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH07.05 — Timing et spacing](07_ANIMATION/CH07_05_TIMING/README.md) | 8 contrôles enregistrés · 1 accepté / 7 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH07.06 — Arcs, overlap, follow-through](07_ANIMATION/CH07_06_OVERLAP/README.md) | 8 contrôles enregistrés · 1 accepté / 7 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH07.07 — Posing et silhouette](07_ANIMATION/CH07_07_POSING/README.md) | 8 contrôles enregistrés · 1 accepté / 7 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH07.08 — Cycles de marche](07_ANIMATION/CH07_08_WALK/README.md) | 8 contrôles enregistrés · 1 accepté / 7 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH07.09 — Course, saut, interactions](07_ANIMATION/CH07_09_RUN_JUMP/README.md) | 8 contrôles enregistrés · 1 accepté / 7 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH07.10 — Acting](07_ANIMATION/CH07_10_ACTING/README.md) | 8 contrôles enregistrés · 1 accepté / 7 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH07.11 — Animation faciale et lip sync](07_ANIMATION/CH07_11_FACIAL/README.md) | 8 contrôles enregistrés · 1 accepté / 7 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH07.12 — Animation de caméra](07_ANIMATION/CH07_12_CAMERA/README.md) | 8 contrôles enregistrés · 1 accepté / 7 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH07.13 — Animation non linéaire](07_ANIMATION/CH07_13_NLA/README.md) | 8 contrôles enregistrés · 1 accepté / 7 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH07.14 — Motion capture](07_ANIMATION/CH07_14_MOCAP/README.md) | 8 contrôles enregistrés · 1 accepté / 7 refusé | A08 échange et réouverture |
| [CH07.15 — Scène dialoguée](07_ANIMATION/CH07_15_DIALOGUE/README.md) | 8 contrôles enregistrés · 1 accepté / 7 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |

### Phase 08

| Chapitre | Preuve repérée | À confirmer |
|---|---|---|
| [CH08.01 — Rigid Bodies](08_SIMULATIONS/CH08_01_RIGID_BODIES/README.md) | 8 contrôles enregistrés · 1 accepté / 7 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH08.02 — Soft Bodies](08_SIMULATIONS/CH08_02_SOFT_BODIES/README.md) | 7 contrôles enregistrés · 1 accepté / 6 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH08.03 — Cloth](08_SIMULATIONS/CH08_03_CLOTH/README.md) | 6 contrôles enregistrés · 1 accepté / 5 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH08.04 — Particules et distribution](08_SIMULATIONS/CH08_04_PARTICLES/README.md) | 8 contrôles enregistrés · 1 accepté / 7 refusé | A07 configuration ou différence 5.3 |
| [CH08.05 — Fluides (Mantaflow)](08_SIMULATIONS/CH08_05_FLUIDS/README.md) | 6 contrôles enregistrés · 1 accepté / 5 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH08.06 — Fumée et feu](08_SIMULATIONS/CH08_06_SMOKE_FIRE/README.md) | 7 contrôles enregistrés · 1 accepté / 6 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH08.07 — Destruction](08_SIMULATIONS/CH08_07_DESTRUCTION/README.md) | 6 contrôles enregistrés · 1 accepté / 5 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH08.08 — Cheveux et fourrure](08_SIMULATIONS/CH08_08_HAIR_FUR/README.md) | 8 contrôles enregistrés · 1 accepté / 7 refusé | A07 configuration ou différence 5.3 |
| [CH08.09 — Forces](08_SIMULATIONS/CH08_09_FORCES/README.md) | 7 contrôles enregistrés · 1 accepté / 6 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH08.10 — Caches et baking](08_SIMULATIONS/CH08_10_CACHES/README.md) | 6 contrôles enregistrés · 1 accepté / 5 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |

### Phase 09

| Chapitre | Preuve repérée | À confirmer |
|---|---|---|
| [CH09.01 — Théorie de la lumière](09_CINEMATOGRAPHY/CH09_01_LIGHT_THEORY/README.md) | 7 contrôles enregistrés · 1 accepté / 6 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH09.02 — Trois points et variantes](09_CINEMATOGRAPHY/CH09_02_THREE_POINT/README.md) | 6 contrôles enregistrés · 1 accepté / 5 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH09.03 — Naturel et HDRI](09_CINEMATOGRAPHY/CH09_03_NATURAL_HDRI/README.md) | 7 contrôles enregistrés · 1 accepté / 6 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH09.04 — Dramatique et stylisé](09_CINEMATOGRAPHY/CH09_04_DRAMATIC/README.md) | 7 contrôles enregistrés · 1 accepté / 6 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH09.05 — Volumétrie](09_CINEMATOGRAPHY/CH09_05_VOLUMETRICS/README.md) | 6 contrôles enregistrés · 1 accepté / 5 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH09.06 — Exposition et contraste](09_CINEMATOGRAPHY/CH09_06_EXPOSURE/README.md) | 6 contrôles enregistrés · 1 accepté / 5 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH09.07 — Composition](09_CINEMATOGRAPHY/CH09_07_COMPOSITION/README.md) | 7 contrôles enregistrés · 1 accepté / 6 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH09.08 — Objectifs et focales](09_CINEMATOGRAPHY/CH09_08_LENSES/README.md) | 7 contrôles enregistrés · 1 accepté / 6 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH09.09 — Profondeur de champ](09_CINEMATOGRAPHY/CH09_09_DEPTH_OF_FIELD/README.md) | 7 contrôles enregistrés · 1 accepté / 6 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH09.10 — Mouvements et grammaire](09_CINEMATOGRAPHY/CH09_10_MOVEMENTS/README.md) | 8 contrôles enregistrés · 1 accepté / 7 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH09.11 — Couleur et émotion](09_CINEMATOGRAPHY/CH09_11_COLOR_EMOTION/README.md) | 8 contrôles enregistrés · 1 accepté / 7 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH09.12 — Mise en scène](09_CINEMATOGRAPHY/CH09_12_STAGING/README.md) | 9 contrôles enregistrés · 1 accepté / 8 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |

### Phase 10

| Chapitre | Preuve repérée | À confirmer |
|---|---|---|
| [CH10.01 — EEVEE en profondeur](10_RENDERING/CH10_01_EEVEE/README.md) | 8 contrôles enregistrés · 1 accepté / 6 refusé | A07 configuration ou différence 5.3 |
| [CH10.02 — Cycles en profondeur](10_RENDERING/CH10_02_CYCLES/README.md) | 8 contrôles enregistrés · 1 accepté / 6 refusé | A07 configuration ou différence 5.3 |
| [CH10.03 — Bruit et débruitage](10_RENDERING/CH10_03_DENOISING/README.md) | 7 contrôles enregistrés · 1 accepté / 5 refusé | A07 configuration ou différence 5.3 |
| [CH10.04 — Passes, AOV, View Layers](10_RENDERING/CH10_04_PASSES/README.md) | 9 contrôles enregistrés · 1 accepté / 7 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH10.05 — Mémoire et optimisation](10_RENDERING/CH10_05_MEMORY/README.md) | 7 contrôles enregistrés · 1 accepté / 5 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH10.06 — EXR et couleur](10_RENDERING/CH10_06_EXR_COLOR/README.md) | 7 contrôles enregistrés · 1 accepté / 5 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH10.07 — Rendu distribué](10_RENDERING/CH10_07_BATCH/README.md) | 9 contrôles enregistrés · 1 accepté / 7 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |

### Phase 11

| Chapitre | Preuve repérée | À confirmer |
|---|---|---|
| [CH11.01 — Compositor](11_COMPOSITING_VFX/CH11_01_COMPOSITOR/README.md) | 8 contrôles enregistrés · 1 accepté / 6 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH11.02 — Compositing multipasse](11_COMPOSITING_VFX/CH11_02_MULTIPASS/README.md) | 8 contrôles enregistrés · 1 accepté / 6 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH11.03 — Masques et Cryptomatte](11_COMPOSITING_VFX/CH11_03_MASKS/README.md) | 7 contrôles enregistrés · 1 accepté / 5 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH11.04 — Depth, defocus, motion blur](11_COMPOSITING_VFX/CH11_04_DEPTH_FX/README.md) | 7 contrôles enregistrés · 1 accepté / 5 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH11.05 — Glare et effets](11_COMPOSITING_VFX/CH11_05_GLARE/README.md) | 8 contrôles enregistrés · 1 accepté / 6 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH11.06 — Color grading](11_COMPOSITING_VFX/CH11_06_GRADING/README.md) | 8 contrôles enregistrés · 1 accepté / 6 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH11.07 — Keying](11_COMPOSITING_VFX/CH11_07_KEYING/README.md) | 7 contrôles enregistrés · 1 accepté / 5 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH11.08 — Tracking et matchmoving](11_COMPOSITING_VFX/CH11_08_TRACKING/README.md) | 7 contrôles enregistrés · 1 accepté / 5 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH11.09 — Intégration 3D/réel](11_COMPOSITING_VFX/CH11_09_INTEGRATION/README.md) | 7 contrôles enregistrés · 1 accepté / 5 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH11.10 — Cohérence visuelle](11_COMPOSITING_VFX/CH11_10_CONSISTENCY/README.md) | 6 contrôles enregistrés · 1 accepté / 4 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |

### Phase 12

| Chapitre | Preuve repérée | À confirmer |
|---|---|---|
| [CH12.01 — Video Sequencer](12_EDITING_SOUND/CH12_01_VSE/README.md) | 8 contrôles enregistrés · 1 accepté / 6 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH12.02 — Montage narratif](12_EDITING_SOUND/CH12_02_EDITING/README.md) | 8 contrôles enregistrés · 1 accepté / 6 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH12.03 — Son](12_EDITING_SOUND/CH12_03_SOUND/README.md) | 8 contrôles enregistrés · 1 accepté / 6 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH12.04 — Mixage](12_EDITING_SOUND/CH12_04_MIX/README.md) | 8 contrôles enregistrés · 1 accepté / 6 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH12.05 — Titres et sous-titres](12_EDITING_SOUND/CH12_05_TITLES/README.md) | 8 contrôles enregistrés · 1 accepté / 6 refusé | A07 configuration ou différence 5.3 |
| [CH12.06 — Export et livraison](12_EDITING_SOUND/CH12_06_EXPORT/README.md) | 7 contrôles enregistrés · 1 accepté / 6 refusé | A07 configuration ou différence 5.3 · A08 échange et réouverture |

### Phase 13

| Chapitre | Preuve repérée | À confirmer |
|---|---|---|
| [CH13.01 — Python pour artistes](13_PYTHON_AUTOMATION/CH13_01_PYTHON_BASICS/README.md) | 7 contrôles enregistrés · 1 accepté / 6 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH13.02 — L'API bpy](13_PYTHON_AUTOMATION/CH13_02_BPY_API/README.md) | 7 contrôles enregistrés · 1 accepté / 5 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH13.03 — Génération d'objets et matériaux](13_PYTHON_AUTOMATION/CH13_03_MESH_MATERIALS/README.md) | 9 contrôles enregistrés · 1 accepté / 6 refusé | A06 expliciter prérequis et métadonnées · A10 retrouver la preuve autonome |
| [CH13.04 — Collections, caméras, rendus](13_PYTHON_AUTOMATION/CH13_04_PLAN_SETUP/README.md) | 1 contrôles enregistrés | A05 expliquer mécanisme et choix |
| [CH13.05 — Batch rendering](13_PYTHON_AUTOMATION/CH13_05_BATCH_RENDER/README.md) | 1 contrôles enregistrés | A05 expliquer mécanisme et choix |
| [CH13.06 — Validation](13_PYTHON_AUTOMATION/CH13_06_QUALITY_CONTROL/README.md) | 1 contrôles enregistrés | A05 expliquer mécanisme et choix |
| [CH13.07 — Opérateurs et UI](13_PYTHON_AUTOMATION/CH13_07_OPERATORS_UI/README.md) | 1 contrôles enregistrés | A05 expliquer mécanisme et choix |
| [CH13.08 — Extensions](13_PYTHON_AUTOMATION/CH13_08_EXTENSIONS/README.md) | 1 contrôles enregistrés | A05 expliquer mécanisme et choix |
| [CH13.09 — Debugging et performance](13_PYTHON_AUTOMATION/CH13_09_DEBUG_PERFORMANCE/README.md) | 1 contrôles enregistrés | A05 expliquer mécanisme et choix |

### Phase 14

| Chapitre | Preuve repérée | À confirmer |
|---|---|---|
| [CH14.01 — Cadre, éthique et droits](14_AI_PRODUCTION/CH14_01_RIGHTS/README.md) | Revue documentaire | A05 expliquer mécanisme et choix · A04 relire le livrable et sa preuve |
| [CH14.02 — IA en préproduction](14_AI_PRODUCTION/CH14_02_PREPRODUCTION/README.md) | Revue documentaire | A05 expliquer mécanisme et choix · A04 relire le livrable et sa preuve |
| [CH14.03 — IA pour les assets](14_AI_PRODUCTION/CH14_03_ASSETS/README.md) | Revue documentaire | A05 expliquer mécanisme et choix · A04 relire le livrable et sa preuve |
| [CH14.04 — IA pour l'animation](14_AI_PRODUCTION/CH14_04_ANIMATION/README.md) | Revue documentaire | A05 expliquer mécanisme et choix · A04 relire le livrable et sa preuve |
| [CH14.05 — IA pour la mise en scène](14_AI_PRODUCTION/CH14_05_DIRECTION/README.md) | Revue documentaire | A05 expliquer mécanisme et choix · A04 relire le livrable et sa preuve |
| [CH14.06 — Claude Code et Blender](14_AI_PRODUCTION/CH14_06_CLAUDE_CODE/README.md) | Revue documentaire | A05 expliquer mécanisme et choix · A04 relire le livrable et sa preuve |
| [CH14.07 — Pipeline hybride](14_AI_PRODUCTION/CH14_07_HYBRID_PIPELINE/README.md) | Revue documentaire | A05 expliquer mécanisme et choix · A04 relire le livrable et sa preuve |

### Phase 15

| Chapitre | Preuve repérée | À confirmer |
|---|---|---|
| [CH15.01 — De l'idée au scénario](15_SHORT_FILMS/CH15_01_SCRIPT/README.md) | Revue documentaire | A05 expliquer mécanisme et choix · A04 relire le livrable et sa preuve |
| [CH15.02 — Storyboard et animatique](15_SHORT_FILMS/CH15_02_STORYBOARD/README.md) | 1 contrôles enregistrés | A05 expliquer mécanisme et choix |
| [CH15.03 — Direction artistique](15_SHORT_FILMS/CH15_03_ART_DIRECTION/README.md) | Revue documentaire | A05 expliquer mécanisme et choix · A04 relire le livrable et sa preuve |
| [CH15.04 — Planification](15_SHORT_FILMS/CH15_04_PLANNING/README.md) | Revue documentaire | A05 expliquer mécanisme et choix · A04 relire le livrable et sa preuve |
| [CH15.05 — Fabrication](15_SHORT_FILMS/CH15_05_PRODUCTION/README.md) | 1 contrôles enregistrés | A05 expliquer mécanisme et choix |
| [CH15.06 — Finition](15_SHORT_FILMS/CH15_06_FINISHING/README.md) | 1 contrôles enregistrés | A05 expliquer mécanisme et choix |

### Phase 16

| Chapitre | Preuve repérée | À confirmer |
|---|---|---|
| [CH16.01 — Développement d'un film](16_FEATURE_FILMS/CH16_01_DEVELOPMENT/README.md) | Revue documentaire | A05 expliquer mécanisme et choix · A04 relire le livrable et sa preuve |
| [CH16.02 — Séquences et plans](16_FEATURE_FILMS/CH16_02_SHOT_TRACKING/README.md) | 1 contrôles enregistrés | A05 expliquer mécanisme et choix |
| [CH16.03 — Asset management](16_FEATURE_FILMS/CH16_03_ASSET_MANAGEMENT/README.md) | 1 contrôles enregistrés | A05 expliquer mécanisme et choix |
| [CH16.04 — Pipelines de rendu](16_FEATURE_FILMS/CH16_04_RENDER_PIPELINES/README.md) | 1 contrôles enregistrés | A05 expliquer mécanisme et choix |
| [CH16.05 — Équipes et départements](16_FEATURE_FILMS/CH16_05_TEAMS/README.md) | Revue documentaire | A05 expliquer mécanisme et choix · A04 relire le livrable et sa preuve |
| [CH16.06 — Budget, planning, risques](16_FEATURE_FILMS/CH16_06_BUDGET_RISKS/README.md) | 1 contrôles enregistrés | A05 expliquer mécanisme et choix |
| [CH16.07 — Solo vs indé vs studio](16_FEATURE_FILMS/CH16_07_PRODUCTION_MODELS/README.md) | Revue documentaire | A05 expliquer mécanisme et choix · A04 relire le livrable et sa preuve |
| [CH16.08 — Livraison](16_FEATURE_FILMS/CH16_08_DELIVERY/README.md) | 1 contrôles enregistrés | A08 échange et réouverture · A05 expliquer mécanisme et choix |

### Phase 17

| Chapitre | Preuve repérée | À confirmer |
|---|---|---|
| [CH17.01 — Character Artist](17_EXPERT_SPECIALIZATIONS/CH17_01_CHARACTER_ARTIST/README.md) | Revue documentaire | A05 expliquer mécanisme et choix · A04 relire le livrable et sa preuve |
| [CH17.02 — Environment Artist](17_EXPERT_SPECIALIZATIONS/CH17_02_ENVIRONMENT_ARTIST/README.md) | Revue documentaire | A05 expliquer mécanisme et choix · A04 relire le livrable et sa preuve |
| [CH17.03 — Technical Artist](17_EXPERT_SPECIALIZATIONS/CH17_03_TECHNICAL_ARTIST/README.md) | Revue documentaire | A05 expliquer mécanisme et choix · A04 relire le livrable et sa preuve |
| [CH17.04 — Animator](17_EXPERT_SPECIALIZATIONS/CH17_04_ANIMATOR/README.md) | Revue documentaire | A05 expliquer mécanisme et choix · A04 relire le livrable et sa preuve |
| [CH17.05 — Lighting Artist](17_EXPERT_SPECIALIZATIONS/CH17_05_LIGHTING_ARTIST/README.md) | Revue documentaire | A05 expliquer mécanisme et choix · A04 relire le livrable et sa preuve |
| [CH17.06 — VFX Artist](17_EXPERT_SPECIALIZATIONS/CH17_06_VFX_ARTIST/README.md) | Revue documentaire | A05 expliquer mécanisme et choix · A04 relire le livrable et sa preuve |
| [CH17.07 — Technical Director](17_EXPERT_SPECIALIZATIONS/CH17_07_TECHNICAL_DIRECTOR/README.md) | Revue documentaire | A05 expliquer mécanisme et choix · A04 relire le livrable et sa preuve |
| [CH17.08 — Pipeline Developer](17_EXPERT_SPECIALIZATIONS/CH17_08_PIPELINE_DEVELOPER/README.md) | 2 contrôles enregistrés | A05 expliquer mécanisme et choix |
| [CH17.09 — CG Supervisor](17_EXPERT_SPECIALIZATIONS/CH17_09_CG_SUPERVISOR/README.md) | Revue documentaire | A05 expliquer mécanisme et choix · A04 relire le livrable et sa preuve |
| [CH17.10 — Réalisateur d'animation](17_EXPERT_SPECIALIZATIONS/CH17_10_DIRECTOR/README.md) | Revue documentaire | A05 expliquer mécanisme et choix · A04 relire le livrable et sa preuve |

### Phase 18

| Chapitre | Preuve repérée | À confirmer |
|---|---|---|
| [CH18.01 — Formes et volumes](18_GREASE_PENCIL/CH18_01_SHAPES_VOLUMES/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH18.02 — Perspective](18_GREASE_PENCIL/CH18_02_PERSPECTIVE/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH18.03 — Proportions, silhouettes, gestuelle](18_GREASE_PENCIL/CH18_03_PROPORTIONS_GESTURE/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH18.04 — Expressions et personnages](18_GREASE_PENCIL/CH18_04_EXPRESSIONS_CHARACTERS/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH18.05 — Composition et dessin cinématographique](18_GREASE_PENCIL/CH18_05_COMPOSITION/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH18.06 — Grease Pencil : interface et objets](18_GREASE_PENCIL/CH18_06_GP_INTERFACE/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | A07 configuration ou différence 5.3 |
| [CH18.07 — Brushes, traits, remplissages, matériaux](18_GREASE_PENCIL/CH18_07_BRUSHES_MATERIALS/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | A07 configuration ou différence 5.3 |
| [CH18.08 — Calques, modificateurs, transformations](18_GREASE_PENCIL/CH18_08_LAYERS_MODIFIERS/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | A07 configuration ou différence 5.3 |
| [CH18.09 — Dessin dans l'espace 3D et organisation](18_GREASE_PENCIL/CH18_09_DRAWING_IN_3D/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | A07 configuration ou différence 5.3 |
| [CH18.10 — Langage cinématographique](18_GREASE_PENCIL/CH18_10_FILM_LANGUAGE/README.md) | 4 contrôles enregistrés · 2 accepté / 2 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH18.11 — Continuité et dialogue](18_GREASE_PENCIL/CH18_11_CONTINUITY/README.md) | 4 contrôles enregistrés · 2 accepté / 2 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH18.12 — Cadrage, composition, découpage technique](18_GREASE_PENCIL/CH18_12_TECHNICAL_BREAKDOWN/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH18.13 — Storyboards d'action, d'émotion, complexes](18_GREASE_PENCIL/CH18_13_COMPLEX_BOARDS/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH18.14 — Du scénario à l'animatique](18_GREASE_PENCIL/CH18_14_ANIMATIC/README.md) | 4 contrôles enregistrés · 2 accepté / 2 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH18.15 — Son, rythme, transitions, export, révision](18_GREASE_PENCIL/CH18_15_SOUND_EXPORT/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH18.16 — Animation 2D : principes et image par image](18_GREASE_PENCIL/CH18_16_2D_ANIMATION/README.md) | 5 contrôles enregistrés · 2 accepté / 3 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH18.17 — Timing, spacing, cycles](18_GREASE_PENCIL/CH18_17_TIMING_CYCLES/README.md) | 4 contrôles enregistrés · 2 accepté / 2 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH18.18 — Personnages, expressions, effets, caméra](18_GREASE_PENCIL/CH18_18_ACTING_FX/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH18.19 — Dessiner dans et sur la 3D](18_GREASE_PENCIL/CH18_19_DRAW_ON_3D/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH18.20 — Workflow 2D → 3D](18_GREASE_PENCIL/CH18_20_2D_TO_3D/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH18.21 — IA pour le storyboard](18_GREASE_PENCIL/CH18_21_AI_STORYBOARD/README.md) | 2 contrôles enregistrés · 1 accepté / 1 refusé | Comparer tutoriel, exercice autonome et preuve de réussite |
| [CH18.22 — Projets de la phase](18_GREASE_PENCIL/CH18_22_PROJECTS/README.md) | 16 contrôles enregistrés · 7 accepté / 9 refusé | A10 retrouver la preuve autonome |
