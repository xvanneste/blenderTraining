# CH01.14 — Ressources

| Ressource | URL |
|---|---|
| Manuel — Render (introduction) | https://docs.blender.org/manual/en/latest/render/introduction.html |
| Manuel — Cycles Sampling | https://docs.blender.org/manual/en/latest/render/cycles/render_settings/sampling.html |
| Manuel — EEVEE | https://docs.blender.org/manual/en/latest/render/eevee/index.html |
| Manuel — Color Management | https://docs.blender.org/manual/en/latest/render/color_management.html |
| Manuel — Output Properties | https://docs.blender.org/manual/en/latest/render/output/properties/output.html |

Vérifications 5.3.0 : configuration OCIO livrée (`datafiles/colormanagement/config.ocio`) :
vues Standard, ACES 1.3, ACES 2.0, Khronos PBR Neutral, AgX, Filmic, Filmic Log, False Color,
Raw ; looks *AgX - Punchy*, *AgX - Medium High Contrast*, *AgX - Base Contrast*… ; menu *Render*
(*Render Image*, *Render Animation*) dans `space_topbar.py` ; propriétés Cycles de
débruitage. Rendus de référence produits par le script de construction et contrôlés à l'œil.
