# CH00.02 — Dépannage

| Symptôme | Cause probable | Solution |
|---|---|---|
| Mes réglages disparaissent au redémarrage | *Auto-Save Preferences* décoché et pas de *Save Preferences* ; ou Blender lancé avec `--factory-startup` | Menu ☰ → cocher *Auto-Save Preferences* ou cliquer *Save Preferences* ; lancer Blender normalement |
| Après *Load Factory Settings*, les préférences ne sont plus sauvegardées | Comportement documenté : après un chargement d'usine, l'auto-save est suspendu | Menu ☰ → *Save Preferences* |
| `1`, `2`, `3` ne changent plus le mode de sélection en Edit Mode | *Emulate Numpad* actif | Utiliser les boutons sommets/arêtes/faces de l'en-tête, ou désactiver l'émulation si vous avez un pavé |
| L'orbite tourne autour d'un point bizarre | *Orbit Around Selection* actif avec une sélection lointaine ; ou *Auto Depth* sur un objet en arrière-plan | Sélectionner l'objet voulu / `.` pour cadrer ; ou désactiver *Auto Depth* |
| Le zoom « bloque » et n'avance plus | En mode zoom classique, on s'approche du point de pivot sans le dépasser | `.` sur l'objet visé, ou `Shift`+MMB pour déplacer la vue, ou la navigation Fly/Walk (*View → Navigation → Fly Navigation / Walk Navigation*) |
| Un objet lointain disparaît dans la vue 3D | *Clip End* de la vue (1000 m par défaut) | `N` → *View* → *Clip End* |
| Un petit objet vu de près est « tranché » | *Clip Start* trop grand | `N` → *View* → *Clip Start* = 0,001 m (sans exagérer : précision de profondeur) |
| L'interface est floue ou minuscule | Échelle Windows et Resolution Scale combinées | Ajuster *Interface → Display → Resolution Scale* |
| `bcma_prefs_profile.py` affiche « lancé avec --factory-startup » | Vous auditez les réglages d'usine | Relancer sans `--factory-startup` pour auditer **vos** réglages |
| File → New montre une scène inattendue | Fichier de démarrage personnalisé | *File → Defaults → Load Factory Settings* puis *Save Startup File* |
| Le correcteur dit « Aiguille dans le cadre » ✘ alors qu'on la voit dans la vue | Vous avez cadré la **vue**, pas la **caméra** | `Ctrl+Alt+Num 0` pour aligner la caméra active sur la vue, vérifier avec `Num 0` |
