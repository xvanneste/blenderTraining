# CH03.10 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| « Transformations appliquées » refusé | Échelle ≠ 1, rotation ≠ 0 ou position ≠ 0 | Rotation à 0 d'abord (Alt+R), puis Object > Apply > All Transforms |
| Après Apply, le personnage est toujours penché | Rotation gelée dans les sommets | Annulez ; remettez la rotation à 0 AVANT d'appliquer |
| Origine mal placée | Origine au centre du corps | Maillage pieds sur z = 0, centré ; curseur 3D en 0,0,0 ; Origin to 3D Cursor |
| Nom refusé | « .001 », espace, mauvaise forme | `CHR_Hero_Body` ; données `ME_CHR_Hero_Body` ; collection `CHR_Hero` |
| « Face vers −Y » refusé | Le personnage regarde +Y ou un côté | Rotation Z de 180° (ou 90°), puis appliquer |
| Taille hors 1,55–1,95 m | Maillage en cm / en mm | Appliquer l'échelle ; ou mettre à l'échelle de 1,76 m |
| Symétrie < 97 % | Un côté modifié, rotation non nulle | Mesh > Symmetrize, ou Mirror ; rotation à 0 |
| Pose non conforme | Bras le long du corps ou à un angle intermédiaire | A (30–55°) ou T (80–100°), les deux bras identiques à 6° près |
| Pieds écartés refusé | Jambes jointes ou trop ouvertes | Centre à centre 18–45 cm |
| « Volume fermé » refusé | Membres détachés, trous | Voxel Remesh, Fill, rattacher les membres |
| Doublons / sommets isolés | Join sans fusion, import | Merge by Distance ; Loose Geometry puis supprimer |
