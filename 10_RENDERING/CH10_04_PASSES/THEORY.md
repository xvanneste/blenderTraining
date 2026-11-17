# CH10.04 — Cours théorique : Passes, AOV, View Layers

## 1. Les passes
View Layer Properties > Passes : Data (Z, Normal, Object Index…), Light (Diffuse, Glossy, Transmission : Direct, Indirect, Color), Cryptomatte (Object, Material, Asset), Light Groups, Shader AOV. Chaque passe devient des canaux EXR (Depth.Z, Normal.X/Y/Z, Diffuse Color.R/G/B…).

## 2. Les light groups
Dans le calque : Light Groups, ajouter « key », « fill ». Sur chaque lampe : Object Properties > Shading > Light Group. Canaux : Combined_key, Combined_fill.

## 3. Les AOV
Dans le calque : Shader AOV, type Color, nom « tint ». Dans le matériau : nœud Shader AOV Output avec le même nom. Canal : tint.R/G/B/A.

## 4. L'index d'objet
Object Properties > Relations > Pass Index (entier). La passe Object Index le restitue.

## 5. Les calques de vue
Un calque = une vue du décor avec ses collections exclues et ses passes. « FG » exclut Backdrop ; « BG » exclut Hero. Les canaux portent le préfixe du calque.

## 6. L'EXR multicouche
En 5.3, le type de média est **Multi-Layer EXR**. L’API lui donne la valeur `image_settings.media_type = 'MULTI_LAYER_IMAGE'`. Le fichier de l’exercice comporte une partie par calque et les noms des canaux figurent dans les en-têtes.

## 7. Pièges
- Oublier d'activer Cycles : plusieurs passes sont propres à Cycles.
- Un AOV défini dans le calque mais sans nœud dans le matériau : canal vide.
- Light group nommé dans la lampe mais absent du calque : pas de canal.
- Écrire du PNG : une seule image.

## 8. Limites
Pas de lecture des pixels de l'EXR ; Cryptomatte vérifié seulement par la présence de CryptoObject00 ; pas de Denoising Data ; EEVEE non traité.
