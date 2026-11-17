# CH08.10 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **a** — Pour la relire dans n'importe quel ordre | Sans cache, il faut rejouer depuis l'image 1. |
| Q2 | **a** — Enregistrer le fichier | Le dossier blendcache est créé à côté du .blend enregistré. |
| Q3 | **a** — blendcache_scene | `blendcache_<nom du fichier>`. |
| Q4 | — | En mémoire : rapide mais perdu à la fermeture selon les cas et pas de fichiers ; sur disque : fichiers .bphys (61 pour 60 images), gros caches et partage. |
| Q5 | — | Le cache est cherché dans `blendcache_<nouveau nom>` : s'il n'existe pas, il est perdu ; copier le dossier avec le fichier. |
| Q6 | **a** — Celle de la scène | Mesuré : scène 1–30 pendant la cuisson : 31 fichiers. |
| Q7 | **a** — Fichiers .bphys + relecture identique | Au moins 60 fichiers et positions identiques en sautant 60 → 40 → 60 → 40. |
| Q8 | — | Mesuré : après avoir changé Number à 150, `is_outdated` reste faux ; le correcteur compte donc les particules (150 au lieu de 100). |
| Q9 | — | Cache cuit (is_baked vrai) mais en mémoire : 0 fichier sur disque ; la consigne exige le disque. |
| Q10 | — | L'opérateur `ptcache.bake` exige un `point_cache` dans le contexte : `temp_override(point_cache=pc)`. |
<!-- QUIZ_ANSWERS_END -->

## Exercices
`COMPLETED_EXAMPLES/ch08_10_caches_solution.blend` (+ `_reference.png`)

**Fabrication.** Générées par script (`build_ch08_10_files.py`) : émetteur, cuisson réelle de chaque variante, dossiers blendcache. Score 33/33 ; starter 15/33. Courbe regardée.

## Contre-épreuve du correcteur (`COMPLETED_EXAMPLES/COUNTER_EXAMPLES/`)
| Fichier faux | Défaut | Tests qui le refusent |
|---|---|---|
| `…_no_bake` | rien n'est cuit | cuisson ; disque ; fichiers |
| `…_short_range` | scène 1–30 pendant la cuisson : 31 fichiers | fichiers (< 60) |
| `…_memory_only` | cuit en mémoire seulement (pas de Disk Cache) | disque ; fichiers |
| `…_outdated` | Number changé à 150 après la cuisson : 150 particules | nombre de particules |
Aussi refusé : le starter.

## Limites
- Seul le cache de particules est testé.
- `is_outdated` non fiable ici.
- Noms de boutons non relus.
