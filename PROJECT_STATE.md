# PROJECT_STATE — État de production de l'académie

**Dernière mise à jour :** 14/11/2026 · **Session :** 3 — 61 chapitres vérifiés sur 199

> L'état chapitre par chapitre, calculé à partir des fichiers réels, est dans
> **[TASKS.md](TASKS.md)** (régénéré par `python TOOLS/academy_status.py`).
> Ce fichier-ci résume décisions, méthode et prochaine action.

## Résumé
- 19 phases (0–18), **199 chapitres** au cursus (Phase 18 Grease Pencil ajoutée, Phase 17
  détaillée en 10 parcours).
- Phase 0 : **8/8 chapitres terminés et vérifiés**.
- Phase 1 : **14/14 chapitres terminés et vérifiés** + projet P1 (`01_FUNDAMENTALS/PROJECT_P1/`, correcteur validate_p1.py).
- Phase 18 : CH18.01 à CH18.22 terminés (phase 18 complète) et vérifiés (modules A et B complets, C en cours) ; bibliothèques `SCRIPTS/bcma_gp.py` (dessin GP par script) et
  `SCRIPTS/bcma_gp_check.py` (correcteur générique piloté par `SCRIPTS/gp_spec.json` de chaque chapitre).
- Phase 2 : **13/13 chapitres terminés et vérifiés** + projet P2 (`02_MODELING/PROJECT_P2/`, validate_p2.py testé par test_p2.py).
- Phases 3–17 et Phase 18 modules C–G : non commencés (programme détaillé dans CURRICULUM.md et READMEs de phase).
- État exact et à jour : `python TOOLS/academy_status.py` → TASKS.md.

## Méthode de production d'un chapitre (à suivre à l'identique)
1. Vérifier les fonctions/libellés dans Blender 5.3 (API `-b --python-expr`, sources
   `5.3/scripts/startup/bl_ui/*.py`, keymap `blender_default.py`).
2. Écrire `SCRIPTS/build_chNN_MM_files.py` (utilise `SCRIPTS/bcma_lib.py`) → starters + solutions.
3. Écrire `SCRIPTS/validate_chNN_MM.py` (classe `L.Report`) et `SCRIPTS/tests.json`.
4. `python TOOLS/run_all_tests.py CHNN_MM` jusqu'à 0 échec ; contrôler visuellement un rendu si utile.
5. Écrire `chapter.json`, `QUIZZES/chNN_MM.json`, `THEORY.md`, `TUTORIAL.md`, `LESSON.md`,
   `EXERCISES.md`, `SOLUTIONS.md`, `TROUBLESHOOTING.md`, `RESOURCES.md`, fiche `CHEAT_SHEETS/`.
6. `python TOOLS/render_chapter.py <dossier>` (README + QUIZ + réponses du quiz dans SOLUTIONS).
7. `python TOOLS/register_assets.py <dossier>` puis `python TOOLS/check_manifest.py --update-hashes`.
8. `python TOOLS/academy_status.py` (TASKS.md + tableaux des README de phase).

## Outils de l'académie
| Outil | Rôle |
|---|---|
| `SCRIPTS/bcma_lib.py` | Bibliothèque Blender partagée (scène, matériaux, lumières, caméra, Report, rendu de contrôle) |
| `SCRIPTS/bcma_naming_check.py` | Contrôle des conventions dans un .blend |
| `SCRIPTS/bcma_backup.py` | Sauvegarde zip datée et vérifiée |
| `SCRIPTS/bcma_shotlist_check.py` | Vérification de shot list CSV |
| `TOOLS/run_all_tests.py` (+ `.ps1`) | Tests découverts via `*/CH*/SCRIPTS/tests.json`, résultats fusionnés dans `TOOLS/last_test_results.json` |
| `TOOLS/render_chapter.py` | README + QUIZ depuis `chapter.json` et `QUIZZES/*.json` |
| `TOOLS/register_assets.py` | Enregistre les ressources générées dans `ASSET_MANIFEST.json` |
| `TOOLS/check_manifest.py` | Cohérence + empreintes SHA-256 du manifeste |
| `TOOLS/academy_status.py` | Inventaire réel → `TASKS.md`, tableaux des README de phase |

