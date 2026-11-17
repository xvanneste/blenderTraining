# Suivi de la refonte Blender

## État de la refonte au 17 novembre 2026

Les 199 chapitres ont été inventoriés et soumis aux contrôles structurels de départ. La reprise détaillée a commencé sur CH00.01–CH00.03. **Reprise en cours.** Les 199 chapitres ont reçu au moins une amélioration ou une vérification ciblée. Les chapitres d’installation ont été repris en détail et les autres ont une variante de transfert ou un cas de production supplémentaire. [Audit de départ et triage](AUDIT_COURS_BLENDER.md) · [Plan par lots](PLAN_AMELIORATION_BLENDER.md)

**À poursuivre** Reprendre les chapitres encore marqués « Transfert ajouté » ou « Cas approfondi » pour leur revue détaillée. Rejouer les variantes en interface selon les points ouverts par chapitre. Observer une première séance avec un débutant. Vérifier la provenance des 42 binaires dont l’empreinte historique diffère.

## Changements transverses du premier lot

- **Guide d’entrée**. Première séance centrée sur une image que l’apprenant peut rouvrir et partager. Voies vers la modélisation et le premier plan conservées.
- **Version**. Blender 5.3.0 maintenu. Confirmation par le binaire et la publication officielle. Le binaire a accepté le réglage séparé de PNG en IMAGE et de VIDEO avec MPEG4, H264 et AAC. La migration commence désormais par une exécution sans reconstruction des scènes.
- **Navigation**. Les liens des chapitres s’ouvrent dans l’application, les renvois ciblent des titres et les fichiers Blender restent accessibles. Le site distingue les contrôles techniques enregistrés des supports évalués par revue. Le test Edge a couvert les ancres du démarrage, l’atelier humain, le mobile et la reprise des anciennes données. Le contrôle statique a couvert 2 073 routes et ancres du site. Les nouveaux résultats enregistrent l’empreinte de la spécification. Le catalogue vérifie aussi le nombre et l’intitulé des cas attendus. L’historique sans empreinte est identifié par les libellés. Une modification des scripts ou scènes à spécification constante requiert toujours une relance.
- **Contrôles**. 6 tests sur CH00.01, 5 sur CH00.02, 4 sur CH00.03 dans Blender 5.3.0, sans reconstruire les scènes. La mire a été rendue et décodée deux fois en CPU. La restauration a été éprouvée sur un profil isolé. Trois états de la scène de galets et deux cas de masquage ont été testés.
- **Vérifications humaines ouvertes**. Parcours de première séance effectué par un débutant, durée observée, gestes rejoués entièrement à la souris, Windows portable et autres systèmes. Le scénario de rendu GPU doit être observé avec les périphériques concernés. Le test de configuration GPU utilise un rendu de contrôle CPU. Les performances réelles du starter lourd en pleine résolution ne font pas partie du rejeu.

## Deuxième lot · setup, fondamentaux et pratique

- **Commandes Blender**. 328 exemples dans 326 documents et 157 commandes dans 156 métadonnées remettent l’option --python-exit-code avant --python. Le gabarit de génération a été corrigé. Une exception sentinelle dans Blender 5.3.0 a donné 0 avec l’ancien ordre, 7 avec l’ordre corrigé.
- **CH00.04–08**. Navigation selon le matériel, installation locale dans un profil isolé, création portable de l’arborescence, récupération depuis une copie et calcul de durée pour le découpage. La boîte asymétrique a conservé ses dimensions dans le repère monde et le nom du matériau lors des trois réimports GLB, USD et OBJ. FBX conserve aussi le nom du matériau sur la boîte. Alembic a été vérifié sur une image pour la géométrie et doit garder le cache accessible si nécessaire. Les OBJ de l’exercice exigent le MTL associé.
- **CH01–08**. Un contrôle de transfert propre à chaque chapitre compare un geste, un réglage ou un état précis. Le test de la maison confirme le toit fermé de neuf faces et l’absence de face écrasée. Le correcteur du premier rendu accepte les réglages CPU ou GPU.
- **Portée des preuves**. Les 20 tests ciblés du deuxième lot sont passés. Les contrôles anciens du corpus sont en cours de réexécution sans reconstruction. Un test de fichier de référence et un contrôle de transfert proposé restent des preuves distinctes. Le matériel d’entrée, l’ergonomie et le temps réel du débutant restent à observer.

## Réexécution complète et projets de phase

- **Suite Blender 5.3.0**. 938 tests ont réussi dans la réexécution complète sans étape de reconstruction. Une relance de 30 tests sur onze chapitres a remplacé les résultats des chapitres repris. Le registre contient 944 résultats courants réussis sur 177 chapitres testables et 22 chapitres documentaires. Les cas du premier passage restent reliés aux libellés de leur spécification. La relance ajoute son empreinte aux 30 résultats mis à jour.
- **Projet P1**. Atelier en trois séances, scène de référence adaptée de CH01.14 et deux rendus 1920 × 1080 produits dans Blender. Le correcteur valide 27/27. Il refuse deux variantes, l’une avec les pommes dissociées et l’autre avec un emplacement matériau inutilisé par les faces. Blender a signalé un échec d’écriture de la vignette système. Le fichier principal a été rouvert et validé.
- **Projets P3 et P12**. Réexécution indépendante dans Blender des deux références et de leurs variantes fautives. 10 cas P3 et 11 cas P12 réussis. Les deux lanceurs activent le code de sortie Blender avant le script. Les commandes de 337 autres exemples ou commentaires de scripts ont aussi été remises dans l’ordre et les empreintes des scripts enregistrés ont été recalculées.
- **Fondamentaux CH01.06–13**. Contrôles ajoutés aux procédures d’accrochage, de pivot, de parentage, de matériau, de caméra et d’éclairage. Les 16 scénarios déclarés réussissent. Cette relance conserve les 944 résultats courants et ajoute 16 empreintes de spécification.
- **Fichiers et navigation**. 2 021 documents, 199 quiz et 2 115 renvois contrôlés. Le site écrit ses données dans un fichier temporaire avant de les remplacer. Deux reconstructions consécutives ont réussi après des erreurs d’ouverture en écriture directe. Le manifeste compte 1 785 ressources et zéro erreur de présence ou de schéma. Les 42 divergences restantes concernent 39 scènes, deux sauvegardes et un PNG. Dans 33 cas, l’empreinte enregistrée correspond à HEAD. Les neuf autres fichiers sont absents de HEAD. Les versions locales ont été conservées.

## Troisième lot · rendu, production et Grease Pencil

