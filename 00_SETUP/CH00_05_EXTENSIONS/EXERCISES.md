# CH00.05 — Exercices

## Exercice 1 — Facile : installer et utiliser BCMA Hello ⏱ 5 min
Installez `ASSETS/bcma_hello-1.0.0.zip` depuis le disque, utilisez le bouton sur la scène
par défaut, vérifiez les nouveaux noms dans l'Outliner, puis annulez (`Ctrl+Z`).
**Réussi si :** `GEO_Cube`, `CAM_Camera`, `LGT_Light` apparaissent.

## Exercice 2 — Moyen : audit d'une extension du catalogue ⏱ 15 min
Choisissez une extension sur https://extensions.blender.org (sans l'installer). Remplissez :
nom, auteur, licence, permissions déclarées, dernière mise à jour, versions de Blender
compatibles, nombre de téléchargements, avis. Verdict : l'installeriez-vous ? Pourquoi ?

## Exercice 3 — Difficile : « Mon Blender plante depuis que j'ai installé un truc » (SANS procédure) ⏱ 15 min
Rédigez la procédure complète pour identifier et retirer l'extension fautive sans perdre vos
autres réglages (indices : `--factory-startup`, rapport d'extensions, sauvegarde config,
désactivation une par une, dossier `extensions` du répertoire utilisateur).

## Défis
- **Défi 1 :** modifiez `bcma_hello` pour ajouter un second bouton qui **retire** les
  préfixes. Validez, construisez, testez avec `SCRIPTS/test_bcma_hello.py` adapté.
- **Défi 2 :** créez une extension de type **thème** (exportez votre thème, ajoutez un
  manifeste `type = "theme"`), validez-la.

## Mini-projet — Politique d'extensions ⏱ 15 min
Une page `PORTFOLIO/setup/extensions_policy.md` : sources autorisées, procédure
d'évaluation (licence, permissions, lecture), procédure de test, liste blanche actuelle.
Grille : sources 25 · évaluation 25 · test 25 · liste justifiée 25.
