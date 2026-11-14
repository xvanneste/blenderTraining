# CH00.05 — Leçons

## Leçon 1 — Le système d'extensions et les add-ons livrés
**Niveau :** débutant · **Durée :** 25 min · **Compétence :** C00.05.a
### A. Comprendre
Add-on / extension / dépôt ; add-ons livrés en 5.3. → THEORY.md §1–2.
### B. Observer
Rapport `bcma_extensions_report.py` (tutoriel 1).
### C. Reproduire
Tutoriel 2 (Node Wrangler, Rigify).
### D. Pratiquer
- **Facile :** activez Node Wrangler et Rigify.
- **Moyen :** trouvez l'importeur **BVH** et indiquez dans quelle phase il servira.
- **Difficile :** expliquez pourquoi OBJ/USD/Alembic n'apparaissent pas comme add-ons.
### E. Produire
Fiche de poste : liste des add-ons activés et pourquoi.
### F. Optimiser
Rapport par script plutôt que parcours manuel.
### G. Évaluer
Quiz Q1–Q4.
### H. Consolider
Fiche [CH00_05_extensions.md](../../CHEAT_SHEETS/CH00_05_extensions.md).
### I. Livrables
Rapport + fiche.

## Leçon 2 — Installer en sécurité
**Niveau :** débutant · **Durée :** 30 min · **Compétence :** C00.05.a
### A. Comprendre
Accès en ligne, sources fiables, licence, permissions, lecture du paquet, scripts dans les
`.blend`. → THEORY.md §3–4.
### B. Observer
Le manifeste de `bcma_hello` (ASSETS/bcma_hello/blender_manifest.toml).
### C. Reproduire
Tutoriels 3, 4, 6.
### D. Pratiquer
- **Facile :** exercice 1.
- **Moyen :** exercice 2.
- **Difficile :** exercice 3.
### E. Produire
Mini-projet : politique d'extensions de votre poste.
### F. Optimiser
En production : liste blanche + dépôt interne.
### G. Évaluer
Quiz Q5–Q10.
### H. Consolider
Règle d'or : lire avant d'installer, tester sur une copie.
### I. Livrables
Extension installée puis désinstallée, politique écrite.

## Leçon 3 — Anatomie d'une extension
**Niveau :** débutant · **Durée :** 20 min · **Compétence :** C00.05.b
### A. Comprendre
Manifeste TOML, `register()`/`unregister()`, opérateur, panneau. → THEORY.md §5.
### B. Observer
Lisez `ASSETS/bcma_hello/__init__.py` : repérez la classe opérateur (`bl_idname`), la classe
panneau (`bl_category = "BCMA"`), et le dictionnaire de préfixes.
### C. Reproduire
Tutoriel 5 (validate + build).
### D. Pratiquer
- **Facile :** passez la version à `1.0.1`, reconstruisez.
- **Moyen :** ajoutez `"SPEAKER": "SPK_"` au dictionnaire, reconstruisez, réinstallez, testez.
- **Difficile :** défi 1.
### E–I.
Le développement d'extensions est approfondi en phase 13 (CH13.07–CH13.08).
