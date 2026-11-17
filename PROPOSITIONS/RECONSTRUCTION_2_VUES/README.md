# Personnage reconstruit depuis deux vues

## Marche et finition du pantalon

[Vidéo MP4](marche_personnage_0001-0096.mp4) · [Scène de marche](personnage_marche.blend) · [Contrôle des appuis](verification_marche.json) · [Script reproductible](animate_walk.py) · [Skill IA](../../SKILLS/blender-character-workflow/SKILL.md)

Cette scène reprend le personnage anatomique et redessine le bas du pantalon autour de la cheville. Les ourlets ont une coupe plus régulière. La marche avance sur le sol pendant 96 images à 24 i/s. Le tronc suit une trajectoire linéaire, les bras compensent le mouvement et chaque cible de pied reste fixe dans le monde pendant l’appui. Les repères dans la chronologie marquent les contacts. Les anciennes poses restent dans les fichiers précédents.

Le personnage a d’abord été testé comme volume issu des silhouettes. Cette approche donnait un contour utile, mais effaçait le visage. La reprise s’appuie sur une topologie anatomique continue avec UV et poids correspondants, puis sur des contrôles séparés de la forme, de l’habillage et du mouvement. Le skill reprend les décisions qui changent le résultat et les vérifications à refaire sur un autre personnage.

## Personnage final

[Version avec pieds anatomiques ajustés](personnage_final_pieds_ajustes.blend) · [Coupe du chaussant](pied_chaussure_coupe.png) · [Cheville en flexion](pieds_ajustes_pose.png)

Les pieds sont intégrés au maillage du corps. L’avant-pied, le talon et le cou-de-pied sont ajustés sous la tige. Les ourlets dégagent les chevilles. Le rig conserve les modes FK et IK. La coupe est un aperçu de vérification.

[Version avec chaussures basses](personnage_final_chaussures.blend) · [Gros plan](chaussures_detail.png) · [Vérification de l’appui](chaussures_appui.png)

Cette variante remplace les bottes par des chaussures en toile à lacets. Elle conserve les réglages FK et IK du personnage final. Les chaussures ont leur carte `UV_Chaussure`.

[Fichier Blender](personnage_final.blend) · [Personnage entier](personnage_final.png) · [Portrait](personnage_final_portrait.png) · [Pose de contrôle](personnage_final_pose.png)

Le fichier réunit le corps continu, la coiffure ajustée au crâne, les sourcils, les vêtements avec leurs finitions et les bottes corrigées. L’atlas peau 2048 et les gabarits sont intégrés au fichier. Le matériau de projection du premier essai reste disponible dans les slots de `GEO_Personnage`.

- **Poses FK.** Ouvrez les images 1, 25 et 49 dans la chronologie. Le fichier s’ouvre à l’image 1.
- **Pieds IK.** À l’image 1, sélectionnez `RIG_Personnage_FK`. Dans les propriétés de l’armature, affichez la collection **Pieds · IK**. Réglez la propriété personnalisée de l’objet **Pieds IK** sur 1. En mode Pose, déplacez un os `CTRL_Pied_IK`. Le contrôleur `CTRL_Genou` règle la direction de la flexion. Repassez la propriété à 0 pour retrouver les poses FK.
- **Visage.** Sur `GEO_Personnage`, la clé de forme **Sourire léger** se règle de 0 à 1. Les autres déformations faciales restent accessibles par les os MakeHuman. Le fichier ne contient pas de système complet de lip-sync.

