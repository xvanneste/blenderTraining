# CH03.10 — Cours théorique : préparer un personnage au rig

## 1. Pourquoi une checklist
Un rig (CH-phase 6) est construit sur le maillage : os, poids, contraintes. Tout défaut du maillage (échelle, origine, orientation, asymétrie,
doublons) se paie ensuite à chaque animation. On livre donc un personnage « rig-ready » vérifiable.

## 2. La checklist (et ce que le correcteur mesure)
| Point | Exigence | Solution mesurée |
|---|---|---|
| Nom | objet `CHR_<Nom>_Body`, données `ME_…`, collection `CHR_<Nom>` | CHR_Hero_Body |
| Transformations | échelle 1, rotation 0, position 0 (appliquées) | (1, 1, 1) · 0° · (0, 0, 0) |
| Volume | un seul volume fermé | 1 morceau |
| Taille | 1,55–1,95 m | 1,76 m |
| Sol | pieds sur z = 0 (±1 cm) | 0,04 cm |
| Origine | entre les pieds | centre des pieds x = 0 |
| Orientation | face vers −Y | orteils vers −Y |
| Symétrie X | ≥ 97 % à 5 mm | 100 % |
| Pose | A (30–55°) ou T (80–100°), bras symétriques | A à 38° |
| Jambes | pieds écartés de 18–45 cm | 36 cm |
| Propreté | pas de sommets isolés ni de doublons | 0 / 0 |

## 3. Transformations et origine
- **Apply** : *Object > Apply > All Transforms* (ou Ctrl+A > All Transforms) intègre l'échelle, la rotation et la position dans les sommets.
  Un maillage modélisé en cm avec une échelle de 0,01 paraît juste à l'écran mais a des données fausses.
- **Rotation d'abord** : si le personnage est penché de 4°, remettez la rotation à 0 **avant** d'appliquer (sinon vous gelez l'erreur dans les sommets).
- **Origine** : *Object > Set Origin > Origin to 3D Cursor* avec le curseur 3D à l'origine du monde (Shift+C le recentre).

## 4. Poses de rig
- **Pose A** : bras à ≈ 30–55° de la verticale (ici 38°) : plus naturelle, moins de contorsion de l'épaule.
- **Pose T** : bras à 90° : simple à symétriser, convention de nombreux pipelines.
Dans les deux cas : jambes légèrement écartées (hanches), coudes et genoux très légèrement fléchis si le modèle est réaliste (ici non : mannequin).
Jamais les bras collés au corps : aisselles inaccessibles pour les poids.

## 5. Symétrie
Symétrisez le maillage (*Mesh > Symmetrize* en Edit Mode) ou travaillez en Mirror X. Mesuré : un bras décalé de 10 cm → 79 % ; le rig en miroir
produirait des poids faux.

## 6. Propreté
- Sommets isolés : *Select > Select All by Trait > Loose Geometry*.
- Doublons : *Mesh > Clean Up > Merge by Distance*.
- Volume fermé, normales vers l'extérieur (*Mesh > Normals > Recalculate Outside*).

## 7. Limites
Ce chapitre livre un **mannequin** simplifié : il n'a ni visage, ni mains, ni retopologie (CH03.06/07/09). Les mains avec leurs doigts, la tête
retopologisée, etc. s'assemblent dans le projet de fin de phase. Le correcteur ne juge ni la topologie ni la qualité d'anatomie.
