# CH04.06 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — Les UV | Le pinceau projeté sur la surface écrit dans l'image aux coordonnées UV de ce point : des UV propres (CH04.01) sont indispensables. |
| Q2 | **b** — La peinture est perdue à la fermeture du fichier | Une image générée n'existe qu'en mémoire : Image > Pack (ou Save As) avant d'enregistrer le .blend. |
| Q3 | **b** — Un trait en vue de face ne couvre qu'une partie de la surface et se déforme près de la silhouette | Près de la silhouette la surface est vue en rasant : on tourne la vue pour garder des traits propres. |
| Q4 | — | Les pixels hors des îlots ne correspondent à aucun point de l'objet : ils ne sont jamais échantillonnés au rendu. |
| Q5 | — | La peinture donne un contrôle total au pixel mais a une résolution fixe et dépend des UV ; le procédural est sans résolution mais moins précis pour un détail placé. |
| Q6 | **a** — Image > Pack | Le menu Image de l'éditeur d'images contient « Pack » (et « Unpack » quand l'image est déjà empaquetée). |
| Q7 | **b** — Écart de plus de 0,08 par canal avec la couleur dominante (le fond) | Le fond est la couleur la plus fréquente de l'image ; tout pixel qui s'en écarte nettement est considéré peint. |
| Q8 | — | Pour s'assurer d'un vrai travail de peinture (changer de couleur) et pas d'un simple remplissage de l'image avec une seule teinte. |
| Q9 | — | Entre 3 % et 50 % : en dessous rien n'est peint ; au-dessus le fond a probablement été repeint. La solution en couvre 14,6 %. |
| Q10 | — | La propriété color du pinceau est en espace linéaire : il faut convertir la couleur voulue (sRGB) en linéaire ; sinon la peinture paraît délavée (0,8 devient ≈ 0,91 dans l'image). |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`COMPLETED_EXAMPLES/ch04_06_painting_solution.blend` (+ `_reference.png`).

**Fabrication.** Peinte pour de vrai en Texture Paint dans Blender 5.2 piloté par le MCP : l'opérateur `paint.image_paint` reçoit des traits dont les positions d'écran sont calculées par projection 3D → région ; pinceau *Paint Hard* ; quatre vues (0°, 90°, 180°, 270°) ; bande rouge ±0,40 m à mi-hauteur ; cinq pastilles bleues. Image empaquetée, fichier enregistré par la 5.2 (ouverture en 5.3 sans effet). Marqueur `COMPLETED_EXAMPLES/.painted_with_mcp` : `build_ch04_06_files.py` ne l'écrase pas (le repli numpy n'existe que sans marqueur).
Mesures du correcteur : fond (0,80 ; 0,75 ; 0,60) ; couverture 14,6 % ; rouge ≈ 81 % des pixels peints, bleu ≈ 18 % ; hors des îlots UV : 0 % ; score 15/15. Starter : 10/15.

**Ce que le développement a appris** :
1. la couleur du pinceau est linéaire : les premières peintures (rouge pâle, bleu clair) étaient délavées ; après conversion sRGB → linéaire, les pixels valent exactement les couleurs voulues ;
2. `image_paint` exige une clé `location` dans chaque élément de trait et refuse `pen_flip` ;
3. après `open_mainfile`, la projection 3D → écran n'est exacte qu'après un rafraîchissement de la fenêtre (une première version a peint des points au mauvais endroit : le rendu l'a montré) ;
4. une bande de ±0,36 m laissait un trou de ≈ 3° entre vues : portée à ±0,40 m ;
5. des pastilles faites d'un seul petit trait sortaient en « D » : un petit cercle de cinq points donne des disques.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Test qui le refuse |
|---|---|---|
| `…_blank` | rien peint | couverture 0 % (et couleurs 0) |
| `…_one_color` | bande rouge seule | couleurs peintes : 1 (seul test en échec) |
| `…_flood` | image entièrement repeinte (rouge et bleu) | couleurs et peinture hors UV (le fond dominant n'est plus le crème) |
| `…_spill` | aplat vert hors des îlots | peinture hors des îlots : 45 % (seul test en échec) |
| `…_unlinked` | image peinte mais non branchée | T_Can branchée sur Base Color (seul test en échec) |
Aussi refusé : le starter.

## Limites
- Les contre-exemples sont produits en numpy (écriture directe des pixels), pas à la brosse.
- Le correcteur ne détecte pas un repeint complet d'une seule couleur (le fond devient la couleur dominante) : c'est pourquoi le contre-exemple « flood » repeint en deux couleurs.
- Il ne juge ni la netteté des traits ni les bavures aux jonctions.
