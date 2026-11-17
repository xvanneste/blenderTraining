# CH04.07 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Bake rend une image plate | Haute définition non sélectionné ou hors de portée | Sélectionner HIGH puis LOW (actif) ; Selected to Active ; augmenter l'Extrusion |
| « No active image texture » | Pas d'Image Texture actif | Cliquer le nœud Image Texture cible |
| Trous / traînées | Extrusion trop faible | Augmenter l'Extrusion (≥ 0,25 m ici) |
| Coutures sombres | Marge trop petite | Margin ≥ 8 px |
| Relief inversé ou faux | Espace sRGB ou Normal Map absent | Non-Color ; nœud Normal Map (Tangent) |
| Relief perdu à la réouverture | Image non empaquetée | Image > Pack |
| Silhouette trop lisse | Normal map ne change pas la silhouette | Augmenter les polygones ou utiliser du displacement (CH04.08) |
| Image noire après changement d'espace | Tampon réinitialisé | Régler l'espace avant de remplir ou baker |
