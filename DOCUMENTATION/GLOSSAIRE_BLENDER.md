# Glossaire Blender 5.3

Les noms d’interface sont donnés en anglais avec une explication en français. Pour retrouver un geste, ouvrez le chapitre associé à la définition.

## Se repérer et construire

### Arborescence de la scène · Outliner

Sélectionne et organise les objets, collections et données. La vue de l’arborescence peut afficher la structure de la scène ou les datablocks. [CH01.08](../01_FUNDAMENTALS/CH01_08_COLLECTIONS_OUTLINER/README.md)

### Datablock

Unité de données Blender, comme un maillage, une image ou une action. Deux objets peuvent partager le même maillage et garder leurs propres transformations. [CH01.04](../01_FUNDAMENTALS/CH01_04_OBJECTS_DATA/README.md)

### Origine de l’objet · Object Origin

Repère propre à l’objet. Modifier l’origine permet, par exemple, de faire pivoter une porte sur sa charnière. [CH01.07](../01_FUNDAMENTALS/CH01_07_ORIGINS_PIVOTS/README.md)

### Pivot · Pivot Point

Référence temporaire d’une transformation. Le pivot peut être placé au curseur 3D même si l’origine de l’objet est ailleurs. [CH01.07](../01_FUNDAMENTALS/CH01_07_ORIGINS_PIVOTS/README.md)

### Mode Édition · Edit Mode

Mode qui modifie la géométrie ou les données sélectionnées. Un déplacement de sommets peut laisser inchangée la transformation de l’objet. [CH01.05](../01_FUNDAMENTALS/CH01_05_EDIT_MODE/README.md)

### Normale · Normal

Direction associée à une surface. L’orientation d’une face et la normale d’ombrage ont des rôles différents. [CH02.04](../02_MODELING/CH02_04_NORMALS/README.md)

### Boucle d’arêtes · Edge Loop

Suite d’arêtes que l’on suit dans la topologie. Une boucle peut isoler une zone, guider un chanfrein ou faciliter une flexion. [CH02.01](../02_MODELING/CH02_01_TOPOLOGY/README.md)

### Modificateur · Modifier

Opération évaluée à partir des données d’origine. L’ordre de la pile influence le résultat. Appliquer un modificateur reporte son résultat dans les données. [CH01.10](../01_FUNDAMENTALS/CH01_10_MODIFIERS/README.md)

### Retopologie · Retopology

Reconstruction de la structure d’un maillage pour contrôler les boucles, le budget et les déformations. [CH03.09](../03_SCULPTING/CH03_09_RETOPOLOGY/README.md)

## Surfacer et éclairer

### UV et îlot UV

Coordonnées de repérage sur l’image. Un îlot rassemble des faces contiguës dans le dépliage. Le damier aide à juger échelle et étirement. [CH04.01](../04_MATERIALS/CH04_01_UV_UNWRAP/README.md)

### Tuile UDIM

Partie d’un ensemble d’images adressées par tuile UV. Le nom des fichiers, les numéros et les îlots doivent rester cohérents. [CH04.02](../04_MATERIALS/CH04_02_PACKING_UDIM/README.md)

### Shader

Décrit la réponse d’une surface ou d’un volume à la lumière. Un réseau de nœuds peut faire varier ses paramètres selon la position. [CH04.04](../04_MATERIALS/CH04_04_SHADER_EDITOR/README.md)

### Rugosité · Roughness

Paramètre qui modifie la largeur et la netteté des reflets. Testez-le à lumière fixe pour isoler son effet. [CH04.03](../04_MATERIALS/CH04_03_PBR_PRINCIPLED/README.md)

### Bake · Cuisson

Calcul qui écrit un résultat dans une ressource réutilisable, par exemple une image issue d’un matériau. Le terme s’applique aussi aux caches de simulation. [CH04.07](../04_MATERIALS/CH04_07_BAKING/README.md)

### Bump et déplacement

Le bump modifie l’orientation utilisée par l’ombrage. Un déplacement géométrique peut modifier la silhouette. [CH04.08](../04_MATERIALS/CH04_08_RELIEF/README.md)

### AgX

