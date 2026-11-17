# CH12.03 — Cours théorique : Son

## 1. Les trois familles
Ambiance (continue), bruitages (ponctuels, synchrones), voix (réplique calée). Plus la musique (CH12.04).

## 2. Synchroniser
Placer le début du strip sur l'image de l'action (marqueur de timeline) : ± 2 images pour un bruitage, ± 3 pour une voix.

## 3. L'ambiance
Elle doit couvrir toute la séquence ; sinon un silence trahit le montage.

## 4. Le niveau
Un bruitage domine l'ambiance (rapport 12 ici) ; une réplique aussi.

## 5. Le mixage
`bpy.ops.sound.mixdown` écrit un WAV ; le correcteur mesure le RMS par fenêtre.

## 6. L'écrêtage
Crête ≤ 0,98 : au-delà, distorsion numérique.

## 7. Pièges
- Son décalé d'une dizaine d'images.
- Ambiance trop courte.
- Strip muet.
- Volume trop fort qui écrête.

## 8. Limites
Sons synthétiques ; pas de musique ni de panoramique (CH12.04) ; les menus d'ajout de son (Add > Sound) n'ont pas été regardés.
