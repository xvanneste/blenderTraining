# CH07.14 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Le mouvement reste tremblé | Lissage insuffisant | Smooth (Gaussian) plus fort |
| Le mouvement est écrasé | Lissage trop fort | Réduire le facteur |
| Des pics subsistent | Glitches non supprimés | Supprimer les clés aberrantes avant de lisser |
| Trop de clés | Pas de décimation | Decimate (Allowed Change), Clean Keyframes |
| Les courbes sont anguleuses | Interpolation Linear | T > Bezier |
| La référence a disparu | MOCAP_RAW modifiée ou supprimée | Rouvrir le starter |
| L'import échoue | Chemin du BVH | Fichier voisin, chemin absolu |
| Le rig est couché ou inversé | Axes d'import | Forward −Z, Up Y |