## Décisions
| # | Décision |
|---|---|
| D1 | Blender 5.3.0 = référence gelée |
| D2 | Interface en anglais, cours en français |
| D3 | Tous les .blend générés par script + correcteur automatique |
| D4 | Dossiers `NN_PHASE/CHNN_MM_NOM/` |
| D5 | App de consultation : générateur HTML statique hors ligne (`TOOLS/build_site.py` → `SITE/`, produit et testé le 14/11/2026) |
| D6 | Quiz en JSON (`QUIZZES/`) → QUIZ.md généré |
| D8 | Phase 18 (Grease Pencil) transversale, modules A–D obligatoires avant la phase 15 |
| D9 | Ordre de production = ordre d'apprentissage, pour que l'apprenant puisse commencer immédiatement |
| D10 | Aucun logiciel tiers téléchargé/installé sans accord explicite de l'utilisateur |

## Ordre de production (lots)
1. ✅ Phase 0 · 2. Phase 1 · 3. Phase 18 modules A–B · 4. Phase 2 · 5. Phase 18 modules C–D ·
6. Phases 3, 4 · 7. Phase 5 · 8. Phases 6, 7 · 9. Phase 18 modules E–G · 10. Phases 8–12 ·
11. Phases 13, 14 · 12. Phases 15, 16, 17 · en parallèle : `DOCUMENTATION/COMPLEMENTARY_SOFTWARE.md`,
`TOOLS/build_site.py` (application), `FINAL_AUDIT.md`.

## Limites connues
- Pas de captures d'écran d'interface (Blender piloté en arrière-plan) : schémas texte, SVG et rendus.
- Les écrans du premier lancement sont décrits d'après le manuel.
- Les nouveautés 5.3 annoncées par la presse sont revérifiées dans l'API au moment de leur chapitre
  (système de projet : vérifié en CH00.06).

## Reprise après interruption
```powershell
cd G:\_formation\blender\BLENDER_CINEMA_MASTER_ACADEMY
python TOOLS\academy_status.py          # où en est-on ?
python TOOLS\run_all_tests.py --no-build # tout est-il vert ?
python TOOLS\build_site.py              # régénérer l'application SITE/
python TOOLS\final_audit.py             # régénérer FINAL_AUDIT.md (état réel)
```
Puis ouvrir `TASKS.md`, prendre le premier chapitre « Non commencé » de l'ordre de production
ci-dessus et appliquer la méthode.

## Prochaine action (reprise exacte)
1. **Phase 18 COMPLÈTE** (CH18.01–CH18.22, 7 projets obligatoires avec correcteur `validate_ch18_22.py -- --exercise p1…p7`).
   Phase 3 : CH03.01–04 FAITS ; reprendre à **CH03.05** Sculpture réaliste (`03_SCULPTING/CH03_05_REALISTIC/`), puis phase 4, 5, 6–7, 8–12, 13–14, 15–17.
   Outils ajoutés : SCRIPTS/bcma_shots.py (valeurs de plans mesurées), bcma_gp.polyline_clipped.
2. Après chaque chapitre : render_chapter, register_assets, check_manifest --update-hashes,
   academy_status, build_site, final_audit.
3. Fait en session 3 : CH18.03 → CH18.09 ; Phase 2 complète (CH02.01–CH02.13 + P2) ; DOCUMENTATION/COMPLEMENTARY_SOFTWARE.md ; application
   `SITE/` (TOOLS/build_site.py, testée dans un navigateur : navigation, quiz, recherche, mobile) ;
   `FINAL_AUDIT.md` généré par TOOLS/final_audit.py.
   Découvertes vérifiées (CLAUDE.md, pièges) : passe Z pour l'occlusion GP/3D au rendu ; remplissages
   GP portés par trait (`fill_id`) ; `use_lights` ; masque caché inactif (opacité 0) ; libellés 5.3.
