# CH00.01 — Exercices

Créez un dossier de travail et ouvrez les scènes fournies comme point de départ. Enregistrez chaque exercice sous un autre nom. [Conventions de nommage](../../DOCUMENTATION/CONVENTIONS.md).

---

## Exercice 1 — Facile : régler la mire pour Cycles (avec procédure) ⏱ cible 10 min
**Compétences :** C00.01.a, C00.01.c

1. Ouvrez `STARTER_FILES/ch00_01_testcard_starter.blend`.
2. Enregistrez-le immédiatement sous `ch00_01_testcard_<prenom>_v001.blend`
   (**File → Save As**, `Shift+Ctrl+S`).
3. *Properties → Render* : **Render Engine = Cycles**, **Device = CPU** pour le premier essai. Si vous avez validé un GPU compatible, essayez **GPU Compute** sur une copie.
4. *Render → Sampling → Render* : **Max Samples = 128**, **Denoise** coché.
5. *Properties → Output → Format* : **Resolution % = 100**.
6. Vérifiez que *Output* (le chemin) commence par `//`.
7. Enregistrez la scène, puis rendez avec F12. Depuis **Image → Save As**, enregistrez mire_v001.png en PNG et ouvrez-le dans un lecteur.
8. Lancez le correcteur (TUTORIAL.md, tutoriel 6) avec `--exercise testcard_cpu --render` sur CPU ou `--exercise testcard --render` sur GPU.

**Réussi si :** le correcteur affiche `RÉSULTAT : VALIDÉ`.

---

## Exercice 2 — Moyen : le même rendu, en ligne de commande, versionné ⏱ cible 15 min
**Compétences :** C00.01.c, C00.01.d

Sans procédure détaillée, à partir de votre fichier de l'exercice 1 :
1. Créez une **v002** du fichier avec *File → Save Incremental* (`Ctrl+Alt+S`).
2. Dans la v002, réglez Max Samples à 64.
3. Depuis PowerShell, rendez l’image 1 de la v002 en mode arrière-plan. Utilisez un préfixe ex2_cpu_. Si vous avez un GPU compatible, relancez avec le préfixe ex2_gpu_ et le périphérique correspondant.
4. Ouvrez chaque PNG. Confirmez même cadre, résolution et échantillons. Notez les mesures et calculez le rapport de temps uniquement si les deux périphériques ont rendu le même cas. Sur CPU seul, comparez plutôt 64 et 128 échantillons à taille identique, en nommant les deux sorties.

**Réussi si** chaque rendu demandé a un nom distinct et le fichier v002 passe le correcteur de sa configuration. Notez ce que le test mesure et les différences visibles.

---

## Exercice 3 — Difficile : « Le rendu est noir ! » (SANS procédure) ⏱ cible 20 min
**Compétence :** C00.01.e

Un collègue vous envoie `STARTER_FILES/ch00_01_broken_render_starter.blend` avec ce message :
> « Ma mire de test rend une image noire et minuscule. Je n'ai rien touché, je te jure. »

La scène contient **cinq** problèmes différents. Trouvez-les et réparez-les.
Règles :
- Ne lisez pas SOLUTIONS.md avant d'avoir terminé.
- Vous pouvez utiliser THEORY.md §6 (les 5 suspects).
- Enregistrez votre réparation sous `ch00_01_broken_render_<prenom>_v001.blend`.
- Validez avec : `--exercise broken --render`.

**Barème (12 pts) :** 2 pts par panne réparée + 2 pts si le rendu de contrôle n'est pas noir.
**Réussi si :** 12/12. Notez dans vos notes **dans quel ordre** vous avez trouvé les pannes
et **comment** (quel indice vous a mis sur la piste).

---

## Défis avancés (facultatifs)

### Défi 1 — Deux Blender, deux configurations
Installez une copie zip **portable** de Blender 5.3 sur un autre disque. Configurez-la
avec un thème clair et l'interface à 1,25× (*Preferences → Interface → Resolution Scale*).
Prouvez, captures à l'appui, que votre installation principale n'a pas changé, et
indiquez où chacune stocke ses préférences (le rapport système le dit : champ `user_config`).

### Défi 2 — La meilleure configuration de rendu pour VOTRE machine
Avec `bcma_render_benchmark.py`, mesurez :
- CPU seul, CUDA seul, OptiX seul (`--devices CPU,CUDA,OPTIX`) ;
- à 64 puis 256 échantillons (`--samples`) ;
- à 50 % puis 100 % (`--percent`).
Présentez un tableau, et répondez : l'accélération GPU est-elle constante ? Pourquoi ?

### Défi 3 — Script de rendu en un clic
Écrivez un fichier `render_testcard.ps1` qui rend la mire en GPU dans un dossier daté
(`renders\2026-11-14\…`). Indice : `Get-Date -Format yyyy-MM-dd`.

---

## Mini-projet — Fiche de poste « Studio prêt » (part 1/8 du projet P0) ⏱ 30 min
Complétez `ASSETS/workstation_sheet_template.md` (copiez-le dans
`PORTFOLIO/setup/workstation_sheet_<prenom>.md`) avec :
1. Matériel (depuis votre rapport système).
2. Version(s) de Blender installée(s), méthode, dossiers.
3. Résultats du benchmark et périphérique de rendu choisi, avec justification.
4. Emplacement de la sauvegarde de votre configuration.
5. Trois risques identifiés sur votre poste et la parade (ex. « 8 Go de VRAM → scènes
   lourdes en CPU ou optimisation des textures »).

### Grille d'évaluation du mini-projet (sur 100)
| Critère | Points |
|---|---|
| Fiche complète et exacte (cohérente avec le rapport système) | 30 |
| Benchmark réalisé et interprété correctement | 20 |
| Choix du périphérique justifié par des mesures | 15 |
| Sauvegarde de configuration effectivement faite | 15 |
| Trois risques pertinents avec parade | 20 |

Seuils : < 50 à refaire · 50–69 à consolider · 70–84 acquis · ≥ 85 maîtrisé.

---

## Tests chronométrés (à refaire en révision espacée J+7, J+30)
| Test | Temps cible | Critère |
|---|---|---|
| T1 : ouvrir la mire, régler Cycles CPU ou GPU, 128 échantillons, 100 %, enregistrer en v001 | **2 min** | Correcteur VALIDÉ |
| T2 : retrouver la version exacte de Blender par 2 méthodes | **1 min** | Les deux concordent |
| T3 : réparer la scène cassée (après l'avoir déjà faite une fois) | **5 min** | 12/12 |
| T4 : rendre l'image 1 d'un fichier en ligne de commande, de mémoire | **2 min** | Image produite |

## Application cinématographique
En production, la mire de test (*test card*, *lookdev scene*) est un vrai outil : on la
rend sur chaque nouvelle machine, chaque nouveau pilote, chaque nouvelle version de
Blender, et on compare l'image au rendu de référence. Une différence = un problème
détecté **avant** qu'il n'abîme mille plans. Gardez
`COMPLETED_EXAMPLES/ch00_01_testcard_reference_render.png` comme image de référence de votre
poste.