- **CH09–12 et CH18**. Variantes par chapitre avec preuve attendue sur éclairage, cadrage, rendu, compositing, montage, animation 2D et continuité.
- **CH13–17**. Quarante cas de production explicitent une décision et sa mesure. Les exercices distinguent le test local, la proposition simulée et la décision à faire relire.
- **Débutants et navigation**. Glossaire en français relié aux chapitres, contrôle de liens reproductible et [protocole d’essai de la première séance](DOCUMENTATION/ESSAI_PREMIERE_SEANCE.md).
- **Corrigé CH01.05**. La solution publiée avait une face de surface nulle et quatre arêtes hors variété. Le corrigé propre est publié et l’ancien fichier est devenu un contre-exemple vérifié.
- **CH01.14**. Le correcteur accepte CPU ou GPU. Le cas CPU relit le PNG de référence, puis rend réellement une image de contrôle à 15 %. Le calcul intégral 1080p avec le matériel de l’apprenant relève de sa propre séance.

## Modélisation et sculpture · CH02–03

- **Tutoriels corrigés**. Les 13 tutoriels de modélisation et les 10 tutoriels de sculpture ont été revus. Les mises à jour couvrent la topologie, les raccords, l’origine, le choix des brosses, la continuité des volumes, les axes du Shrinkwrap et les contrôles du personnage avant rigging.
- **Preuves**. 9 tests ciblés pour CH02.01–04 et 67 pour CH02.05–13 et CH03.06–10. Grid Fill et la fermeture du cylindre ont été rejoués directement sur le starter CH02.01. Dans CH03.10, `All Transforms` a conservé les coordonnées mondiales des sommets après remise à zéro de la rotation. L’origine est (0, 0, 0) et le point inférieur est à 0,38 mm du sol. Le registre compte désormais **945 contrôles réussis** sur 177 chapitres testables.
- **Route P1**. Les chemins générés du site et des trois fichiers de référence ont été contrôlés. Le rejeu navigateur complet de la nouvelle route reste ouvert après l’échec du lancement Edge sans interface dans cet environnement.

## Décisions et reprise

- **Deux lectures dans le site**. L’accueil propose un parcours de trois projets avec validation locale par livrable, et une bibliothèque des 199 chapitres avec recherche. Les scores, favoris et acquis historiques restent accessibles. Le projet P1 comporte une version courte pour le dernier jalon.

- **Matériaux et Geometry Nodes**. Tutoriels CH04 et CH05 repris. 21 figures de référence et deux dispositions UV reliées au geste à contrôler. Le corrigé du mur de briques utilise désormais Invert sur Bump. L’ancien corrigé est le contre-exemple. Les réponses du quiz, la théorie et le dépannage décrivent le masque dans le même sens.
- **Rigging, animation et simulation**. Relecture des tutoriels de rigging et de simulation. Correctifs d’insertion des clés au survol des propriétés, du retiming autour de la tête de lecture et de l’échantillonnage du saut. Les contrôles sur fixtures couvrent les cas attendus. Les gestes à la souris et les réglages artistiques restent à observer.
- **Rendu, montage et livraison**. Type Multi-Layer EXR et type Video confirmés dans Blender 5.3. L’atelier CH16.08 contrôle désormais un ZIP choisi. La démo et la démo explicitement passée ont donné dix pièces et deux sous-titres. Les variantes d’empreinte et de timecode ont été refusées séparément.
- **Vérifications de cette reprise**. Le premier passage de CH04 a pris l’ancien corrigé du mur pendant sa mise à jour. La relance a ensuite réussi ses 146 scénarios, y compris les 9 cas du mur. La relance animation, tissu, cadrage, rendu, montage et Grease Pencil a réussi ses 81 scénarios. Le registre contient 946 résultats courants réussis. Les 42 écarts historiques du manifeste restent ouverts.

- Conserver les chemins, les références historiques, les codes du catalogue et le stockage de progression. Séparer un résultat estimé, un résultat testé, une recommandation et un choix artistique.
- Contrôler les consignes qui citent le terminal, les espaces de travail et les raccourcis selon la configuration. Indiquer les manques dans chaque entrée lors de la relecture.
- Le rapport qualité final se rédige après la reprise détaillée de tous les chapitres. Ce journal donne l’état de chaque chapitre et les preuves de reprise déjà produites.

## État par chapitre

« Inventorié » signifie que les documents, données et éléments de preuve ont été repérés. La révision de fond est encore ouverte. « Révisé » qualifie le travail de ce lot et indique les vérifications en attente.


### Phase 00

| Chapitre | État | Modifications | Preuves | Suite |
|---|---|---|---|---|
| [CH00.01](00_SETUP/CH00_01_INSTALLATION/README.md) | Révisé | Voie CPU, PNG, versionnage, commande portable, correcteur explicite et données de chapitre. | 6 tests. Rejeu des deux rendus CPU à 128 et 64 échantillons, lecture PNG et résultat sauvegardé dans un chemin avec espaces. | Observer le pas-à-pas en interface et comparer un rendu matériel sur GPU compatible. |
| [CH00.02](00_SETUP/CH00_02_PREFERENCES/README.md) | Révisé | Cadrage par le menu, preuve sans vitesse minimale, préférences sauvegardées et restauration isolée. | 5 tests. Profil sauvegardé puis rouvert. Restauration de deux valeurs. Le cas de lecture seule VRAM est toléré. | Observer le parcours de cadrage et la reprise sur un profil préexistant. Vérifier les variantes clavier et trackpad. |
| [CH00.03](00_SETUP/CH00_03_PERFORMANCE/README.md) | Révisé | Estimation expliquée, comparaison à réglages constants, contrôle des galets masqués. | 4 tests. 202 → 3 maillages distincts, estimation 16 384 002 puis 256 002, contre-épreuves objet et collection. | Mesurer le coût réel et comparer les rendus sur des postes différents. Rejouer Copy to Selected en interface. |
| [CH00.04](00_SETUP/CH00_04_INPUT_DEVICES/README.md) | Révisé | Menus et gestes adaptés au matériel, choix d’émulation, preuve sans seuil de vitesse. | 4 tests ciblés. Six vues, cadrage et mode Face exécutés dans Blender. | Observer le trackpad et la pression d’un stylet. |
| [CH00.05](00_SETUP/CH00_05_EXTENSIONS/README.md) | Révisé | Lecture du manifeste et installation dans un profil d’exercice. | 3 tests. Paquet local installé sans accès en ligne, opérateur exécuté, panneau désactivé. | Rejouer les menus d’installation et Ctrl+Z en interface. |
| [CH00.06](00_SETUP/CH00_06_PROJECT_ORGANIZATION/README.md) | Révisé | Chemins portables, nommage lu par segments et contrôle des ressources à la réouverture. | 3 tests. Arborescence, nommage de référence et contre-exemple. | Vérifier la variante déplacée avec ses textures sur un deuxième poste. |
| [CH00.07](00_SETUP/CH00_07_BACKUP_VERSIONS/README.md) | Révisé | Récupération sur copie et échange de fichiers. | 4 tests. Aller-retour monde GLB, USD, OBJ, FBX et Alembic. | Observer Auto Save et tester une application destinataire. |
| [CH00.08](00_SETUP/CH00_08_PIPELINE_INTRO/README.md) | Révisé | Exemple de découpage et exercice de réduction à 24 secondes. | Correcteur de listes testé. 720 et 576 images vérifiées arithmétiquement à 24 i/s. | Évaluer la lisibilité des coupes sur une animatique. |

