# CH03.06 — Cours théorique : le visage

## 1. Quatre zones, quatre structures
| Zone | Structure à sculpter | Piège fréquent |
|---|---|---|
| **Yeux** | globe dans l'orbite ; **paupière haute** recouvrant le haut de l'iris, paupière basse plus fine, pli au-dessus | yeux « ronds » : paupières absentes |
| **Nez** | arête, bout, **ailes**, deux **narines** (creux sous le bout) | narine percée de part en part |
| **Bouche** | **ligne** entre les lèvres, deux lèvres de volumes différents, **commissures** | ligne trop droite et trop courte |
| **Oreilles** | **hélix** (bord enroulé), **conque** (creux), lobe | pastille plate collée au crâne |

## 2. Repères moyens (à vérifier sur votre sujet)
- Largeur de bouche ≈ écart des pupilles (solution : ≈ 6,4 cm pour 6,4 cm d'écart).
- Oreille : de la ligne des sourcils environ jusqu'à la base du nez.
- Ligne des yeux à mi-hauteur de la tête (CH03.05).
Ce sont des moyennes artistiques : s'en écarter est un choix, pas une faute.

## 3. Ordre de travail
1. Bouche et paupières (elles fixent l'expression).
2. Nez : ailes et narines.
3. Oreilles.
4. Plis secondaires et grain (CH03.05) en dernier.

## 4. Les expressions de base
Une expression = quelques déplacements simples :
| Expression | Déplacements principaux |
|---|---|
| Neutre | commissures à la hauteur du centre de la bouche |
| **Sourire** | commissures **relevées**, plis naso-géniens plus marqués, joues qui remontent, yeux légèrement plissés |
| Moue | commissures abaissées |
Mesuré dans la solution : relèvement des commissures = **≈ 0 mm** (neutre), **+5,3 mm** (sourire), **−12,4 mm** (moue).
Les expressions se sculptent en **déformant** le visage neutre (Grab, Smooth) — c'est le principe des Shape Keys de la
phase 6 : un neutre propre d'abord, des variations ensuite.

## 5. Mesurer ce qu'on a sculpté : la référence cachée
Un détail de 2 mm sur une oreille ne se distingue pas de l'anatomie de base par une mesure « absolue » (essayé :
résidu d'un ajustement de surface, creux par rapport à une surface lissée — les deux échouent à séparer un visage
sculpté d'un visage non sculpté). Le fichier de départ embarque donc **REF_Base**, copie cachée du buste de départ.
Le correcteur mesure, pour chaque zone, l'**écart signé** de votre surface à REF_Base : creusé (négatif) ou relevé
(positif). C'est une mesure d'**avant/après**, la seule honnête à cette échelle.

## 6. Limites
Le correcteur vérifie que la structure existe avec le bon ordre de grandeur ; il ne juge pas la beauté. Un visage mal
dessiné mais creusé aux bons endroits passe ; la grille d'auto-évaluation corrige cela.
