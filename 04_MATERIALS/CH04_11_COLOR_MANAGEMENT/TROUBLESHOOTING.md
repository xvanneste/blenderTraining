# CH04.11 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Matériau trop brillant ou relief faux | Données en sRGB | Non-Color pour rugosité, métal, normales |
| Texture terne et sombre | Albedo en Non-Color | sRGB |
| Hautes lumières cramées | Vue Standard | AgX |
| Image délavée | Gamma ≠ 1 | Gamma 1 |
| Rendu trop clair/sombre | Exposure extrême | Régler la lumière ; Exposure ±1,5 |
| Bandes dans les dégradés | Sortie PNG 8 bits | EXR 16 bits pour le maître |
| Couleurs différentes dans un autre logiciel | Espaces différents | Documenter et aligner les réglages |
| Image noire après changement d'espace | Tampon réinitialisé (image générée) | Choisir l'espace avant de remplir |
