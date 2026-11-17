# CH03.08 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Le tissu traverse le corps | Collider masqué dans la vue (non évalué) ; Distance trop faible | Collider visible en affichage Wire ; Distance ≥ 3 mm |
| Le tissu tombe au sol, loin du corps | Il n'y a pas de collision sur le collider | Physics > Collision sur `COLLIDER` |
| Le tissu traverse le sol | Pas de Collision sur le sol | Physics > Collision sur `GEO_Floor` |
| Tissu dentelé, qui vibre | Self Collisions + pas d'amortissement | Décochez Self Collisions ; Damping 5 ; Quality Steps 12 |
| Tissu qui s'étire | Rigidités trop faibles | Tension / Compression 15 ou plus |
| Plis absents (plastique) | Bending trop fort, ou lissage | Bending 0,08 – 0,4 ; pas de Smooth massif |
| Tissu qui ne couvre pas les épaules | Trop petit, mal placé | Plus grand (≈ 0,54 m) ; au-dessus des épaules, centré |
| Tissu qui s'étale au sol en nappe | Trop grand | Réduire, ou raccourcir |
| Correcteur : « modificateur Cloth APPLIQUÉ » refusé | Simulation non appliquée | À l'image de repos : Ctrl+A sur le modificateur |
| Le fichier relu ne contient plus la simulation | Cache non appliqué | Appliquer le modificateur (le cache n'est pas le maillage) |
| Simulation très lente | Collider trop dense, Quality trop haute | Decimate du collider ; baisser Quality Steps pendant les essais |
