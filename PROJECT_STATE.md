# PROJECT_STATE — État de production de l'académie

**Dernière mise à jour :** 14/11/2026 · **Session :** 2 interrompue (limite d'usage) — 24 chapitres vérifiés sur 199

> L'état chapitre par chapitre, calculé à partir des fichiers réels, est dans
> **[TASKS.md](TASKS.md)** (régénéré par `python TOOLS/academy_status.py`).
> Ce fichier-ci résume décisions, méthode et prochaine action.

## Résumé
- 19 phases (0–18), **199 chapitres** au cursus (Phase 18 Grease Pencil ajoutée, Phase 17
  détaillée en 10 parcours).
- Phase 0 : **8/8 chapitres terminés et vérifiés**.
- Phase 1 : **14/14 chapitres terminés et vérifiés** + projet P1 (`01_FUNDAMENTALS/PROJECT_P1/`, correcteur validate_p1.py).
- Phase 18 : CH18.01 terminé et vérifié ; bibliothèques `SCRIPTS/bcma_gp.py` (dessin GP par script) et
  `SCRIPTS/bcma_gp_check.py` (correcteur générique piloté par `SCRIPTS/gp_spec.json` de chaque chapitre).
- Phases 2–18 : non commencées (programme détaillé dans CURRICULUM.md et READMEs de phase).
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
| D5 | App de consultation : générateur HTML statique hors ligne (`TOOLS/build_site.py`, à produire) |
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
```
Puis ouvrir `TASKS.md`, prendre le premier chapitre « Non commencé » de l'ordre de production
ci-dessus et appliquer la méthode.

## Prochaine action (reprise exacte)
1. **CH18.03** : scripts, gp_spec, tests et rendu de référence FAITS et passants (3/3) ; il reste
   à écrire THEORY, TUTORIAL, LESSON, EXERCISES, SOLUTIONS, TROUBLESHOOTING, RESOURCES,
   chapter.json, QUIZZES/ch18_03.json, CHEAT_SHEETS, puis render_chapter / register_assets.
2. CH18.04 → CH18.09, puis Phase 2, puis Phase 18 modules C–D, etc. (ordre ci-dessus).
3. Restent aussi : DOCUMENTATION/COMPLEMENTARY_SOFTWARE.md (référencé dans CURRICULUM, encore
   absent), TOOLS/build_site.py (application de consultation), FINAL_AUDIT.md.