### Phase 01

| Chapitre | État | Modifications | Preuves | Suite |
|---|---|---|---|---|
| [CH01.01](01_FUNDAMENTALS/CH01_01_INTERFACE/README.md) | Tutoriel corrigé | Division et réunion des zones avec direction et aperçu. | Manuel Blender 5.3 et deux tests Blender. | Rejouer la nouvelle variante et poursuivre la revue ligne à ligne. |
| [CH01.02](01_FUNDAMENTALS/CH01_02_NAVIGATION/README.md) | Tutoriel corrigé | Sélection du sujet, caméra active, contexte des raccourcis et marche. | Manuel Blender 5.3 et deux tests Blender. | Rejouer le réglage des trois caméras et poursuivre la revue ligne à ligne. |
| [CH01.03](01_FUNDAMENTALS/CH01_03_SELECTION_TRANSFORM/README.md) | Tutoriel précisé | Validation de chaque translation, sélection active et champs Item. | Deux tests Blender. | Rejouer la nouvelle variante et poursuivre la revue ligne à ligne. |
| [CH01.04](01_FUNDAMENTALS/CH01_04_OBJECTS_DATA/README.md) | Tutoriel précisé | Duplication retracée et observation du nombre d’utilisateurs. | Deux tests Blender. | Rejouer la nouvelle variante et poursuivre la revue ligne à ligne. |
| [CH01.05](01_FUNDAMENTALS/CH01_05_EDIT_MODE/README.md) | Révisé | Fusion du faîtage dans le tutoriel et le corrigé, test de continuité. | 4 tests. Toit fermé de 9 faces, contre-exemple historique refusé. | Rejouer les gestes dans l’interface. |
| [CH01.06](01_FUNDAMENTALS/CH01_06_TRANSFORMS_ADVANCED/README.md) | Tutoriel précisé | Placement contrôlé de côté et solution numérique. | Deux tests Blender. | Rejouer l’accrochage avec deux positions de vue. |
| [CH01.07](01_FUNDAMENTALS/CH01_07_ORIGINS_PIVOTS/README.md) | Tutoriel corrigé | Sélection des deux sommets et restauration du pivot après la comparaison. | Deux tests Blender. | Rejouer les trois pivots dans la vue. |
| [CH01.08](01_FUNDAMENTALS/CH01_08_COLLECTIONS_OUTLINER/README.md) | Tutoriel précisé | Contexte de sélection et parentage avec transformation conservée. | Deux tests Blender. | Rejouer le parentage et l’aller-retour de visibilité. |
| [CH01.09](01_FUNDAMENTALS/CH01_09_PROPERTIES_EDITOR/README.md) | Tutoriel précisé | Échantillons d’aperçu et de rendu et accès aux propriétés de scène. | Deux tests Blender et manuel EEVEE. | Rejouer le paramétrage depuis le starter. |
| [CH01.10](01_FUNDAMENTALS/CH01_10_MODIFIERS/README.md) | Tutoriel précisé | Lecture du biseau sous lumière et accès direct au rendu. | Deux tests Blender. | Rejouer la comparaison du bord du seau. |
| [CH01.11](01_FUNDAMENTALS/CH01_11_MATERIALS_BASICS/README.md) | Tutoriel corrigé | Affectation par faces et test de la surface émissive. | Deux tests Blender. | Rejouer l’assignation et la comparaison de lanterne. |
| [CH01.12](01_FUNDAMENTALS/CH01_12_CAMERAS/README.md) | Tutoriel précisé | Comparaison de la profondeur de champ à point fixe. | Deux tests Blender. | Rejouer les cadrages et la comparaison f/2,8 à f/16. |
| [CH01.13](01_FUNDAMENTALS/CH01_13_LIGHTING_BASICS/README.md) | Tutoriel corrigé | Axes de visée du spot et comparaison des trois sources en rendu. | Deux tests Blender et axes du script de scène vérifiés. | Refaire la variation des lampes avec des rendus comparables. |
| [CH01.14](01_FUNDAMENTALS/CH01_14_FIRST_RENDERS/README.md) | Révisé | Parcours CPU/GPU et PNG relu. | 3 tests, dont un rendu CPU de contrôle. | Observer la sortie 1080p sur plusieurs postes. |

### Phase 02

| Chapitre | État | Modifications | Preuves | Suite |
|---|---|---|---|---|
| [CH02.01](02_MODELING/CH02_01_TOPOLOGY/README.md) | Tutoriel repris | Modes de sélection, Grid Fill et fermeture du cylindre. | Trois tests Blender, dont le rejeu du starter en mémoire. | Observer la sélection et le diagnostic à la souris. |
| [CH02.02](02_MODELING/CH02_02_POLY_TOOLS_1/README.md) | Tutoriel repris | Extrusions dirigées et sélection des faces pour Bridge. | Deux cas Blender et manuel de Bridge Edge Loops. | Rejouer les coupes, le raccord et le biseau à la souris. |
| [CH02.03](02_MODELING/CH02_03_POLY_TOOLS_2/README.md) | Tutoriel repris | Exemples de Spin, Knife et Screw avec retour à la scène attendue. | Deux cas Blender et manuel de Spin. | Rejouer les opérations sur la scène transmise. |
| [CH02.04](02_MODELING/CH02_04_NORMALS/README.md) | Tutoriel repris | Orientation, ombrage pondéré et références visuelles. | Deux cas Blender et manuel des normales. | Comparer les reflets au même cadrage. |
| [CH02.05](02_MODELING/CH02_05_HARD_SURFACE/README.md) | Tutoriel repris | Sélection des arêtes et placement numérique des boutons. | Cas de la suite Blender. | Rejouer la sélection des poids de biseau. |
| [CH02.06](02_MODELING/CH02_06_SUBDIVISION/README.md) | Tutoriel repris | Rapport de quatre faces évaluées entre deux niveaux de subdivision. | Cas de la suite Blender. | Lire les compteurs au même cadrage. |
| [CH02.07](02_MODELING/CH02_07_BOOLEANS/README.md) | Tutoriel repris | Profondeur des cutters et condition de la caractéristique d’Euler. | Cas de la suite Blender. | Rejouer la modification d’un seul cutter. |
| [CH02.08](02_MODELING/CH02_08_ORGANIC/README.md) | Tutoriel repris | Contrôle de profondeur et images du squelette et du volume. | Cas de la suite Blender. | Vérifier les formes de jonction à la souris. |
| [CH02.09](02_MODELING/CH02_09_RETOPOLOGY/README.md) | Tutoriel repris | Gestes de Poly Build et inspection de la profondeur. | Cas de la suite Blender et manuel de Poly Build. | Rejouer la retopologie manuelle. |
| [CH02.10](02_MODELING/CH02_10_OPTIMIZATION/README.md) | Tutoriel repris | Comparaison de silhouette et vérification du ratio sur chaque objet lié. | Cas de la suite Blender. | Mesurer les différences à distance fixe. |
| [CH02.11](02_MODELING/CH02_11_UV_BASICS/README.md) | Tutoriel repris | Dépliage par angle et contexte du compactage des UV. | Cas de la suite Blender. | Rejouer les coutures et le compactage. |
| [CH02.12](02_MODELING/CH02_12_ANIMATION_READY/README.md) | Tutoriel repris | Position des boucles par delta et séparation de la flexion simulée et du rig. | Cas de la suite Blender et lecture du calcul de volume. | Comparer les deux poses avec la déformation réelle. |
| [CH02.13](02_MODELING/CH02_13_ASSETS/README.md) | Tutoriel repris | Import Link et Append dans deux scènes distinctes. | Cas de la suite Blender et manuel des bibliothèques. | Rouvrir les deux scènes créées par l’apprenant. |