Transformation de vue. Elle intervient dans la présentation de l’image calculée. Les textures de données et les fichiers de sortie restent des décisions distinctes. [CH04.11](../04_MATERIALS/CH04_11_COLOR_MANAGEMENT/README.md)

### Passe de rendu · Render Pass

Sortie séparée du rendu, par exemple profondeur ou contribution d’éclairage. Chaque passe a un usage et une portée à vérifier. [CH11.02](../11_COMPOSITING_VFX/CH11_02_MULTIPASS/README.md)

## Animer et générer

### Image clé · Keyframe

Échantillon d’une propriété associé à un temps sur la timeline. L’interpolation définit son comportement entre les clés. [CH07.02](../07_ANIMATION/CH07_02_KEYFRAMES/README.md)

### Action

Conteneur réutilisable de données animées. En Blender 5.3, un slot permet d’identifier la cible que sert une partie de l’action. [CH07.03](../07_ANIMATION/CH07_03_DOPESHEET/README.md)

### Courbe d’animation · F-Curve

Représente la propriété animée en fonction du temps. Les poignées de Bézier modifient la vitesse et peuvent produire un dépassement. [CH07.04](../07_ANIMATION/CH07_04_GRAPHEDITOR/README.md)

### Strip NLA

Usage d’une action sur une plage du montage d’animation. Sa position, sa répétition et son influence changent l’évaluation sans déplacer les clés d’origine. [CH07.13](../07_ANIMATION/CH07_13_NLA/README.md)

### Armature et pose

L’armature contient des os et définit leur état de repos. La pose modifie les transformations évaluées pour animer, tester et déformer. [CH06.01](../06_RIGGING/CH06_01_ARMATURES/README.md)

### Poids · Vertex Weight

Contribution d’un groupe à la déformation d’un sommet. Vérifier les groupes voisins en flexion aide à diagnostiquer un pli. [CH06.03](../06_RIGGING/CH06_03_SKINNING/README.md)

### FK et IK

La FK pilote la chaîne par rotation successive de ses éléments. L’IK résout des articulations pour atteindre une cible. [CH06.04](../06_RIGGING/CH06_04_IK_FK/README.md)

### Instance

Occurrence d’une géométrie de référence derrière une transformation. Réaliser une instance produit de la géométrie exploitable par des nœuds qui en ont besoin. [CH05.03](../05_GEOMETRY_NODES/CH05_03_INSTANCES/README.md)

### Champ · Field

Expression évaluée sur les éléments d’un contexte géométrique. Le domaine et le type des données déterminent comment une entrée est lue. [CH05.05](../05_GEOMETRY_NODES/CH05_05_ATTRIBUTES/README.md)

### Cache de simulation

Résultat conservé pour relire une simulation sur une plage. Changer la source du calcul peut exiger une nouvelle cuisson. [CH08.10](../08_SIMULATIONS/CH08_10_CACHES/README.md)

## Produire et livrer

### Link, Append, Library Override

Link garde un lien avec une bibliothèque. Append importe des données locales. Un override permet certaines adaptations locales d’une hiérarchie liée. [CH16.03](../16_FEATURE_FILMS/CH16_03_ASSET_MANAGEMENT/README.md)

### Storyboard et animatique

Le storyboard décrit les plans par images. L’animatique les met en durée et permet de tester coupes, rythme et son avant le layout. [CH15.02](../15_SHORT_FILMS/CH15_02_STORYBOARD/README.md)

### Master et copie de revue

Le master sert à la conservation ou à la fabrication des dérivés selon le cahier des charges. La copie de revue sert à regarder et commenter. [CH16.08](../16_FEATURE_FILMS/CH16_08_DELIVERY/README.md)

### GLB, USD, OBJ

Formats d’échange dont la portée diffère. GLB peut regrouper scène, matériau et animation compatible. USD transporte une scène structurée. OBJ sert surtout à l’échange de géométrie, avec MTL pour les matériaux de l’exercice. [CH00.07](../00_SETUP/CH00_07_BACKUP_VERSIONS/README.md)

### Plage inclusive

Une plage de 1 à 120 contient 120 images. Sa durée à 24 i/s vaut cinq secondes. En production, distinguez la plage du plan, celle du lot et les poignées. [CH16.02](../16_FEATURE_FILMS/CH16_02_SHOT_TRACKING/README.md)
