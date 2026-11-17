# Dépannage

| Symptôme | Vérification et correction |
|---|---|
| L’objet existe dans bpy.data mais reste absent de l’Outliner. | Vérifiez les deux liens, de la collection à la scène et de l’objet à la collection. |
| Des faces extérieures sont orientées à l’envers. | Vérifiez la connectivité et l’ordre des quads. Rejouez le recalcul dans BMesh et confirmez avec Face Orientation. |
| Le bloc flotte ou traverse le sol. | Vérifiez que son Z local minimal vaut 0 et que le Z de son objet vaut 0. |
| Le biseau est invisible dans la vue. | Activez l’icône d’écran du modificateur et vérifiez que la largeur est positive. Un rendu sous un éclairage rasant permet de juger le reflet. |
| Les couleurs sont correctes mais le reflet reste uniforme. | Passez en Material Preview puis remontez le fil de Roughness vers Result et de Value vers Fac. |
| COL_Presentoir existe déjà. | Enregistrez le texte séparément si nécessaire, puis recopiez-le sur une nouvelle copie du starter et relancez-le. |
| Un bloc est au mauvais endroit. | Affichez le nom et la position attendue. Dans la formule d’emplacement, l’indice de colonne règle X et l’indice de rangée règle Y. |