### Phase 03

| Chapitre | État | Modifications | Preuves | Suite |
|---|---|---|---|---|
| [CH03.01](03_SCULPTING/CH03_01_ARTISTIC_ANATOMY/README.md) | Tutoriel repris | Symétrie des proportions autour du curseur et vérification sur deux vues. | Cas de la suite Blender. | Rejouer les mesures et la variante de pose. |
| [CH03.02](03_SCULPTING/CH03_02_SCULPT_MODE/README.md) | Tutoriel repris | Sélection des brosses par étagère et contrôle du masque. | Cas de la suite Blender et manuel des brosses. | Rejouer les traits et la visibilité des Face Sets. |
| [CH03.03](03_SCULPTING/CH03_03_DYNAMIC_RESOLUTION/README.md) | Tutoriel repris | Fusion contrôlée par sélection liée et résolution adaptative. | Cas de la suite Blender et manuel du remesh. | Rejouer la toute première fusion et le changement de résolution. |
| [CH03.04](03_SCULPTING/CH03_04_STYLIZED/README.md) | Tutoriel repris | Creux booléens et aspect de silhouette pendant la sculpture. | Cas de la suite Blender. | Vérifier le montage interactif des volumes. |
| [CH03.05](03_SCULPTING/CH03_05_REALISTIC/README.md) | Tutoriel repris | Lissage local des raccords du buste. | Cas de la suite Blender. | Rejouer la préparation et les raccords avec les brosses. |
| [CH03.06](03_SCULPTING/CH03_06_FACES/README.md) | Tutoriel repris | Brosses de visage et contrôles de profil au moment du lissage. | Cas de la suite Blender. | Rejouer les brosses dans Blender 5.3. |
| [CH03.07](03_SCULPTING/CH03_07_HANDS_FEET/README.md) | Tutoriel repris | Fusion de la main et continuité du pied vers la cheville. | Cas de la suite Blender. | Rejouer la fusion et inspecter le pied en trois quarts. |
| [CH03.08](03_SCULPTING/CH03_08_CLOTHING/README.md) | Tutoriel repris | Lecture séquentielle de la simulation et comparaison avant application. | Cas de la suite Blender. | Rejouer depuis une copie avec un cache neuf. |
| [CH03.09](03_SCULPTING/CH03_09_RETOPOLOGY/README.md) | Tutoriel repris | Repère local de la grille, projection et inspection de profil. | Cas de la suite Blender. | Rejouer la grille, les anneaux et le Shrinkwrap à la souris. |
| [CH03.10](03_SCULPTING/CH03_10_RIG_READY/README.md) | Tutoriel repris | Application des transformations et position des semelles. | Cas de la suite Blender et rejeu en mémoire sur le starter. | Observer les manipulations et l’export dans une séance débutant. |

### Phase 04

| Chapitre | État | Modifications | Preuves | Suite |
|---|---|---|---|---|
| [CH04.01](04_MATERIALS/CH04_01_UV_UNWRAP/README.md) | Tutoriel repris | Coutures, densité moyenne et damier. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH04.02](04_MATERIALS/CH04_02_PACKING_UDIM/README.md) | Tutoriel repris | Sélection UV par emplacement et séparation 1001–1002. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH04.03](04_MATERIALS/CH04_03_PBR_PRINCIPLED/README.md) | Tutoriel repris | Comparaison PBR à lumière et cadre fixes. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH04.04](04_MATERIALS/CH04_04_SHADER_EDITOR/README.md) | Tutoriel repris | Connexions du graphe et extrêmes du mélange. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH04.05](04_MATERIALS/CH04_05_PROCEDURAL_TEXTURES/README.md) | Tutoriel repris | Inversion du relief, scène corrigée et contre-exemple. | Corrigé relu dans Blender, rendu deux vues, 9 scénarios et ancien corrigé refusé. | Rejouer la procédure et la variante en interface. |
| [CH04.06](04_MATERIALS/CH04_06_TEXTURE_PAINTING/README.md) | Tutoriel repris | Vues à 90°, raccord de texture et persistance. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH04.07](04_MATERIALS/CH04_07_BAKING/README.md) | Tutoriel repris | Image de destination active et bake tangent. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH04.08](04_MATERIALS/CH04_08_RELIEF/README.md) | Tutoriel repris | Subdivision simple déterministe et silhouette de profil. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH04.09](04_MATERIALS/CH04_09_TYPICAL_MATERIALS/README.md) | Tutoriel repris | Comparaison du reflet anisotrope et de la rugosité. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH04.10](04_MATERIALS/CH04_10_CHARACTER_MATERIALS/README.md) | Tutoriel repris | Comparaison SSS à lumière et cadre fixes. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH04.11](04_MATERIALS/CH04_11_COLOR_MANAGEMENT/README.md) | Tutoriel repris | Séparation entre la référence linéaire et son aperçu PNG. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |

### Phase 05

| Chapitre | État | Modifications | Preuves | Suite |
|---|---|---|---|---|
| [CH05.01](05_GEOMETRY_NODES/CH05_01_PRINCIPLES/README.md) | Tutoriel repris | Domaine du Viewer et valeur du champ. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH05.02](05_GEOMETRY_NODES/CH05_02_PROCEDURAL_GEOMETRY/README.md) | Tutoriel repris | Nom Transform Geometry et branches assemblées. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH05.03](05_GEOMETRY_NODES/CH05_03_INSTANCES/README.md) | Tutoriel repris | Composant Instances et nombre de transformées. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH05.04](05_GEOMETRY_NODES/CH05_04_DISTRIBUTION/README.md) | Tutoriel repris | Prises distinctes en modes Random et Poisson. | Prises des deux méthodes confirmées par Blender 5.3 et tests déclarés réussis. | Rejouer la procédure et la variante en interface. |
| [CH05.05](05_GEOMETRY_NODES/CH05_05_ATTRIBUTES/README.md) | Tutoriel repris | Propagation du champ nommé et diagnostic du matériau. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH05.06](05_GEOMETRY_NODES/CH05_06_PARAMETERS/README.md) | Tutoriel repris | Interface du groupe et entrées du modificateur. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH05.07](05_GEOMETRY_NODES/CH05_07_SCATTERING/README.md) | Tutoriel repris | Comparaison des seuils de pente à densité constante. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH05.08](05_GEOMETRY_NODES/CH05_08_ARCHITECTURE/README.md) | Tutoriel repris | Cas d’une seule travée. | Grille à un sommet en X évaluée et tests déclarés réussis. | Rejouer la procédure et la variante en interface. |
| [CH05.09](05_GEOMETRY_NODES/CH05_09_LOOPS/README.md) | Tutoriel repris | Indices de répétition et position de la dernière marche. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH05.10](05_GEOMETRY_NODES/CH05_10_TOOLS/README.md) | Tutoriel repris | Mesure avant et après Realize Instances. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |

