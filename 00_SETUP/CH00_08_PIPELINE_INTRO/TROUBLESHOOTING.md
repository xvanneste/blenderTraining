# CH00.08 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| « colonnes manquantes » | Séparateur virgule au lieu de point-virgule, ou en-tête modifié | Enregistrer en CSV « point-virgule » ; recopier l'en-tête du modèle |
| Accents illisibles (Ã©) | Fichier enregistré en ANSI | Enregistrer en UTF-8 (LibreOffice : jeu de caractères Unicode UTF-8) |
| Erreur de statut sur la dernière colonne alors qu'elle est correcte | Un point-virgule dans la description décale les colonnes | Remplacer `;` par `,` dans les descriptions |
| Excel transforme `sh0010` ou les durées | Conversion automatique | Importer via *Données → À partir d'un fichier texte* en type Texte, ou utiliser LibreOffice |
| Durée totale fausse | FPS différent | Option `--fps 25` (ou 30) si votre projet n'est pas à 24 i/s |