Le [script de finition](finish_character.py) part de la version aux pieds corrigés. Le maillage anatomique, les UV, le squelette et les poids de départ sont issus de [MakeHuman sous CC0](https://github.com/makehumancommunity/makehuman/blob/a8bc2d54ff0ac92e78ff71431b1023eda42bf482/LICENSE.md).

## Personnage entier · UV et rig

[Version avec les pieds corrigés](personnage_corps_uv_rig_pieds.blend) · [Détail des bottes](bottes_v2_detail.png) · [Appui en pose](bottes_v2_appui.png)

Les bottes corrigées ont leur propre carte UV, une semelle plate et un col avec une ouverture pour le pantalon. Les poids passent du pied au bas de jambe sur la tige. Le pied porteur a été contrôlé aux images 1, 25, 49 et 73. Le rig de cette version reste FK.

[Fichier Blender](personnage_corps_uv_rig.blend) · [Pose neutre](personnage_neutre.png) · [Pose FK de contrôle](personnage_pose_fk.png) · [Atlas couleur 2048](atlas_personnage_2048.png)

Sélectionnez `GEO_Personnage` et ouvrez **UV Editing** pour afficher `UV_Atlas`. Le matériau utilise cette carte UV et la texture couleur intégrée. Le tee-shirt et le pantalon sont des maillages ajustés sur le corps et pondérés sur la même armature. Les bottes suivent les os des pieds.

Sélectionnez `RIG_Personnage_FK`, puis passez en **mode Pose**. Les images **1, 25, 49 et 73** de la chronologie contiennent le repos, deux poses de contrôle et le retour au repos. Les commandes visibles sont les os FK du corps. Affichez les collections Doigts, Visage et Os intermédiaires dans les propriétés de l’armature pour voir les autres os. Le rig permet de tester les déformations sans configuration supplémentaire. Les contrôleurs IK, les expressions faciales et la retouche artistique des poids restent à faire.

Le [script](build_body_uv_rig.py) ajuste une base anatomique continue, ses UV, son squelette et ses poids [MakeHuman sous CC0](https://github.com/makehumancommunity/makehuman/blob/a8bc2d54ff0ac92e78ff71431b1023eda42bf482/LICENSE.md). Il conserve les deux vues comme gabarits. La ressemblance avec l’illustration, la coiffure et les détails des vêtements restent à affiner.

## Deuxième essai · ajustement anatomique du visage

[Buste ajusté dans Blender](visage_recale.blend) · [Argile de face](visage_recale_face.png) · [Argile de profil](visage_recale_profil.png) · [Essai de projection couleur](visage_recale_projection.png)

Le [script d’ajustement](fit_anatomy.py) part du maillage et du morphotype adulte de MakeHuman, distribués sous [CC0](https://github.com/makehumancommunity/makehuman/blob/a8bc2d54ff0ac92e78ff71431b1023eda42bf482/LICENSE.ASSETS.md). Les deux fichiers sources proviennent du commit `a8bc2d54ff0ac92e78ff71431b1023eda42bf482`. Les correspondances verticales et les corrections de largeur et de profondeur utilisent les mêmes gabarits. Le crâne, la mâchoire, les oreilles, le cou et les épaules appartiennent au maillage anatomique continu. Les yeux restent des objets séparés.

Les deux rendus de contrôle utilisent l’argile neutre. La projection couleur reste stockée comme matériau séparé dans le fichier et montre un essai de lecture du personnage avec les couleurs des gabarits. Une ressemblance finale demanderait de reprendre à la main les paupières, la forme des lèvres, l’angle mandibulaire et la coiffure. Cet essai porte sur le buste.

## Premier essai · extraction des silhouettes

[Scène Blender](personnage_deux_vues.blend) · [Référence de face](reference_face.png) · [Référence de profil](reference_profil.png) · [Aperçu du maillage](maillage_trois_quarts.png)

La planche a été créée avec l’outil de génération d’images intégré. Les deux panneaux ont été extraits de la même planche pour conserver leur alignement. Le script lit les deux silhouettes ligne par ligne. À chaque hauteur, la face donne les largeurs et le profil donne les profondeurs. Les régions masquées, comme une partie du torse derrière le bras, utilisent des sections estimées. Une seule extraction de surface forme le personnage.

Dans Blender, **Pavé num. 1** affiche la face et **Pavé num. 3** le profil. Les deux références sont intégrées dans le fichier. Activez le mode Édition (**Tab**) pour revoir la grille du modèle. L’objet de la collection **03 · Correspondances exactes** contient les 25 points tracés. Affichez-le dans l’Outliner, puis passez en mode Édition pour sélectionner ses sommets. Les groupes du personnage désignent le sommet de surface le plus proche de chaque point. Un repère d’articulation peut être au milieu du volume et donc à une certaine distance de la surface. [Coordonnées et projections](correspondances.json)

Le maillage a été rouvert et contrôlé dans Blender 5.3 : une coque connectée, 34 532 sommets, 34 530 quads, aucune arête ouverte ou non-manifold. Il sert de blocage 3D. Deux vues déterminent les contours et certains repères visibles. Les détails du visage, le dos et les volumes entre les caméras demandent encore une passe de modélisation.

## Prompt de la planche

Create ONE wide 3D character modelling turnaround reference sheet, with exactly two orthographic reference images side by side in equal square panels. Same original stylized adult male character, long slender heroic face with clear angular cheekbones, natural nose and lips, close-cropped dark hair (visible exact head outline), slim athletic build, fitted slate-blue short-sleeved athletic top and fitted charcoal straight trousers, flat simple fitted boots. Entire figure visible including feet with margins, on perfectly flat plain off-white background, no text, no axes, no props, no cast shadow. Left panel true straight FRONT view (no yaw or pitch); right panel true SIDE profile view, nose facing left, exactly 90 degrees (see one eye, one ear, near foot may occlude far foot). Neutral relaxed A pose with arms 18 degrees from torso, hands neutral with fingers together; legs straight about hip width, both feet point directly forward. Same pose and clothing across views, identically scaled and aligned to an imaginary horizontal grid: crown, chin, shoulders, elbows, wrists, hips, knees, boot soles at identical heights. Flat neutral diffuse lighting, appealing precise stylized animation concept, high contrast clean silhouettes. Right panel centered around body axis with good margin on all sides. Whole body only, no duplicates, no inset portraits. Joint and facial positions should be easy to trace for 3D reconstruction. Landscape aspect ratio.