### Phase 06

| Chapitre | État | Modifications | Preuves | Suite |
|---|---|---|---|---|
| [CH06.01](06_RIGGING/CH06_01_ARMATURES/README.md) | Tutoriel repris | Symétrie, suffixes et liaison Connected. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH06.02](06_RIGGING/CH06_02_CONSTRAINTS/README.md) | Tutoriel repris | Comparaison de l’ordre des contraintes. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH06.03](06_RIGGING/CH06_03_SKINNING/README.md) | Tutoriel repris | Sélection active avant poids automatiques. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH06.04](06_RIGGING/CH06_04_IK_FK/README.md) | Tutoriel repris | Transition entre IK et FK avec pose alignée. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH06.05](06_RIGGING/CH06_05_HUMANOID/README.md) | Tutoriel repris | Armature In Front et vérification des influences. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH06.06](06_RIGGING/CH06_06_QUADRUPED/README.md) | Tutoriel repris | Normalisation et test de chaque patte. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH06.07](06_RIGGING/CH06_07_MECHANICAL/README.md) | Tutoriel repris | Alignement et longueur du vérin. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH06.08](06_RIGGING/CH06_08_SHAPEKEYS/README.md) | Tutoriel repris | Forme corrective vérifiée à trois angles. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH06.09](06_RIGGING/CH06_09_FACIAL/README.md) | Tutoriel repris | Test indépendant des deux contrôles faciaux. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH06.10](06_RIGGING/CH06_10_CONTROLS/README.md) | Tutoriel repris | Visibilité des os et continuité de la déformation. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH06.11](06_RIGGING/CH06_11_ADVANCED/README.md) | Tutoriel repris | Inspection du tube et de ses B-Bones. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |

### Phase 07

| Chapitre | État | Modifications | Preuves | Suite |
|---|---|---|---|---|
| [CH07.01](07_ANIMATION/CH07_01_PRINCIPLES/README.md) | Correctif ciblé | Clé d’échelle au survol du champ. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH07.02](07_ANIMATION/CH07_02_KEYFRAMES/README.md) | Correctif ciblé | Clés d’emplacement et contrôle des canaux. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH07.03](07_ANIMATION/CH07_03_DOPESHEET/README.md) | Correctif ciblé | Tête de lecture fixée avant le retiming. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH07.04](07_ANIMATION/CH07_04_GRAPHEDITOR/README.md) | Transfert ajouté | Variante propre au chapitre et preuve attendue. | Contrôles du catalogue et référence conservés. | Rejouer la nouvelle variante et poursuivre la revue ligne à ligne. |
| [CH07.05](07_ANIMATION/CH07_05_TIMING/README.md) | Transfert ajouté | Variante propre au chapitre et preuve attendue. | Contrôles du catalogue et référence conservés. | Rejouer la nouvelle variante et poursuivre la revue ligne à ligne. |
| [CH07.06](07_ANIMATION/CH07_06_OVERLAP/README.md) | Transfert ajouté | Variante propre au chapitre et preuve attendue. | Contrôles du catalogue et référence conservés. | Rejouer la nouvelle variante et poursuivre la revue ligne à ligne. |
| [CH07.07](07_ANIMATION/CH07_07_POSING/README.md) | Transfert ajouté | Variante propre au chapitre et preuve attendue. | Contrôles du catalogue et référence conservés. | Rejouer la nouvelle variante et poursuivre la revue ligne à ligne. |
| [CH07.08](07_ANIMATION/CH07_08_WALK/README.md) | Correctif ciblé | Raccord du cycle et plage d’export. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH07.09](07_ANIMATION/CH07_09_RUN_JUMP/README.md) | Correctif ciblé | Échantillons de la parabole et pose de réception. | Corrigé et variantes vérifiés. Positions d’échantillonnage déduites de la gravité à 24 i/s. | Rejouer la procédure et la variante en interface. |
| [CH07.10](07_ANIMATION/CH07_10_ACTING/README.md) | Transfert ajouté | Variante propre au chapitre et preuve attendue. | Contrôles du catalogue et référence conservés. | Rejouer la nouvelle variante et poursuivre la revue ligne à ligne. |
| [CH07.11](07_ANIMATION/CH07_11_FACIAL/README.md) | Transfert ajouté | Variante propre au chapitre et preuve attendue. | Contrôles du catalogue et référence conservés. | Rejouer la nouvelle variante et poursuivre la revue ligne à ligne. |
| [CH07.12](07_ANIMATION/CH07_12_CAMERA/README.md) | Correctif ciblé | Clés de translation de la caméra. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH07.13](07_ANIMATION/CH07_13_NLA/README.md) | Transfert ajouté | Variante propre au chapitre et preuve attendue. | Contrôles du catalogue et référence conservés. | Rejouer la nouvelle variante et poursuivre la revue ligne à ligne. |
| [CH07.14](07_ANIMATION/CH07_14_MOCAP/README.md) | Transfert ajouté | Variante propre au chapitre et preuve attendue. | Contrôles du catalogue et référence conservés. | Rejouer la nouvelle variante et poursuivre la revue ligne à ligne. |
| [CH07.15](07_ANIMATION/CH07_15_DIALOGUE/README.md) | Transfert ajouté | Variante propre au chapitre et preuve attendue. | Contrôles du catalogue et référence conservés. | Rejouer la nouvelle variante et poursuivre la revue ligne à ligne. |

### Phase 08

