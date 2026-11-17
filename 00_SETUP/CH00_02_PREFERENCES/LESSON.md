# CH00.02 — Leçons

## Leçon 1 — La fenêtre Preferences et ses sauvegardes
**Niveau :** débutant · **Durée :** 25 min · **Prérequis :** CH00.01 · **Compétences :** C00.02.a, C00.02.b

### A. Comprendre
Préférences (`userpref.blend`, comportement du logiciel) ≠ fichier de démarrage
(`startup.blend`, contenu de *File → New*) ≠ réglages de scène (dans chaque `.blend`).
→ THEORY.md §1–2.

### B. Observer
Ouvrez *Edit → Preferences*, recherchez « undo », ouvrez le menu ☰. Notez que la fenêtre
est **indépendante** du fichier ouvert : ouvrez un autre `.blend`, les préférences ne
changent pas.

### C. Reproduire
TUTORIAL.md — tutoriels 1 (sauvegarde du dossier config) et 2 (visite).
✅ Archive `config_5.3_<date>.zip` créée. L’état de *Auto-Save Preferences* est relevé.

### D. Pratiquer
- **Facile :** trouvez par la recherche les réglages *Save Versions*, *Resolution Scale*,
  *Emulate Numpad* et notez leur catégorie.
- **Moyen :** changez le thème, puis annulez avec *Revert to Saved Preferences*… Ça ne
  marche pas ? Expliquez pourquoi (indice : auto-save).
- **Difficile :** exercice 4 de EXERCISES.md (restauration complète).

### E. Produire
Section 5 de la fiche de poste : liste de vos réglages modifiés.

### F. Optimiser
Manuel (fenêtre) → Pro (script `bcma_prefs_profile.py --apply --save`) → Automatisé
(même script lancé à chaque installation de poste). Compromis : le script est rapide et
reproductible, mais vous devez comprendre chaque réglage qu'il applique.

### G. Évaluer
Quiz Q1–Q4.

### H. Consolider
Trois fichiers, trois rôles. Sauvegardez `config\` avant toute expérimentation.

### I. Livrables
`config_5.3_<date>.zip`.

---

## Leçon 2 — Interface : échelle, thème, langue, barre d'état
**Niveau :** débutant · **Durée :** 20 min · **Prérequis :** L1 · **Compétence :** C00.02.a

### A. Comprendre
Resolution Scale pour la lisibilité ; anglais comme langue de référence ; barre d'état
comme tableau de bord (statistiques, mémoire, VRAM, version). → THEORY.md §3.

### B. Observer
Ouvrez `ch00_02_navigation_playground.blend` avec les *Scene Statistics* affichées :
lisez le nombre d'objets (≈ 404) et de faces. Ces chiffres seront vos repères de
« lourdeur » d'une scène.

### C. Reproduire
TUTORIAL.md — tutoriel 3. ✅ Barre d'état complète.

### D. Pratiquer
- **Facile :** réglez une Resolution Scale confortable.
- **Moyen :** sélectionnez 10 bâtiments (`Shift`+clic) : observez la barre d'état passer
  de `0/404` à `10/404` objets sélectionnés.
- **Difficile :** activez la traduction française de l'interface mais **pas** des
  infobulles (*Tooltips*) ; expliquez l'intérêt de ce compromis.

### E. Produire
Capture de votre interface réglée → `PORTFOLIO/setup/interface.png`.

### F. Optimiser
Un thème exporté (*Themes → Export*) se réinstalle en un clic sur un autre poste.

### G. Évaluer
Quiz Q5–Q6.

### H. Consolider
Interface en anglais, statistiques visibles en permanence.

### I. Livrables
Capture d'écran.

---

## Leçon 3 — Navigation : orbite, zoom, profondeur, émulations
**Niveau :** débutant · **Durée :** 35 min · **Prérequis :** L2 · **Compétence :** C00.02.c

### A. Comprendre
Quatre réglages (Orbit Around Selection, Zoom to Mouse Position, Auto Depth, Auto
Perspective) + deux émulations + deux gestes clés (`.` Frame Selected, `Home` Frame All).
→ THEORY.md §4.

### B. Observer
Dans la ville, **sans** les réglages : orbitez autour d'un bâtiment éloigné — il sort de
l'écran. **Avec** Orbit Around Selection : il reste au centre.

### C. Reproduire
TUTORIAL.md — tutoriels 4 et 7.

### D. Pratiquer
- **Facile :** exercice 1 (EXERCISES.md).
- **Moyen :** exercice 2 (cadrer deux objets et expliquer le geste).
- **Difficile :** exercice 3 (cadrer l'aiguille avec la caméra) — correcteur automatique.

### E. Produire
Fichier `ch00_02_navigation_<prenom>_v001.blend` validé.

### F. Optimiser
| Méthode | Temps typique pour trouver l'aiguille |
|---|---|
| Orbite/zoom à l'œil, réglages d'usine | 1 à 5 min |
| Avec les réglages du profil | 30 s à 2 min |
| Outliner + Frame Selected (`.`) | < 10 s |
Leçon : **la sélection précède la navigation**.

### G. Évaluer
Quiz Q7–Q10, correcteur `--exercise needle`.

### H. Consolider
`.` = Frame Selected, `Home` = Frame All, `Ctrl+Alt+Num 0` = caméra sur la vue.

### I. Livrables
Fichier validé + vos temps dans PROGRESS.md (journal des tests de rapidité).

---

## Leçon 4 — Édition et sécurité
**Niveau :** débutant · **Durée :** 25 min · **Prérequis :** L1 · **Compétences :** C00.02.a, C00.02.b

### A. Comprendre
Annulation (RAM) ≠ `.blend1/.blend2` (copies écrasées) ≠ versions incrémentales
(historique). Auto-Save. Chemins relatifs. Copy on Duplicate. Startup file.
→ THEORY.md §5–6.

### B. Observer
Enregistrez trois fois de suite un fichier de test : regardez apparaître `.blend1` puis
`.blend2` dans l'explorateur.

### C. Reproduire
TUTORIAL.md — tutoriels 5 et 6. ✅ Audit `--strict` sans écart obligatoire.

### D. Pratiquer
- **Facile :** réglez Undo Steps, Save Versions, Auto-Save.
- **Moyen :** créez un fichier de démarrage personnel (cube supprimé, 1920×1080, 24 i/s),
  vérifiez avec *File → New → General*, puis restaurez l'original.
- **Difficile :** exercice 4.

### E. Produire
Fiche de poste section 5 complétée.

### F. Optimiser
`bcma_prefs_profile.py --apply --save` sur chaque nouveau poste ; ajoutez vos propres
réglages au tableau `PROFILE` du script (c'est du Python lisible, voir phase 13).

### G. Évaluer
Quiz Q11–Q15.

### H. Consolider
Voir la fiche [CHEAT_SHEETS/CH00_02_preferences.md](../../CHEAT_SHEETS/CH00_02_preferences.md).

### I. Livrables
Audit sans écart obligatoire, fiche de poste.
