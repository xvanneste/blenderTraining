# CH08.08 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Aucun cheveu | Type Emitter | Type Hair |
| Cheveux sous la tête | Pas de groupe de densité | Vertex Groups > Density |
| Peu de brins | Pas d'enfants | Children Interpolated |
| Pas de mèches | Clumping 0 | 0,5 |
| Cheveux figés | Hair Dynamics décoché | Cocher |
| Dynamique différente à chaque lecture | Lecture non séquentielle | Depuis l'image 1 |
| `use_hair_dynamics` introuvable | Propriété du système, pas des réglages | `ps.use_hair_dynamics` |
| Lenteur | Trop de parents | 300 parents, 10 enfants |
