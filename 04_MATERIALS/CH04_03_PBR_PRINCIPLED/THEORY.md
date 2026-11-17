# CH04.03 — Cours théorique : PBR et Principled BSDF

## 1. Le PBR en une page
*Physically Based Rendering* : on décrit un matériau avec des paramètres qui ont un sens physique, et la lumière fait le reste. Quatre idées :
1. **Métal ou non** : un métal n'a pas de couleur diffuse, il réfléchit en teintant ; un diélectrique (plastique, bois, peau, verre) a une couleur diffuse et un reflet blanc faible.
2. **Rugosité** : l'état de surface étale plus ou moins le reflet.
3. **Conservation de l'énergie** : un matériau ne renvoie jamais plus de lumière qu'il n'en reçoit ; d'où l'albedo borné.
4. **Environnement** : ce qu'on voit dans un reflet est le monde (World) ; sans environnement, pas de métal convaincant.

## 2. Les entrées du Principled BSDF (noms confirmés dans l'API 5.3)
Base Color · Metallic · Roughness · IOR · Alpha · Normal · Diffuse Roughness · **Subsurface** (Weight, Radius, Scale, IOR, Anisotropy) · Specular (IOR Level, Tint) · Anisotropic (+ Rotation, Tangent) · **Transmission Weight** (+ Dispersion Scale / Abbe Number) · **Coat** (Weight, Roughness, IOR, Tint, Normal) · **Sheen** (Weight, Roughness, Tint) · Emission (Color, Strength) · Thin Film (Thickness, IOR) · option Thin Wall.
Menus du nœud : *Distribution* (GGX, Multiscatter GGX) et *Subsurface Method* (Burley, Random Walk, Random Walk (Skin) ; une variante « Legacy » existe dans l'API).

## 3. Les quatre matériaux du chapitre
| Matériau | Metallic | Base Color | Roughness | Particularité |
|---|---|---|---|---|
| Or poli | 1 | (1,00 ; 0,77 ; 0,34) | 0,25 | IOR 1,45 |
| Caoutchouc | 0 | 0,05 (très sombre) | 0,75 | mat |
| Verre | 0 | blanc | 0,02 | Transmission 1, IOR 1,5 |
| Cire | 0 | (0,85 ; 0,70 ; 0,48) | 0,45 | Subsurface 0,6, rayon (1 ; 0,5 ; 0,25), Coat 0,2 |

## 4. Règles que le correcteur applique
- Metal : Metallic ≥ 0,9 ; luminance de Base Color ≥ 0,5 ; Roughness 0,05–0,6.
- Rubber : Metallic ≤ 0,05 ; albedo (luminance) 0,02–0,5 ; Roughness ≥ 0,55 ; pas de transmission.
- Glass : Metallic ≤ 0,05 ; Transmission ≥ 0,9 ; Roughness ≤ 0,1 ; IOR 1,3–1,7.
- Wax : Metallic ≤ 0,05 ; albedo 0,3–0,9 ; Subsurface Weight ≥ 0,2 avec rayon R > B ; Roughness 0,2–0,8.
- Général : quatre matériaux distincts ; aucun diélectrique à albedo > 0,9 ; Metallic jamais entre 0,1 et 0,9.

## 5. Pièges
- Metallic = 0,5 « pour un demi-métal » : physiquement faux ; mélangez deux matières avec un masque.
- Verre à Transmission 0 : opaque. Sur EEVEE, le verre épais peut exiger les réglages de réfraction du moteur (voir CH10).
- Cire sans Subsurface : rendu plastique.
- Albedo = 1 : blanc « brûlé ». Mesurer ≈ 0,8–0,9 pour du papier blanc.

## 6. Limites
Le correcteur contrôle des plages de valeurs plausibles, pas la beauté du rendu : on regarde toujours l'image. Il ne juge pas les matériaux à textures (CH04.04 et suivants).