| Chapitre | État | Modifications | Preuves | Suite |
|---|---|---|---|---|
| [CH08.01](08_SIMULATIONS/CH08_01_RIGID_BODIES/README.md) | Tutoriel repris | Image de bascule Animated et cache. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH08.02](08_SIMULATIONS/CH08_02_SOFT_BODIES/README.md) | Tutoriel repris | Comparaison entre le bord libre et les sommets ancrés. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH08.03](08_SIMULATIONS/CH08_03_CLOTH/README.md) | Tutoriel repris | Relecture séquentielle et invalidation du cache. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH08.04](08_SIMULATIONS/CH08_04_PARTICLES/README.md) | Tutoriel repris | Particules historiques et durée de vie. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH08.05](08_SIMULATIONS/CH08_05_FLUIDS/README.md) | Tutoriel repris | Séquence de calcul des deux caches du liquide. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH08.06](08_SIMULATIONS/CH08_06_SMOKE_FIRE/README.md) | Tutoriel repris | Contrôle du volume et portée du correcteur. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH08.07](08_SIMULATIONS/CH08_07_DESTRUCTION/README.md) | Tutoriel repris | Test d’une paire et comparaison du seuil. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH08.08](08_SIMULATIONS/CH08_08_HAIR_FUR/README.md) | Tutoriel repris | Périmètre du système Hair historique. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH08.09](08_SIMULATIONS/CH08_09_FORCES/README.md) | Tutoriel repris | Comparaison vent et turbulence à graine fixe. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH08.10](08_SIMULATIONS/CH08_10_CACHES/README.md) | Tutoriel repris | Relecture de la même image après réouverture. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |

### Phase 09

| Chapitre | État | Modifications | Preuves | Suite |
|---|---|---|---|---|
| [CH09.01](09_CINEMATOGRAPHY/CH09_01_LIGHT_THEORY/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH09.02](09_CINEMATOGRAPHY/CH09_02_THREE_POINT/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH09.03](09_CINEMATOGRAPHY/CH09_03_NATURAL_HDRI/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH09.04](09_CINEMATOGRAPHY/CH09_04_DRAMATIC/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH09.05](09_CINEMATOGRAPHY/CH09_05_VOLUMETRICS/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH09.06](09_CINEMATOGRAPHY/CH09_06_EXPOSURE/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH09.07](09_CINEMATOGRAPHY/CH09_07_COMPOSITION/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH09.08](09_CINEMATOGRAPHY/CH09_08_LENSES/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH09.09](09_CINEMATOGRAPHY/CH09_09_DEPTH_OF_FIELD/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH09.10](09_CINEMATOGRAPHY/CH09_10_MOVEMENTS/README.md) | Correctif ciblé | Contrôle des plans juste avant et après les coupes. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH09.11](09_CINEMATOGRAPHY/CH09_11_COLOR_EMOTION/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH09.12](09_CINEMATOGRAPHY/CH09_12_STAGING/README.md) | Correctif ciblé | Clés de position et silhouette au cadre. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |

### Phase 10

| Chapitre | État | Modifications | Preuves | Suite |
|---|---|---|---|---|
| [CH10.01](10_RENDERING/CH10_01_EEVEE/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH10.02](10_RENDERING/CH10_02_CYCLES/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH10.03](10_RENDERING/CH10_03_DENOISING/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH10.04](10_RENDERING/CH10_04_PASSES/README.md) | Correctif ciblé | Type Multi-Layer EXR et lecture des passes. | Nom de média lu par RNA dans Blender 5.3. | Rejouer la procédure et la variante en interface. |
| [CH10.05](10_RENDERING/CH10_05_MEMORY/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH10.06](10_RENDERING/CH10_06_EXR_COLOR/README.md) | Correctif ciblé | Réglage de compression après le type de média. | Nom de média et format résultant lus par RNA. | Rejouer la procédure et la variante en interface. |
| [CH10.07](10_RENDERING/CH10_07_BATCH/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |

### Phase 11

| Chapitre | État | Modifications | Preuves | Suite |
|---|---|---|---|---|
| [CH11.01](11_COMPOSITING_VFX/CH11_01_COMPOSITOR/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH11.02](11_COMPOSITING_VFX/CH11_02_MULTIPASS/README.md) | Correctif ciblé | Addition couleur à facteur plein. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH11.03](11_COMPOSITING_VFX/CH11_03_MASKS/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH11.04](11_COMPOSITING_VFX/CH11_04_DEPTH_FX/README.md) | Correctif ciblé | Branchements Image, Depth et Vector documentés. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH11.05](11_COMPOSITING_VFX/CH11_05_GLARE/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH11.06](11_COMPOSITING_VFX/CH11_06_GRADING/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH11.07](11_COMPOSITING_VFX/CH11_07_KEYING/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH11.08](11_COMPOSITING_VFX/CH11_08_TRACKING/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH11.09](11_COMPOSITING_VFX/CH11_09_INTEGRATION/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH11.10](11_COMPOSITING_VFX/CH11_10_CONSISTENCY/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |

### Phase 12

| Chapitre | État | Modifications | Preuves | Suite |
|---|---|---|---|---|
| [CH12.01](12_EDITING_SOUND/CH12_01_VSE/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH12.02](12_EDITING_SOUND/CH12_02_EDITING/README.md) | Correctif ciblé | Bornes exactes du recouvrement et sens du fondu. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH12.03](12_EDITING_SOUND/CH12_03_SOUND/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH12.04](12_EDITING_SOUND/CH12_04_MIX/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH12.05](12_EDITING_SOUND/CH12_05_TITLES/README.md) | Correctif ciblé | Menu réel d’export et contrôle du SRT. | Menu relu dans les sources de Blender 5.3. | Rejouer la procédure et la variante en interface. |
| [CH12.06](12_EDITING_SOUND/CH12_06_EXPORT/README.md) | Correctif ciblé | Type Video, encodage et plage inclusive. | Type Video et format résultant lus par RNA dans Blender 5.3. | Rejouer la procédure et la variante en interface. |

### Phase 13

| Chapitre | État | Modifications | Preuves | Suite |
|---|---|---|---|---|
| [CH13.01](13_PYTHON_AUTOMATION/CH13_01_PYTHON_BASICS/README.md) | Cas approfondi | Mécanisme expliqué, cas pratique et contrôle de transfert. | La preuve correspond aux ressources et tests du dossier. | Vérifier la variante et la revue du livrable. |
| [CH13.02](13_PYTHON_AUTOMATION/CH13_02_BPY_API/README.md) | Cas approfondi | Mécanisme expliqué, cas pratique et contrôle de transfert. | La preuve correspond aux ressources et tests du dossier. | Vérifier la variante et la revue du livrable. |
| [CH13.03](13_PYTHON_AUTOMATION/CH13_03_MESH_MATERIALS/README.md) | Cas approfondi | Mécanisme expliqué, cas pratique et contrôle de transfert. | La preuve correspond aux ressources et tests du dossier. | Vérifier la variante et la revue du livrable. |
| [CH13.04](13_PYTHON_AUTOMATION/CH13_04_PLAN_SETUP/README.md) | Cas approfondi | Mécanisme expliqué, cas pratique et contrôle de transfert. | La preuve correspond aux ressources et tests du dossier. | Vérifier la variante et la revue du livrable. |
| [CH13.05](13_PYTHON_AUTOMATION/CH13_05_BATCH_RENDER/README.md) | Cas approfondi | Mécanisme expliqué, cas pratique et contrôle de transfert. | La preuve correspond aux ressources et tests du dossier. | Vérifier la variante et la revue du livrable. |
| [CH13.06](13_PYTHON_AUTOMATION/CH13_06_QUALITY_CONTROL/README.md) | Cas approfondi | Mécanisme expliqué, cas pratique et contrôle de transfert. | La preuve correspond aux ressources et tests du dossier. | Vérifier la variante et la revue du livrable. |
| [CH13.07](13_PYTHON_AUTOMATION/CH13_07_OPERATORS_UI/README.md) | Cas approfondi | Mécanisme expliqué, cas pratique et contrôle de transfert. | La preuve correspond aux ressources et tests du dossier. | Vérifier la variante et la revue du livrable. |
| [CH13.08](13_PYTHON_AUTOMATION/CH13_08_EXTENSIONS/README.md) | Cas approfondi | Mécanisme expliqué, cas pratique et contrôle de transfert. | La preuve correspond aux ressources et tests du dossier. | Vérifier la variante et la revue du livrable. |
| [CH13.09](13_PYTHON_AUTOMATION/CH13_09_DEBUG_PERFORMANCE/README.md) | Cas approfondi | Mécanisme expliqué, cas pratique et contrôle de transfert. | La preuve correspond aux ressources et tests du dossier. | Vérifier la variante et la revue du livrable. |

