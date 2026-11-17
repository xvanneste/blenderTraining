# CH05.03 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Aucune instance | Sortie Instances non reliée | Instances → Group Output |
| Piquets enfoncés | Cylinder centré, pas relevé | Transform z = 0,5 |
| Tous identiques | Random Value non reliés | → Rotation et Scale |
| Rotation sans effet | Random de type Float | Type Vector pour la rotation |
| Fichier lourd | Realize Instances | Garder les instances |
| Pas de matériau | Set Material manquant | L'ajouter avant l'instanciation |
| Grille trop dense | Vertices trop grands | 21 × 21 |
| Instances alignées | Seed identique / pas d'aléa | Random Value avec Seed différent |
