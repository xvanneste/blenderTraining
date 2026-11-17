# CH08.09 — Cours théorique : Forces

## 1. Champs de force
Add > Force Field : Force, Wind, Vortex, Magnetic, Harmonic, Charge, Lennard-Jones, Texture, Curve Guide, Boid, Turbulence, Drag, Fluid Flow, Smoke Flow. Un champ est un objet (souvent un Empty) avec une propriété Strength.

## 2. Vent
Wind pousse selon l'axe local Z de l'objet : rotation de +90° autour de Y : vers +X (mesuré : x moyen +4,06 m à l'image 60 pour la force 5) ; −90° : −4,04 m.

## 3. Turbulence
Turbulence ajoute un champ de bruit : Strength et Size (la taille des tourbillons). Mesuré : écart-type en y 0,15 m sans, 0,48 m avec turbulence seule, 0,30 m avec le vent.

## 4. Field Weights
Chaque système de particules possède des poids par type de champ (gravity, wind, turbulence…). Un poids de 0 ignore ce champ (contre-exemple).

## 5. L'exercice
EMITTER : 300 particules (images 1–40, vie 80, Normal 2, gravité 20 %). FORCE_Wind : force 5, rotation Y +90°. FORCE_Turb : force 5, taille 0,5. Images 1–100.

## 6. Mesure
À l'image 60 : 300 vivantes ; x moyen 3,9 m (2,5–8) ; écart-type en y 0,30 m (≥ 0,25).

## 7. Pièges
- Vent sans rotation : il souffle vers −Z (par défaut) et les particules retombent.
- Poids du système à 0.
- Force trop faible face à l'impulsion initiale.

## 8. Limites
Pas de falloff ni de champs locaux ; pas d'effet sur le tissu (CH08.03) ni les corps rigides (CH08.01) ; un seul émetteur ; le correcteur ne lit que les positions moyennes.
