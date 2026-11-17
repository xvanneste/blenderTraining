# CH03.07 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| « Cinq doigts/orteils » : trop peu de pics | Doigts fusionnés (remesh, lissage) | Écartez-les (≥ 5 mm), Voxel Size < moitié de l'écart, moins de Smooth |
| Un doigt ou orteil flotte (2 morceaux) | N'est pas rattaché au corps | Faites chevaucher la base dans la paume / l'avant-pied ; relancez le remesh |
| Doigts « en chapelet » | Phalanges qui se touchent à peine | Chevauchement large (≈ 40 %), rayon qui diminue de 7 % |
| Pouce refusé (trop long/court) | Longueur ≠ 40–75 % du majeur | Il atteint à peu près la 1ʳᵉ articulation de l'index |
| Majeur pas le plus long | Doigts de même longueur | Majeur > annulaire ≈ index > auriculaire |
| Pied « plat » refusé | Pas de voûte | Le milieu du pied à ≥ 1 cm du sol |
| Semelle refusée (< 80 cm²) | Talon/balle coupés près de leur pôle | Patins plats centrés sur z = 0, puis Bisect à z = 0 |
| Talon trop large | Talon ≈ avant-pied | Talon 50–85 % de la balle |
| Cheville en œuf | Pas de coupe | Bisect à z = 0,14, Clear Outer + Fill |
| Volume « non fermé » | Coupe sans Fill | Fill ou Bisect avec Fill |
| Mauvaise orientation | Doigts vers −Y | Doigts/orteils vers +Y ; pouce / gros orteil vers +X |
| Rendu où l'on ne voit pas le guide | GP couché ou rotation en trop | Guide dans le plan XY (rotation −90° autour de X), vue Num 7 |
