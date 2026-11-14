# CH00.02 — Exercices

## Exercice 1 — Facile : appliquer le profil BCMA à la main ⏱ cible 10 min
1. Appliquez à la main (fenêtre Preferences) tous les réglages des tutoriels 3, 4 et 5.
2. Lancez l'audit (tutoriel 6) avec `--strict`.
**Réussi si :** code de retour 0, aucun `✘` dans le rapport.

## Exercice 2 — Moyen : mesurer le gain de navigation ⏱ cible 15 min
1. Lancez Blender avec les réglages d'usine : raccourci *blender_factory_startup.cmd* du
   dossier d'installation (ou `blender --factory-startup`).
2. Ouvrez la ville. Chronométrez-vous : trouver `GEO_Needle` **sans** l'Outliner, jusqu'à
   ce qu'elle occupe le quart de la vue. Notez le temps T1.
3. Relancez Blender normalement (vos préférences). Même exercice, toujours sans
   l'Outliner. Temps T2.
4. Troisième essai avec l'Outliner + `.`. Temps T3.
5. Notez T1, T2, T3 dans PROGRESS.md et écrivez en 2 phrases ce que vous en concluez.
**Réussi si :** trois temps notés, T3 < 15 s.

## Exercice 3 — Difficile : cadrer l'aiguille (SANS procédure) ⏱ cible 10 min
Dans la ville, faites de `CAM_Needle` la caméra active et placez-la pour que l'aiguille
occupe **au moins 15 % de la hauteur de l'image**, entièrement dans le cadre. Enregistrez
sous `ch00_02_navigation_<prenom>_v001.blend`, puis :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch00_02_navigation_<prenom>_v001.blend" `
  --python "SCRIPTS\validate_ch00_02.py" --python-exit-code 1 -- --exercise needle --render
```
**Barème (10 pts)** : objets présents 1 · caméra active 2 · distance < 3 m 2 · aiguille
dans le cadre 2 · gros plan 2 · rendu non noir 1. **Réussi si :** VALIDÉ.

## Exercice 4 — Difficile : la restauration (SANS procédure) ⏱ cible 10 min
Scénario : « J'ai tout cassé : thème illisible, plus d'orbite autour de la sélection, et
un fichier de démarrage rempli de cubes. » Remettez votre poste **exactement** dans l'état
de votre sauvegarde du tutoriel 1, sans réinstaller Blender.
**Réussi si :** l'audit `--strict` passe et *File → New → General* montre la scène
habituelle (cube, caméra, lumière).

## Défis avancés
- **Défi 1 :** ajoutez au script `bcma_prefs_profile.py` deux réglages de votre choix
  (ex. `view.show_splash = False`), avec explication. Vérifiez par l'audit.
- **Défi 2 :** créez un fichier de démarrage « production » : pas de cube, unités
  métriques, 1920×1080, 24 i/s, collections `SET`, `PROPS`, `CHARACTERS`, `LIGHTS`,
  `CAMERAS` vides. Documentez comment revenir au démarrage d'usine.
- **Défi 3 :** exportez votre thème et votre keymap (*Keymap → Export*), réimportez-les dans
  une copie portable de Blender (CH00.01 défi 1).

## Mini-projet — Profil de poste reproductible ⏱ 25 min
Livrez : (1) l'archive de configuration, (2) le rapport d'audit (copie du terminal dans
`PORTFOLIO/setup/prefs_audit.txt`), (3) la section 5 de la fiche de poste avec, pour
chaque réglage modifié, **pourquoi** vous l'avez modifié.

| Critère | Points |
|---|---|
| Audit sans écart obligatoire | 30 |
| Sauvegarde de configuration réelle et datée | 20 |
| Justification de chaque réglage | 30 |
| Procédure de restauration écrite et testée | 20 |

## Tests chronométrés (révision J+7, J+30)
| Test | Cible |
|---|---|
| T1 : retrouver et activer Orbit Around Selection + Zoom to Mouse Position | 45 s |
| T2 : trouver GEO_Needle via l'Outliner et la cadrer | 10 s |
| T3 : caméra active + Align Active Camera to View | 30 s |
| T4 : restaurer les préférences d'usine puis vos préférences sauvegardées | 3 min |

## Application cinématographique
En production, un plan peut contenir des milliers d'objets (une ville, une forêt). Les
layout artists et animateurs passent leur journée à naviguer : un réglage de navigation
qui fait gagner 2 secondes 500 fois par jour, c'est un quart d'heure par jour et par
personne. Les studios distribuent donc un profil de préférences commun.
