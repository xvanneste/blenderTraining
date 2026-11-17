# CH00.02 — Exercices

## Exercice 1 — Facile : appliquer le profil BCMA à la main ⏱ cible 10 min
1. Appliquez à la main (fenêtre Preferences) tous les réglages des tutoriels 3, 4 et 5.
2. Lancez l'audit (tutoriel 6) avec `--strict`.
**Réussi si :** code de retour 0, aucun `✘` dans le rapport.

## Exercice 2 — Consolider le cadrage avec et sans pavé numérique

1. Ouvrez la ville sur une copie. Cherchez l’aiguille en observant la scène, puis notez le point où elle devient difficile à repérer.
2. Revenez à la vue d’ensemble. Sélectionnez GEO_Needle par l’Outliner et utilisez **View → Frame Selected**.
3. Revenez à la vue d’ensemble et recommencez avec GEO_FarBeacon. Si vous disposez d’un pavé numérique, comparez le menu avec son raccourci.
4. Vérifiez que les objets n’ont pas changé de position et expliquez la différence entre cadrage de la vue et cadrage de la caméra.

**Réussi si** vous pouvez retrouver les deux objets sans déplacer leur géométrie et expliquer votre méthode à quelqu’un. Le chronomètre est facultatif. Des essais répétés sur le même objet entraînent aussi la mémoire de sa position.

## Exercice 3 — Difficile : cadrer l'aiguille (SANS procédure) ⏱ cible 10 min
Dans la ville, faites de `CAM_Needle` la caméra active et placez-la pour que l'aiguille
occupe **au moins 15 % de la hauteur de l'image**, entièrement dans le cadre. Enregistrez
sous `ch00_02_navigation_<prenom>_v001.blend`, puis :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch00_02_navigation_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch00_02.py" -- --exercise needle --render
```
**Barème (10 pts)** : objets présents 1 · caméra active 2 · distance < 3 m 2 · aiguille
dans le cadre 2 · gros plan 2 · rendu non noir 1. **Réussi si :** VALIDÉ.

## Exercice 4 — Difficile : la restauration (SANS procédure) ⏱ cible 10 min
Dans le profil de test, désactivez un réglage d’orbite et changez l’échelle de l’interface. Restaurez ensuite l’archive. Comparez les deux valeurs et vérifiez aussi le fichier de démarrage si votre archive en contenait un. Le profil recommandé par l’académie et votre sauvegarde personnelle peuvent avoir des valeurs différentes.

**Réussi si** les deux valeurs reviennent à leur état archivé après fermeture et relance. L’audit strict sert uniquement à vérifier le profil recommandé.

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
