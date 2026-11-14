# CH00.03 — Leçons

## Leçon 1 — Comment Blender utilise CPU, GPU, RAM et VRAM
**Niveau :** débutant · **Durée :** 20 min · **Prérequis :** CH00.01–02 · **Compétence :** C00.03.a

### A. Comprendre
Notion de **budget** ; tableau « qui fait quoi » ; viewport lent ≠ GPU faible. → THEORY.md §1–2.
### B. Observer
Ouvrez le Gestionnaire des tâches Windows (`Ctrl+Shift+Échap` → *Performances*) à côté de
Blender, puis lancez un rendu `F12` en Cycles CPU, puis GPU : observez quel graphique monte.
### C. Reproduire
Notez dans la fiche de poste quelle ressource sature pour : rendu CPU, rendu GPU, rotation
du viewport.
### D. Pratiquer
- **Facile :** quiz Q1–Q3.
- **Moyen :** pour 5 tâches (simulation de fumée, rendu EEVEE, Geometry Nodes, montage,
  rendu Cycles GPU), prédisez la ressource critique puis justifiez.
- **Difficile :** expliquez pourquoi acheter une carte graphique plus puissante n'accélère
  pas un viewport ralenti par 300 personnages animés (déformations).
### E. Produire
Section 6 de la fiche de poste : « goulots d'étranglement de mon poste ».
### F. Optimiser
Manuel (gestionnaire des tâches) → Pro (statistiques Blender + `--cycles-print-stats` en
ligne de commande) → Automatisé (`bcma_scene_cost.py`).
### G. Évaluer
Quiz Q1–Q4.
### H. Consolider
Une ressource saturée à la fois : identifiez-la avant d'optimiser.
### I. Livrables
Fiche de poste §6.

---

## Leçon 2 — Backend graphique : Vulkan et OpenGL
**Niveau :** débutant · **Durée :** 10 min · **Compétence :** C00.03.a
### A. Comprendre
Backend = langue CPU→GPU pour l'affichage ; Vulkan par défaut en 5.3 ; n'affecte pas
Cycles. → THEORY.md §3.
### B–C. Observer / Reproduire
TUTORIAL.md tutoriel 6 (sans changer si tout fonctionne).
### D. Pratiquer
- **Facile :** trouvez le réglage *Backend*.
- **Moyen :** lancez `blender_startup_opengl.cmd` et vérifiez dans *Help → About* ou dans
  le rapport système (`gpu_ui_backend`) le backend actif.
- **Difficile :** rédigez la procédure que vous suivriez si le viewport clignote après une
  mise à jour de pilote.
### E–I.
Quiz Q5–Q6 ; consolidez avec la fiche de révision.

---

## Leçon 3 — Lire les statistiques et estimer le coût au rendu
**Niveau :** débutant · **Durée :** 25 min · **Compétence :** C00.03.b
### A. Comprendre
Statistiques = viewport ; coût au rendu = faces × 4^niveaux de subdivision rendu.
→ THEORY.md §5.
### B. Observer
Starter : barre d'état ≈ 320 000 faces, estimation au rendu 16,4 M.
### C. Reproduire
TUTORIAL.md tutoriel 1.
### D. Pratiquer
- **Facile :** calculez à la main : ico-sphère de 80 faces, Subdivision 3 → ? (5 120)
- **Moyen :** un personnage de 20 000 faces avec Subdivision Render 2 dans une foule de 50 :
  combien de faces ? (16 M) Est-ce raisonnable ? Que proposeriez-vous ?
- **Difficile :** exercice 2.
### E. Produire
Tableau « coût » d'une de vos scènes futures (à reprendre en phase 1).
### F. Optimiser
`bcma_scene_cost.py` vous évite le calcul manuel ; il sera intégré à vos scripts de
contrôle qualité (phase 13).
### G–I.
Quiz Q7–Q9.

---

## Leçon 4 — Les leviers d'optimisation
**Niveau :** débutant · **Durée :** 35 min · **Compétence :** C00.03.b
### A. Comprendre
Partage de données, subdivision raisonnable, Simplify, instances, textures. → THEORY.md §6.
### B. Observer
Comparez dans l'Outliner (mode *Blender File*) le nombre de *Meshes* du starter (202) et
de la solution (3).
### C. Reproduire
TUTORIAL.md tutoriels 2, 3, 4, 5.
### D. Pratiquer
- **Facile :** exercice 1.
- **Moyen :** exercice 2.
- **Difficile :** exercice 3 (sans procédure, correcteur).
### E. Produire
Mini-projet (rapport d'optimisation).
### F. Optimiser
| Méthode | Description | Compromis |
|---|---|---|
| Manuelle | Modifier chaque galet | Lent, erreurs |
| Pro | Sélection + `Ctrl+L` + *Copy to Selected* + Simplify | Rapide, nécessite de bien gérer l'objet actif |
| Automatisée | Script (phase 13) qui relie les maillages identiques et plafonne la subdivision | Instantané, à valider visuellement |
### G. Évaluer
Correcteur `validate_ch00_03.py --exercise optimize`, quiz Q10–Q12.
### H. Consolider
Fiche [CH00_03_performance.md](../../CHEAT_SHEETS/CH00_03_performance.md).
### I. Livrables
`ch00_03_heavy_scene_<prenom>_v001.blend` validé + rapport.
