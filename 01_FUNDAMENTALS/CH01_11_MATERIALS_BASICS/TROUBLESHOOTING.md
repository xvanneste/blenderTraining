# CH01.11 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Les couleurs ne s'affichent pas | Mode Solid | `Z` → Material Preview ou Rendered |
| Le bouton Assign est absent | Object Mode | `Tab` (Edit Mode) |
| Toute la maison est devenue rouge | Couleur modifiée dans le matériau de l'emplacement 0 au lieu du nouveau | Sélectionner le bon emplacement avant de régler |
| Changer un matériau change d'autres objets | Matériau partagé | Copie (bouton de la ligne de datablock) |
| La lanterne ne brille pas | Emission Strength à 0, ou mode Solid | Strength 5–10, mode Rendered |
| Le métal paraît noir | Metallic 1 dans une scène sans rien à refléter (monde noir) | Material Preview (HDRI) ; en rendu, éclairer l'environnement (phase 9) |
| Le verre est noir en EEVEE | Réglages de transparence/ray tracing EEVEE | Tester en Cycles ; EEVEE en phase 10 |
| Taches roses/magenta | Texture introuvable (CH00.06) | *File → External Data → Find Missing Files* |
