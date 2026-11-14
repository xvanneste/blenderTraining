# CH01.13 — Cours théorique : éclairage élémentaire

## 1. Sans lumière, pas d'image
Une scène 3D sans lumière (et avec un monde noir) rend une image noire (CH00.01). L'éclairage
ne sert pas seulement à « voir » : il **sculpte** les formes, oriente le regard et installe
l'émotion. Les directeurs de la photographie disent qu'on « écrit avec la lumière ».

## 2. Les quatre types de lumières (+ le monde)
| Type | Comportement | Unité de puissance | Usage |
|---|---|---|---|
| **Point** | Rayonne dans toutes les directions depuis un point | watts (W) | ampoule nue, bougie |
| **Spot** | Cône de lumière (*Spot Size*, *Blend* = douceur du bord) | W | projecteur, lampe de poche, contre-jour |
| **Area** | Surface lumineuse (carré, rectangle, disque, ellipse) | W | **lumière de studio douce**, fenêtre, softbox |
| **Sun** | Rayons parallèles venant de l'infini ; seule l'orientation compte | *Strength* en W/m² (≈ 1–10) | soleil, lune |
| **World** | Lumière d'ambiance venant de toutes les directions | *Strength* | ciel, HDRI (CH09.03) |
Ajouter : `Shift+A → Light`. Réglages : *Object Data* (ampoule verte).

## 3. Les réglages qui comptent
- **Power / Strength** : intensité. Les lumières Point/Spot/Area suivent la **loi de
  l'inverse du carré** : à deux fois la distance, quatre fois moins de lumière. Rapprocher
  une lumière éclaire beaucoup plus fort.
- **Color** ou **Temperature** (nouveauté exploitée ici : case *Temperature* en kelvins ; la
  couleur devient alors une *Tint*) : 2 700 K bougie/ampoule chaude, 4 000–5 000 K
  soleil de fin de journée, 5 500–6 500 K lumière du jour, 7 000–10 000 K ciel bleu/ombre.
- **Exposure** : réglage d'intensité en « diaphragmes » (+1 = deux fois plus).
- **Radius** (Point/Spot) / **Size** (Area) / **Angle** (Sun) : taille de la source. **Grande
  source = ombres douces ; petite source = ombres dures.** C'est la règle la plus importante
  pour la qualité d'un éclairage.
- **Shadow** : ombres activées (presque toujours).

## 4. L'éclairage trois points
Le schéma de base de la photo de portrait et du cinéma :
```
                 RIM (contre-jour)
                    ●  derrière, en hauteur : détache la silhouette du fond
                    |
        FILL ●   [SUJET]   ● KEY
  (remplissage)     |       (principale)
  côté opposé,      |       devant, sur le côté (~45°), au-dessus des yeux :
  plus faible       |       donne la forme et la direction
                 CAMÉRA
```
| Lumière | Rôle | Position | Puissance relative |
|---|---|---|---|
| **Key** | Forme, direction, ambiance | 30–60° du côté caméra, au-dessus | 1 (référence) |
| **Fill** | Adoucit les ombres de la key | Côté opposé, plus bas | 1/2 à 1/8 (ratio 2:1 à 8:1) |
| **Rim / Back** | Contour lumineux, sépare du fond | Derrière, en hauteur | souvent forte |
Le **ratio key/fill** règle le drame : 2:1 doux et commercial, 4:1 naturel, 8:1 et plus
dramatique (film noir : fill presque absente).

## 5. EEVEE ou Cycles pour juger la lumière ?
Cycles calcule physiquement les rebonds de lumière ; EEVEE est temps réel (avec ray tracing
optionnel en 5.3). Pour régler un éclairage de base, le mode *Rendered* en EEVEE suffit ;
pour un rendu final réaliste, comparez avec Cycles (CH01.14, phase 10).

## 6. En production
Le *lighting artist* éclaire **par séquence** : un setup de lumières est réutilisé (lié) d'un
plan à l'autre, puis ajusté (*shot tweaks*). Les lumières sont nommées par rôle
(`LGT_Key_Window`, `LGT_Rim_Moon`) et rangées dans `LIGHTS` pour être activées/désactivées
facilement.
