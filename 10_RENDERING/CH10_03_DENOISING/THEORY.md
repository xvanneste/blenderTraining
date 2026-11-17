# CH10.03 — Cours théorique : Bruit et débruitage

## 1. Le bruit
Cycles tire des rayons au hasard : peu d'échantillons donnent un grain. Mesuré (160 × 90) : EQM 0,073 à 4 échantillons, 0,0235 à 16, 0,0053 à 128.

## 2. Le débruiteur
OpenImageDenoise (CPU) ; OptiX (carte NVIDIA, non testé ici). Panneau Sampling > Render > Denoise : Denoiser, Passes (RGB, Albedo, Albedo and Normal), Prefilter (None, Fast, Accurate), Quality.

## 3. Passes et préfiltre
Les passes Albedo et Normal guident le débruiteur sur les arêtes et les textures ; le préfiltre nettoie ces passes avant usage. Mesuré à 4 échantillons : sans débruitage 0,073 ; préfiltre None 0,071 ; Accurate 0,056. Dans cette scène, RGB seul (0,055) fait aussi bien : je n'ai pas mesuré d'avantage des passes ici.

## 4. Mesurer la perte
EQM avec une référence ; rapport de contraste du damier (0,85–1,15).

## 5. Le budget
Le rendu est limité à 1–8 échantillons : le débruitage compense. Au-delà (64 échantillons) c'est le coût qui augmente, pas la méthode.

## 6. L'exercice
Départ : 4 échantillons, débruitage off. Solution : OpenImageDenoise, Albedo and Normal, Accurate.

## 7. Pièges
- Débruiter un rendu à 1 échantillon (le débruiteur invente).
- Préfiltre None.
- Juger à l'œil sur une image de 160 × 90.
- Débruiter une animation image par image sans vérifier le scintillement.

## 8. Limites
Une scène, une graine, OIDN seulement ; pas d'animation ; pas de mesure de temps.
