# CH10.03 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Image granuleuse | Débruitage off | Cocher Denoise |
| Détail flou | Trop peu d'échantillons | Au moins 4 |
| Aucun gain | Préfiltre None | Fast ou Accurate |
| Temps trop long | Beaucoup d'échantillons | Rester ≤ 8 et débruiter |
| OptiX indisponible | Pas de carte NVIDIA | OpenImageDenoise |
| Scène modifiée | Lampe changée | Light 60 W |
| Mesure instable | Graine différente | Le correcteur impose la graine 0 |
| Moteur refusé | EEVEE | Cycles |
