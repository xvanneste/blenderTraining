# CH06.05 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Un squelette de description : des os typés (bras, jambe, colonne…) à ajuster au personnage, à partir duquel Rigify génère le rig final | On ajuste le méta-rig, puis Generate Rig produit le rig avec contrôleurs, IK/FK, mécanismes. |
| Q2 | **b** — Le rig généré reprend les proportions du méta-rig : un méta-rig de 1,98 m donnerait un rig de 1,98 m pour un corps de 1,76 m | Échelle ≈ 0,89 puis Ctrl+A > Scale (échelle de l'objet = 1). |
| Q3 | **c** — 706 | Le méta-rig a 159 bones ; le rig généré 706 (DEF-, ORG-, MCH-, contrôleurs, tweaks). |
| Q4 | — | DEF- : os déformants (ceux qui pèsent sur le maillage) ; ORG- : os d'origine copiés du méta-rig ; MCH- : mécanismes (pas pour l'animateur) ; les autres sont des contrôleurs. |
| Q5 | — | Il a les bras en T et le mannequin en A (40°) : il faut ajuster les os des bras en Edit Mode avant de générer (exercice 3). |
| Q6 | **a** — Les bones déformants (DEF-) | Seuls les bones avec Deform créent des groupes (160 groupes sur le corps). |
| Q7 | **a** — Que la peau couvre tout le corps et suit le rig | Chaque sommet doit suivre : déplacement moyen 0,500 m ; 100 % à plus de 0,4 m. |
| Q8 | — | Pour vérifier la localité du skinning : le pied gauche monte de 0,243 m, le pied droit et la tête ne bougent pas (0,0 mm). |
| Q9 | — | Le rig est décalé de 0,5 m du corps : les poids ne correspondent à rien (le pied ne monte pas) et le correcteur signale l'écart de centrage de 50 cm. |
| Q10 | — | Un rig complet (IK/FK, colonne souple, visage, doigts, collections de bones) en quelques minutes ; le prix : un rig lourd (706 bones) et des conventions à connaître. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
`COMPLETED_EXAMPLES/ch06_05_humanoid_solution.blend` (+ `_reference.png`).

**Fabrication.** Générée par script (`build_ch06_05_files.py`) avec les opérateurs réels : `armature_human_metarig_add`, échelle 0,889 appliquée, bras recalés en Edit Mode (coude et poignet sur l'axe du bras, main et doigts tournés et allongés jusqu'au bout des doigts), `pose.rigify_generate`, `parent_set(type='ARMATURE_AUTO')`, `vertex_group_normalize_all`, `vertex_group_limit_total`. Le corps est celui de la référence de P3. Score du correcteur 54/54 ; starter 2/8 (rig absent : arrêt anticipé). Mesures : voir THEORY.md §3.
Croquis regardé : bones DEF alignés avec les jambes, la colonne et la tête ; bras du rig DANS les bras du mannequin (coudes et poignets à ≤ 1,7 cm du centre de la section) ; pied gauche levé : la jambe du corps suit, l'autre jambe et la tête restent.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_not_generated` | méta-rig ajusté mais rig non généré | Rig généré (arrêt anticipé) |
| `…_unskinned` | rig généré mais corps non lié | Corps lié ; groupes ; sommets pesés ; poids ; mouvements (conséquences) |
| `…_wrong_scale` | méta-rig non mis à l'échelle (rig de 1,98 m) | Taille du rig 1,98 m (seul) |
| `…_no_modifier` | modificateur Armature supprimé | Corps parenté avec modificateur ; mouvements (conséquences) |
| `…_partial_weights` | poids supprimés sous 0,5 m (jambes) | Sommets pesés (77 %) ; racine ; pied |
| `…_offset` | rig décalé de 0,5 m en X avant le skinning | Centrage du rig (50,2 cm) ; pied levé (poids erronés) |
| `…_arms_unfitted` | méta-rig mis à l'échelle mais bras non ajustés | Bras du rig dans les bras du corps (poignet hors du bras) — seul test refusé |
Aussi refusé : le starter.
Le contre-exemple « offset » passait d'abord 50/50 : déplacer le méta-rig en X n'a aucun effet car la génération place le rig à l'origine ; il décale maintenant le rig généré.

## Limites
- Doigts et visage ne sont pas testés ; la déformation des bras en pose n'est pas mesurée (exercice 3).
- Audit du 16/11/2026 : la première version laissait les bras non ajustés (mains hors du maillage) avec un correcteur qui ne le voyait pas ; corrigé (ajustement + test + contre-exemple).
- Les noms des objets (CHR_Hero_Body, META_Hero, RIG_Hero) sont imposés.
