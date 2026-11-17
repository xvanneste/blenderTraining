# Dépannage — Rendu par lot

**Symptôme** Le rendu apparaît près du .blend au lieu du dossier demandé.

**Cause à vérifier** -o arrive après -f ou le chemin contient des espaces mal transmis.

**Correction** Passez les options de sortie avant -f et transmettez les arguments séparément.

Refaites le contrôle final. Le chemin invalide échoue et la reprise produit les deux fichiers dans un dossier séparé.
