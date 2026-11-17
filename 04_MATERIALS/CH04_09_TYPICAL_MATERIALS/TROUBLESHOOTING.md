# CH04.09 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Bois uniforme | Wave non reliée | Wave [Fac] → Color Ramp → Base Color |
| Veines trop fines ou rondes | Mapping non étiré | Scale (1 ; 1 ; 0,15) |
| Pierre lisse | Bump absent ou non relié | Texture → Bump [Height] → Normal |
| Acier trop parfait | Roughness constante, sans anisotropie | Anisotropic 0,6 + Noise étiré |
| Verre gris opaque | Transmission 0 | 1 |
| Matériau absent de l'Asset Browser | Non marqué ou dossier non déclaré | Mark as Asset ; Preferences > File Paths |
| Description vide | Métadonnées non remplies | Panneau d'asset : description |
| Plastique pâle | Environnement très clair | Régler l'éclairage ou la couleur |
