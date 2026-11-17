# CH04.11 — Cours théorique : gestion des couleurs

## 1. Le principe
Blender calcule en **linéaire de scène** (`scene_linear`). Les images chargées sont converties vers cet espace selon leur **Color Space** ; le résultat est converti pour l'affichage par un **View Transform** et un **Display Device**. Trois étages : entrée (images), calcul (linéaire), sortie (vue + fichier).

## 2. Couleur ou donnée
| Image | Espace |
|---|---|
| Albedo, couleur d'émission | **sRGB** |
| Rugosité, métal, hauteur, masques | **Non-Color** |
| Normal map | **Non-Color** |
| HDRI (.hdr/.exr) | linéaire (souvent par défaut) |
Un mauvais espace ne donne aucune erreur : le rendu est simplement faux (relief inversé, matériau plus brillant que prévu).
Espaces proposés par Blender 5.3 (liste de l'API) : entre autres *sRGB*, *Non-Color*, *Linear Rec.709*, *ACEScg*, *Rec.2020*, *AgX Base sRGB*, *Filmic sRGB*, *Display P3* (une soixantaine au total).

## 3. View Transform (valeurs acceptées par l'API 5.3, vérifiées)
*Standard*, *Filmic*, *AgX* (valeur par défaut), *Khronos PBR Neutral*, *Raw*, *False Color*, *ACES 1.3*, *ACES 2.0*, *Filmic Log*.
- **AgX** : transform « tone-mapped » par défaut de Blender 5.3 ; conserve la teinte des hautes lumières.
- **Standard** : sRGB sans compression, les valeurs > 1 sont écrêtées.
- **Raw / Filmic Log / False Color** : outils de diagnostic ou de grade, pas des vues de livraison.
- **Looks** AgX : *None*, *AgX - Punchy*, *Base Contrast*, *High Contrast*, *Medium High Contrast*, *Very High Contrast*, *Low Contrast*, *Medium Low Contrast*, *Very Low Contrast*, *Greyscale*.
Mesure sur le panneau lumineux (Emission 4, couleur (1 ; 0,85 ; 0,6)) : Standard → (1 ; 1 ; 1) : teinte perdue ; AgX → (0,87 ; 0,85 ; 0,82) : valeur compressée, teinte conservée.

## 4. Exposition, gamma
**Exposure** décale la vue en diaphragmes : modérée (±1,5 ici). **Gamma** reste à 1 : le Display Device s'en charge.

## 5. Sortie maître
Format **OpenEXR** (linéaire scène, 16 ou 32 bits flottant) pour garder toute la dynamique ; livraison finale ensuite en PNG/vidéo par le pipeline (phases 10–12). Le rendu doit être **regardé** avec le même View Transform que la livraison.

## 6. Pièges
- Albedo en Non-Color : image terne et sombre ; rugosité/normales en sRGB : valeurs fausses.
- Vue Standard avec des lumières fortes : écrêtage.
- Gamma 2,2 : délavé. Exposition +4 : lumière mal réglée.
- PNG 8 bits comme maître : bandes et perte de hautes lumières.

## 7. Limites
Le correcteur contrôle les réglages de la scène, pas le jugement de l'image ; il n'évalue ni OCIO personnalisé, ni ACES complet, ni l'écran du poste.