### Phase 14

| Chapitre | État | Modifications | Preuves | Suite |
|---|---|---|---|---|
| [CH14.01](14_AI_PRODUCTION/CH14_01_RIGHTS/README.md) | Cas approfondi | Mécanisme expliqué, cas pratique et contrôle de transfert. | La preuve correspond aux ressources et tests du dossier. | Vérifier la variante et la revue du livrable. |
| [CH14.02](14_AI_PRODUCTION/CH14_02_PREPRODUCTION/README.md) | Cas approfondi | Mécanisme expliqué, cas pratique et contrôle de transfert. | La preuve correspond aux ressources et tests du dossier. | Vérifier la variante et la revue du livrable. |
| [CH14.03](14_AI_PRODUCTION/CH14_03_ASSETS/README.md) | Cas approfondi | Mécanisme expliqué, cas pratique et contrôle de transfert. | La preuve correspond aux ressources et tests du dossier. | Vérifier la variante et la revue du livrable. |
| [CH14.04](14_AI_PRODUCTION/CH14_04_ANIMATION/README.md) | Cas approfondi | Mécanisme expliqué, cas pratique et contrôle de transfert. | La preuve correspond aux ressources et tests du dossier. | Vérifier la variante et la revue du livrable. |
| [CH14.05](14_AI_PRODUCTION/CH14_05_DIRECTION/README.md) | Cas approfondi | Mécanisme expliqué, cas pratique et contrôle de transfert. | La preuve correspond aux ressources et tests du dossier. | Vérifier la variante et la revue du livrable. |
| [CH14.06](14_AI_PRODUCTION/CH14_06_CLAUDE_CODE/README.md) | Cas approfondi | Mécanisme expliqué, cas pratique et contrôle de transfert. | La preuve correspond aux ressources et tests du dossier. | Vérifier la variante et la revue du livrable. |
| [CH14.07](14_AI_PRODUCTION/CH14_07_HYBRID_PIPELINE/README.md) | Cas approfondi | Mécanisme expliqué, cas pratique et contrôle de transfert. | La preuve correspond aux ressources et tests du dossier. | Vérifier la variante et la revue du livrable. |

### Phase 15

| Chapitre | État | Modifications | Preuves | Suite |
|---|---|---|---|---|
| [CH15.01](15_SHORT_FILMS/CH15_01_SCRIPT/README.md) | Cas approfondi | Mécanisme expliqué, cas pratique et contrôle de transfert. | La preuve correspond aux ressources et tests du dossier. | Vérifier la variante et la revue du livrable. |
| [CH15.02](15_SHORT_FILMS/CH15_02_STORYBOARD/README.md) | Cas approfondi | Mécanisme expliqué, cas pratique et contrôle de transfert. | La preuve correspond aux ressources et tests du dossier. | Vérifier la variante et la revue du livrable. |
| [CH15.03](15_SHORT_FILMS/CH15_03_ART_DIRECTION/README.md) | Cas approfondi | Mécanisme expliqué, cas pratique et contrôle de transfert. | La preuve correspond aux ressources et tests du dossier. | Vérifier la variante et la revue du livrable. |
| [CH15.04](15_SHORT_FILMS/CH15_04_PLANNING/README.md) | Cas approfondi | Mécanisme expliqué, cas pratique et contrôle de transfert. | La preuve correspond aux ressources et tests du dossier. | Vérifier la variante et la revue du livrable. |
| [CH15.05](15_SHORT_FILMS/CH15_05_PRODUCTION/README.md) | Cas approfondi | Mécanisme expliqué, cas pratique et contrôle de transfert. | La preuve correspond aux ressources et tests du dossier. | Vérifier la variante et la revue du livrable. |
| [CH15.06](15_SHORT_FILMS/CH15_06_FINISHING/README.md) | Cas approfondi | Mécanisme expliqué, cas pratique et contrôle de transfert. | La preuve correspond aux ressources et tests du dossier. | Vérifier la variante et la revue du livrable. |

### Phase 16

| Chapitre | État | Modifications | Preuves | Suite |
|---|---|---|---|---|
| [CH16.01](16_FEATURE_FILMS/CH16_01_DEVELOPMENT/README.md) | Cas approfondi | Mécanisme expliqué, cas pratique et contrôle de transfert. | La preuve correspond aux ressources et tests du dossier. | Vérifier la variante et la revue du livrable. |
| [CH16.02](16_FEATURE_FILMS/CH16_02_SHOT_TRACKING/README.md) | Cas approfondi | Mécanisme expliqué, cas pratique et contrôle de transfert. | La preuve correspond aux ressources et tests du dossier. | Vérifier la variante et la revue du livrable. |
| [CH16.03](16_FEATURE_FILMS/CH16_03_ASSET_MANAGEMENT/README.md) | Cas approfondi | Mécanisme expliqué, cas pratique et contrôle de transfert. | La preuve correspond aux ressources et tests du dossier. | Vérifier la variante et la revue du livrable. |
| [CH16.04](16_FEATURE_FILMS/CH16_04_RENDER_PIPELINES/README.md) | Cas approfondi | Mécanisme expliqué, cas pratique et contrôle de transfert. | La preuve correspond aux ressources et tests du dossier. | Vérifier la variante et la revue du livrable. |
| [CH16.05](16_FEATURE_FILMS/CH16_05_TEAMS/README.md) | Cas approfondi | Mécanisme expliqué, cas pratique et contrôle de transfert. | La preuve correspond aux ressources et tests du dossier. | Vérifier la variante et la revue du livrable. |
| [CH16.06](16_FEATURE_FILMS/CH16_06_BUDGET_RISKS/README.md) | Cas approfondi | Mécanisme expliqué, cas pratique et contrôle de transfert. | La preuve correspond aux ressources et tests du dossier. | Vérifier la variante et la revue du livrable. |
| [CH16.07](16_FEATURE_FILMS/CH16_07_PRODUCTION_MODELS/README.md) | Cas approfondi | Mécanisme expliqué, cas pratique et contrôle de transfert. | La preuve correspond aux ressources et tests du dossier. | Vérifier la variante et la revue du livrable. |
| [CH16.08](16_FEATURE_FILMS/CH16_08_DELIVERY/README.md) | Correctif ciblé | Vérification d’une archive choisie dans le terminal. | Archive de démonstration acceptée. Rejet sur empreinte, puis sur borne SRT après mise à jour de l’empreinte. | Rejouer la réception et lire image, son et sous-titres. |

