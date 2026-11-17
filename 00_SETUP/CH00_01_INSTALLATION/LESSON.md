# CH00.01 — Leçons

Pour une première séance, installez Blender si nécessaire et ouvrez le [premier jalon](TUTORIAL.md#premier-jalon--rendre-et-conserver-une-image). Les leçons ci-dessous approfondissent la préparation d’un poste.

Chaque leçon suit le modèle **A. Comprendre → I. Livrables**. La théorie longue est dans
[THEORY.md](THEORY.md), les manipulations détaillées dans [TUTORIAL.md](TUTORIAL.md).

---

## Leçon 1 — L'écosystème Blender
**Niveau :** débutant · **Durée :** 20 min · **Prérequis :** aucun · **Compétence :** C00.01.a

### A. Comprendre
- **Ce que c'est :** Blender est une suite 3D libre et gratuite, développée par la Blender
  Foundation, qui couvre toute la chaîne de fabrication d'un film d'animation.
- **À quoi ça sert dans ce cursus :** c'est l'outil central. Les autres logiciels
  (DaVinci Resolve, Audacity, outils IA…) viendront s'y brancher.
- **Pourquoi c'est important de connaître sa licence et son cycle de versions :** pour
  distinguer la licence du logiciel des droits sur les œuvres et les ressources, et pour
  choisir **la bonne version au bon moment** (stable pour apprendre, LTS pour une
  production longue, jamais une daily build pour un vrai projet).
- **Analogie :** une version de Blender, c'est comme une édition d'un manuel scolaire.
  Les corrections (5.3.1, 5.3.2) corrigent des coquilles ; une nouvelle édition (5.4)
  réorganise des chapitres. On ne change pas d'édition au milieu de l'année.
→ Lire THEORY.md §1.

### B. Observer
Ouvrez https://www.blender.org/download/releases/ : chaque version a une page de notes.
Observez la structure : *Animation & Rigging, Cycles, EEVEE, Geometry Nodes, Modeling,
Python API, Sequencer…* Ces catégories correspondent presque une à une aux phases de
l'académie.

### C. Reproduire
1. Ouvrez la page des notes de version de **5.3**.
2. Repérez trois nouveautés et notez à quelle phase de l'académie chacune se rattache.
3. ✅ Vous avez noté 3 lignes du type « Vulkan par défaut → CH00.03 ».

### D. Pratiquer
- **Facile :** donnez la signification de chaque chiffre de `5.3.0`.
- **Moyen :** expliquez à un ami pourquoi un studio en pleine production refuse de passer
  à la dernière version.
- **Difficile :** un client vous demande si vous avez le droit de vendre un film fait avec
  Blender et des modèles téléchargés. Rédigez une réponse précise (pensez aux **deux**
  licences en jeu : celle du logiciel et celle des assets).

### E. Produire
Rédigez la première ligne de votre **fiche de poste** (`ASSETS/workstation_sheet_template.md`) :
version choisie et justification (stable ou LTS).

### F. Optimiser
- **Manuel :** consulter régulièrement blender.org.
- **Pro :** s'abonner au flux des annonces (Blender Developers Blog, notes de version) et
  planifier un test de chaque nouvelle version sur un projet jetable.
- **IA :** demander à un assistant de **résumer** les notes de version pour vos besoins
  (« quelles nouveautés de Blender 5.3 concernent l'animation de personnages ? ») —
  puis **vérifier** chaque point dans les notes officielles : un assistant peut se tromper
  ou confondre des versions.

### G. Évaluer
Quiz Q1 à Q5.

### H. Consolider
- Blender est libre et gratuit. Les ressources utilisées dans un projet ont leurs propres conditions.
- Stable ≈ tous les 3–4 mois · LTS = 2 ans de corrections · Daily = tests uniquement.
- On gèle la version d'un projet jusqu'à sa livraison.

### I. Livrables
Les 3 nouveautés notées + la réponse « difficile » (dans vos notes personnelles).

---

## Leçon 2 — Les méthodes d'installation sous Windows
**Niveau :** débutant · **Durée :** 25 min · **Prérequis :** L1 · **Compétence :** C00.01.b

### A. Comprendre
Cinq façons d'installer Blender sous Windows : **installeur .msi, zip, zip portable,
Microsoft Store, Steam**. Elles diffèrent par trois critères : besoin de droits
administrateur, intégration à Windows (menu Démarrer, double-clic sur un `.blend`),
contrôle des mises à jour. → THEORY.md §2 (tableau comparatif).

**Quand utiliser quoi ?**
| Situation | Choix |
|---|---|
| Votre poste principal | Installeur `.msi` |
| Tester la prochaine version sans toucher à la vôtre | Zip |
| Travailler sur plusieurs PC avec la même configuration | Zip + dossier `portable` sur disque externe |
| Projet de 6 mois qui ne doit pas bouger | Zip (ou installeur) d'une **LTS**, figé |
| Débutant qui ne veut jamais gérer de mise à jour | Microsoft Store |

### B. Observer
Sur le poste de référence, cinq versions cohabitent :
`C:\Program Files\Blender Foundation\Blender 3.6 / 4.4 / 5.0 / 5.2 / 5.3`. Chacune a été
installée par l'installeur, dans son propre dossier.

### C. Reproduire
Suivez **TUTORIAL.md — Tutoriel 1** (option A ou B).
✅ Blender 5.3 démarre et *Help → About* affiche 5.3.x.

### D. Pratiquer
- **Facile :** installez Blender 5.3 avec la méthode adaptée à votre poste.
- **Moyen :** installez une **deuxième copie** en zip dans un autre dossier, rendez-la
  portable (dossier `portable`), changez son thème : vérifiez que la copie installée
  n'a **pas** changé de thème.
- **Difficile :** vous êtes sur un PC sans droits administrateur et devez pouvoir
  double-cliquer sur un `.blend`. Trouvez comment (indice : THEORY.md §2, colonne
  « association »).

### E. Produire
Ajoutez à votre fiche de poste : méthode d'installation, dossier, justification.

### F. Optimiser
- **Manuel :** télécharger et décompresser à la main.
- **Pro :** garder un dossier `G:\Apps\Blender\` avec une copie zip de chaque version
  utilisée par vos projets (archivage : vous pourrez rouvrir un projet de 2026 en 2030
  avec **la même** version).
- **Automatisé :** `winget` (gestionnaire de paquets Windows) peut installer Blender
  (`winget search Blender` pour voir l'identifiant proposé) ; pratique pour réinstaller un
  poste, mais vérifiez toujours la version installée.

### G. Évaluer
Quiz Q6 à Q9.

### H. Consolider
- Installeur = intégré, admin requis · Zip = libre, sans admin · `portable` = config embarquée.
- Plusieurs versions cohabitent sans problème.
- Toujours télécharger depuis blender.org (ou Store/Steam officiels).

### I. Livrables
Blender 5.3 installé ; capture d'écran de *About Blender* dans `PORTFOLIO/setup/`.

---

## Leçon 3 — Plusieurs versions, préférences et dossiers
**Niveau :** débutant · **Durée :** 20 min · **Prérequis :** L2 · **Compétence :** C00.01.a

### A. Comprendre
Blender sépare le **programme** (dans *Program Files*) de **vos réglages** (dans
`%APPDATA%\Blender Foundation\Blender\<version>\`). Chaque version a son dossier de
réglages : c'est ce qui permet la cohabitation, et c'est pourquoi une nouvelle version
démarre « vierge » (avec la proposition d'importer les anciens réglages).
→ THEORY.md §3 (arborescence commentée).

Deux fichiers essentiels :
- `userpref.blend` — vos **préférences** (thème, raccourcis, GPU, add-ons…).
- `startup.blend` — votre **scène de démarrage** (ce qui s'affiche avec *File → New*).

### B. Observer
Dans l'explorateur Windows, tapez `%APPDATA%\Blender Foundation\Blender` dans la barre
d'adresse : un dossier par version que vous avez lancée.

### C. Reproduire
1. Ouvrez ce dossier, puis `5.3\config\`.
2. ✅ Vous voyez `userpref.blend` (après avoir changé au moins une préférence) et
   `recent-files.txt`.
3. Dans Blender : **File → Defaults → Load Factory Settings** remet tout à zéro *pour la
   session* (rien n'est écrasé tant que vous ne sauvegardez pas les préférences).

### D. Pratiquer
- **Facile :** retrouvez le dossier de réglages de 5.3.
- **Moyen :** faites une **sauvegarde** de ce dossier (copie zip datée) : c'est votre
  configuration de référence.
- **Difficile :** Blender plante au démarrage après l'installation d'une extension.
  Sans désinstaller Blender, trouvez **deux** façons de redémarrer sur une
  configuration saine (indices : un argument de ligne de commande ; un dossier à renommer).

### E. Produire
Fiche de poste : chemin du dossier de réglages + emplacement de votre sauvegarde.

### F. Optimiser
- **Pro :** versionner votre dossier `config\` et vos scripts dans un dépôt Git privé pour
  retrouver votre environnement sur n'importe quel poste.
- **Automatisé :** le script `bcma_system_report.py` affiche ces chemins
  (`bpy.utils.resource_path('USER')`).

### G. Évaluer
Quiz Q10 à Q12.

### H. Consolider
- Programme ≠ réglages. Un dossier de réglages par version.
- `--factory-startup` = démarrer sans vos réglages (diagnostic).
- Sauvegardez votre dossier de configuration.

### I. Livrables
Copie zip de votre dossier de configuration 5.3.

---

## Leçon 4 — Lancement, ligne de commande, GPU et benchmark
**Niveau :** débutant · **Durée :** 35 min · **Prérequis :** L3 · **Compétences :** C00.01.c, C00.01.d

### A. Comprendre
- Le **GPU** accélère énormément Cycles (×9 sur le poste de référence), mais il faut
  1) l'activer dans les **préférences** (*System → Cycles Render Devices*) et
  2) le choisir **dans chaque scène** (*Render → Device → GPU Compute*).
- La **ligne de commande** permet de lancer Blender sans interface : c'est la base des
  rendus de nuit, des render farms et de l'automatisation (phase 13).
→ THEORY.md §4 et §5.

### B. Observer
Rendu de la mire depuis PowerShell (TUTORIAL.md tutoriel 4) : observez dans le terminal
les étapes *Building OptiX acceleration structure*, puis *Saved: …cli_0001.png*.
Comparez ensuite les trois images de `COMPLETED_EXAMPLES/benchmark_reference/` : elles
sont **identiques à l'œil** — seul le temps change.

### C. Reproduire
Tutoriels 3 et 4 de TUTORIAL.md :
1. Activer le GPU dans les préférences. ✅ GPU coché.
2. Ouvrir la mire, passer en Cycles + GPU Compute. ✅ Device = GPU Compute.
3. `F12` pour rendre. ✅ La fenêtre de rendu affiche *Time* en haut ; notez-le.
4. Rendre la même image en ligne de commande. ✅ `cli_0001.png` existe.

### D. Pratiquer
- **Facile :** exercice 1 (EXERCISES.md).
- **Moyen :** exercice 2 (EXERCISES.md).
- **Difficile :** trouver, par la mesure, la meilleure combinaison pour **votre** machine
  (CPU seul ? GPU seul ? CUDA ou OptiX ?) — défi 2.

### E. Produire
Benchmark sur votre machine (tutoriel 5) et conclusion écrite dans la fiche de poste.

### F. Optimiser
| Méthode | Comment | Compromis |
|---|---|---|
| Pédagogique | `F12` et lire le temps | Simple, mais une seule mesure, pas de comparaison |
| Professionnelle | Ligne de commande `-b … -f 1 -- --cycles-device X` | Reproductible, scriptable |
| Automatisée | `bcma_render_benchmark.py` | Mesure tous les périphériques, avec chauffe GPU, rapport écrit |

### G. Évaluer
Quiz Q13 à Q17 · correcteur `validate_ch00_01.py --exercise testcard`.

### H. Consolider
- Préférences = **quel** GPU ; scène = **utiliser** le GPU.
- Premier rendu GPU plus lent (chargement des kernels).
- `-b` sans interface, `-f N` une image, `-a` animation, `--python-exit-code 1` pour l'automatisation.

### I. Livrables
`ch00_01_testcard_<prenom>_v001.blend` validé + `benchmark_<date>.md`.

---

## Leçon 5 — Rapport système et diagnostic
**Niveau :** débutant · **Durée :** 20 min · **Prérequis :** L4 · **Compétence :** C00.01.e

### A. Comprendre
Quand quelque chose ne marche pas, un technicien **ne devine pas** : il collecte les
faits. Le rapport système rassemble version, build, GPU, mémoire, chemins et réglages de
sauvegarde. C'est aussi ce qu'on vous demandera pour tout rapport de bug
(*Help → Report a Bug* pré-remplit d'ailleurs version et GPU).

Pour un **rendu noir ou vide**, la méthode « de la caméra vers la lumière » teste 5 suspects :
clipping caméra → visibilité au rendu (objets **et** collections) → lumières et monde →
résolution → caméra/image/sortie. → THEORY.md §6.

### B. Observer
Ouvrez `COMPLETED_EXAMPLES/system_report_reference/system_report_*.md` : lisez le
diagnostic (statuts OK / ATTENTION / INFO), puis les sections détaillées.

### C. Reproduire
Tutoriel 5 : générez votre propre rapport. ✅ Le diagnostic n'affiche aucun ATTENTION
(sinon, notez-le et consultez TROUBLESHOOTING.md).

### D. Pratiquer
- **Facile :** comparez votre rapport avec et sans `--factory-startup` ; listez les différences.
- **Moyen :** activez Auto Save dans vos préférences si le rapport le signale inactif ;
  régénérez le rapport.
- **Difficile :** **exercice 3** — réparez la scène cassée **sans lire la solution**.

### E. Produire
Mini-projet du chapitre : la **fiche de poste** complète (EXERCISES.md).

### F. Optimiser
- **Pro :** garder un rapport système daté par machine dans `DOCUMENTATION/` ; le
  regénérer après chaque mise à jour de pilote ou de Blender.
- **IA :** coller votre rapport dans un assistant en lui demandant d'expliquer un
  avertissement est utile ; **ne collez jamais** de chemins ou noms de machines
  confidentiels d'un studio dans un service en ligne sans autorisation.

### G. Évaluer
Quiz Q18 à Q20 · correcteur `validate_ch00_01.py --exercise broken --render`.

### H. Consolider
- Collecter les faits avant d'agir.
- 5 suspects du rendu noir, dans l'ordre caméra → lumière.
- Un rendu de contrôle petit et rapide (25 %, 8 échantillons) suffit pour diagnostiquer.

### I. Livrables
Rapport système + scène réparée validée + fiche de poste.
