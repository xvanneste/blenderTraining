# CH03.05 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — À peu près à la moitié de la hauteur de la tête | Erreur classique du débutant : placer les yeux trop haut. Menton → couronne, les yeux sont vers 50 %. |
| Q2 | — | Racine des cheveux → sourcils, sourcils → base du nez, base du nez → menton : trois hauteurs à peu près égales. |
| Q3 | — | Pour que les outils (rayon de brosse, voxel, Multires), les rendus et les mesures aient un sens, et que le buste s'importe sans mise à l'échelle dans un décor ou un rig. |
| Q4 | **b** — À raccorder les plans en douceur pour que la forme soit crédible | Des blocs juxtaposés se lisent comme des morceaux collés ; la transition les fait lire comme une seule forme. |
| Q5 | — | Primaire : la masse du crâne, le nez, la mâchoire. Secondaire : plis naso-géniens, sillon entre les lèvres, poches sous les yeux. Tertiaire : rides fines du front, pores, grain de peau. |
| Q6 | **c** — Primaire, secondaire, tertiaire | Les détails fins sont détruits par toute modification des grandes masses : on les ajoute en dernier. |
| Q7 | **a** — C et S | C = Clay Strips, S = Smooth ; Shift maintenu pendant un trait = Smooth temporaire, Ctrl = inverser. |
| Q8 | — | Crease Sharp ou Draw Sharp pour le pli (Ctrl maintenu inverse le sens du trait) ; Crease Polish (Shift+C) ou Smooth pour adoucir. Il n'existe pas de brosse nommée simplement « Crease » dans les brosses essentielles 5.3. |
| Q9 | — | Non : le détail ne peut pas être plus fin que la densité. Il faut subdiviser (Multires, niveaux supérieurs) ou refaire un Voxel Remesh avec un Voxel Size plus petit, en gardant une copie du niveau précédent. |
| Q10 | — | Essayer le solveur Manifold (mesuré dans ce chapitre : Exact vide, Manifold correct), vérifier que le maillage est fermé (Voxel Remesh avant), puis contrôler le résultat avant d'appliquer. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`COMPLETED_EXAMPLES/ch03_05_bust_solution.blend` (+ `_reference.png` : face, 3/4, profil).

**Comment elle a été produite.** Le **volume** (blocage, Voxel Remesh, lissage, orbites, yeux, socle) est généré par script (`build_ch03_05_files.py` : opérations non
interactives). Les **détails secondaires et tertiaires sont sculptés à la brosse**, dans Blender 5.2 LTS en interface via le MCP, sur ce volume lisse :
plis naso-géniens (6 passes de *Crease Sharp*, rayon 7 mm), sillon des lèvres, poches sous les yeux, rides du front, pli du menton ; grain de peau par ≈ 900 petites touches aléatoires
de *Draw* de signe alterné (moyenne nulle). Mesures du correcteur sur cette solution : creux de plis **0,68 %**, grain médian **15,6 µm**, score **34/34**.
**Ce que l'essai a appris** : (1) un balayage de *Draw* à texture par lignes régulières donne des **stries horizontales** sur tout le visage (la brosse additive empile la matière)
alors que le correcteur était satisfait (grain 24,7 µm) : rendu refusé, recommencé ; (2) le grain se fait par touches aléatoires de signe alterné ; (3) les plis réels sont plus
profonds (0,68 % de creux) que ceux de la version scriptée (0,10 %).

Construction : 16 ellipsoïdes (crâne, face, mâchoire, menton, arcades, 2 pommettes, nez en 4 pièces, 2 lèvres,
cou, 2 sterno-cléido) + un torse en profil de sections → Join (origine remise à (0, 0, 0)) → Voxel Remesh
2,5 mm → lissage de Taubin (45 itérations : les blocs fondent sans rétrécir) → orbites creusées par deux
Boolean Difference (solveur **Manifold**) → oreilles ajoutées après lissage → Voxel Remesh → Bisect/Fill au
ras du bas → plis secondaires (naso-géniens, sillon labial, mento-labial, poches, rides du front) → grain de
peau → globes `EYE_L` / `EYE_R`.

Mesures du correcteur sur le volume (identiques pour la solution sculptée) : un volume fermé, 74 170 faces, buste 49 cm, socle 680 cm², tête
23,1 cm, largeur/hauteur 0,63, yeux à 55 % de la hauteur de tête, écart des yeux 6,4 cm (44 % de la
largeur), pointe du nez à 33 %, nez en saillie de 3,4 cm, symétrie 100 %, creux de plis 0,10 % des sommets
du visage, grain médian 18,5 µm. Score 33/33.

**Variante apprenant** `ch03_05_bust_learner.blend` : construite exactement comme le TUTORIAL (torse en
ellipsoïdes, lissage plus léger) → validée 33/33. Elle a servi à corriger le tutoriel : la première version
(poitrine plate) donnait un socle de 143 cm², refusé.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut introduit | Verdict attendu et obtenu |
|---|---|---|
| `…_smooth` | aucun pli ni grain (argile lisse) | refusé : secondaires **et** tertiaires |
| `…_no_tertiary` | plis présents, pas de grain | refusé : tertiaires seuls (grain 1,6 µm) |
| `…_no_secondary` | grain présent, pas de plis | refusé : secondaires seuls (creux 0,00 %) |
| `…_eyes_high` | yeux au tiers supérieur (85 % de la tête) | refusé : ligne des yeux |
| `…_lopsided` | tête décalée de 2 cm, nez dévié | refusé : symétrie (61 %) et saillie du nez |
| `…_tiny` | buste réduit de moitié (24 cm) | refusé : échelle, tête, yeux, détails |
Autres refus : le starter (aucun buste) et le buste stylisé de CH03.04 (pas d'yeux, pas de tête mesurable).

**Ce que la contre-épreuve a corrigé** (le correcteur était d'abord « vert à tort » ou « rouge à tort ») :
1. la première version validait `no_secondary` (33/33) : la mesure « énergie de détail » mélangeait plis et
   grain ; remplacée par un comptage de sommets en creux ≥ 0,5 mm (plis) et une **médiane** de l'écart fin
   (grain) — chacun ne voit que son niveau ;
2. la détection du menton donnait 16,9 cm de tête sur la bonne solution (elle s'arrêtait au philtrum) ;
3. les yeux étaient lus par leur origine (à 0 après un Ctrl+A) : on lit désormais le centre de leur boîte
   englobante.

## Limites du correcteur (à connaître)
- Les seuils de détail (0,5 mm de creux, médiane 10 µm) supposent un maillage d'**environ 2–3 mm** d'arête sur
  le visage. Avec un maillage beaucoup plus dense ou plus lâche, relisez les valeurs avec `--debug`.
- Il mesure des **proportions moyennes** avec de larges plages (yeux 42–58 %) ; il ne juge pas la
  ressemblance ni le caractère : c'est la grille d'auto-évaluation.
- Un visage détaillé mais mal proportionné est refusé ; un visage « plausible » mais sans caractère passe.

## Correction a posteriori (session 4)
`SCULPT_Bust` portait une translation de −5 mm **non appliquée** (le `transform_apply` du constructeur échouait sans sélection) et les plis étaient calculés en
coordonnées locales : ils tombaient 5 mm plus bas que prévu. Le constructeur déplace maintenant les sommets (translation identité) ; les plis sont aux bons endroits.
Conséquence : le comptage de creux est passé de 0,17 % à **0,10 %** et le seuil de profondeur de 0,8 mm à **0,5 mm** (solution 0,098 %, sans plis 0,000 %, seuil 0,03 %).