### Phase 17

| Chapitre | État | Modifications | Preuves | Suite |
|---|---|---|---|---|
| [CH17.01](17_EXPERT_SPECIALIZATIONS/CH17_01_CHARACTER_ARTIST/README.md) | Cas approfondi | Mécanisme expliqué, cas pratique et contrôle de transfert. | La preuve correspond aux ressources et tests du dossier. | Vérifier la variante et la revue du livrable. |
| [CH17.02](17_EXPERT_SPECIALIZATIONS/CH17_02_ENVIRONMENT_ARTIST/README.md) | Cas approfondi | Mécanisme expliqué, cas pratique et contrôle de transfert. | La preuve correspond aux ressources et tests du dossier. | Vérifier la variante et la revue du livrable. |
| [CH17.03](17_EXPERT_SPECIALIZATIONS/CH17_03_TECHNICAL_ARTIST/README.md) | Cas approfondi | Mécanisme expliqué, cas pratique et contrôle de transfert. | La preuve correspond aux ressources et tests du dossier. | Vérifier la variante et la revue du livrable. |
| [CH17.04](17_EXPERT_SPECIALIZATIONS/CH17_04_ANIMATOR/README.md) | Cas approfondi | Mécanisme expliqué, cas pratique et contrôle de transfert. | La preuve correspond aux ressources et tests du dossier. | Vérifier la variante et la revue du livrable. |
| [CH17.05](17_EXPERT_SPECIALIZATIONS/CH17_05_LIGHTING_ARTIST/README.md) | Cas approfondi | Mécanisme expliqué, cas pratique et contrôle de transfert. | La preuve correspond aux ressources et tests du dossier. | Vérifier la variante et la revue du livrable. |
| [CH17.06](17_EXPERT_SPECIALIZATIONS/CH17_06_VFX_ARTIST/README.md) | Cas approfondi | Mécanisme expliqué, cas pratique et contrôle de transfert. | La preuve correspond aux ressources et tests du dossier. | Vérifier la variante et la revue du livrable. |
| [CH17.07](17_EXPERT_SPECIALIZATIONS/CH17_07_TECHNICAL_DIRECTOR/README.md) | Cas approfondi | Mécanisme expliqué, cas pratique et contrôle de transfert. | La preuve correspond aux ressources et tests du dossier. | Vérifier la variante et la revue du livrable. |
| [CH17.08](17_EXPERT_SPECIALIZATIONS/CH17_08_PIPELINE_DEVELOPER/README.md) | Cas approfondi | Mécanisme expliqué, cas pratique et contrôle de transfert. | La preuve correspond aux ressources et tests du dossier. | Vérifier la variante et la revue du livrable. |
| [CH17.09](17_EXPERT_SPECIALIZATIONS/CH17_09_CG_SUPERVISOR/README.md) | Cas approfondi | Mécanisme expliqué, cas pratique et contrôle de transfert. | La preuve correspond aux ressources et tests du dossier. | Vérifier la variante et la revue du livrable. |
| [CH17.10](17_EXPERT_SPECIALIZATIONS/CH17_10_DIRECTOR/README.md) | Cas approfondi | Mécanisme expliqué, cas pratique et contrôle de transfert. | La preuve correspond aux ressources et tests du dossier. | Vérifier la variante et la revue du livrable. |

### Phase 18

| Chapitre | État | Modifications | Preuves | Suite |
|---|---|---|---|---|
| [CH18.01](18_GREASE_PENCIL/CH18_01_SHAPES_VOLUMES/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH18.02](18_GREASE_PENCIL/CH18_02_PERSPECTIVE/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH18.03](18_GREASE_PENCIL/CH18_03_PROPORTIONS_GESTURE/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH18.04](18_GREASE_PENCIL/CH18_04_EXPRESSIONS_CHARACTERS/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH18.05](18_GREASE_PENCIL/CH18_05_COMPOSITION/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH18.06](18_GREASE_PENCIL/CH18_06_GP_INTERFACE/README.md) | Correctif ciblé | Sélecteur de modes et lecture du placement du trait. | Scènes du catalogue contrôlées par la suite Blender. | Rejouer la procédure et la variante en interface. |
| [CH18.07](18_GREASE_PENCIL/CH18_07_BRUSHES_MATERIALS/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH18.08](18_GREASE_PENCIL/CH18_08_LAYERS_MODIFIERS/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH18.09](18_GREASE_PENCIL/CH18_09_DRAWING_IN_3D/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH18.10](18_GREASE_PENCIL/CH18_10_FILM_LANGUAGE/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH18.11](18_GREASE_PENCIL/CH18_11_CONTINUITY/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH18.12](18_GREASE_PENCIL/CH18_12_TECHNICAL_BREAKDOWN/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH18.13](18_GREASE_PENCIL/CH18_13_COMPLEX_BOARDS/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH18.14](18_GREASE_PENCIL/CH18_14_ANIMATIC/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH18.15](18_GREASE_PENCIL/CH18_15_SOUND_EXPORT/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH18.16](18_GREASE_PENCIL/CH18_16_2D_ANIMATION/README.md) | Correctif ciblé | Contexte de Shift+I et lecture dans le Dope Sheet. | Raccourci d’insertion vide vérifié dans la keymap 5.3. | Rejouer la procédure et la variante en interface. |
| [CH18.17](18_GREASE_PENCIL/CH18_17_TIMING_CYCLES/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH18.18](18_GREASE_PENCIL/CH18_18_ACTING_FX/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH18.19](18_GREASE_PENCIL/CH18_19_DRAW_ON_3D/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH18.20](18_GREASE_PENCIL/CH18_20_2D_TO_3D/README.md) | Correctif ciblé | Dégagement de l’inverse du parent et blocage horizontal. | Flèches vérifiées dans la keymap. Parent Inverse vérifié dans le manuel. | Rejouer la procédure et la variante en interface. |
| [CH18.21](18_GREASE_PENCIL/CH18_21_AI_STORYBOARD/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
| [CH18.22](18_GREASE_PENCIL/CH18_22_PROJECTS/README.md) | Transfert ajouté | Variante spécifique et preuve attendue. | Les contrôles de scène existants portent sur les références et contre-exemples. | Rejouer la nouvelle variante en interface. |
