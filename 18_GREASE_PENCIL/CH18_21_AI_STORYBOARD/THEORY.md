# CH18.21 — Cours théorique : l'IA au service du storyboard, sous contrôle

## 1. Principe : l'IA propose, vous décidez et vous vérifiez
Une IA peut accélérer certaines étapes du storyboard ; elle ne connaît ni votre intention, ni vos règles
de continuité, ni les droits attachés à ses sorties. Règle de ce chapitre : **toute proposition d'IA est
une hypothèse**, à contrôler avec les mêmes critères que votre propre travail (CH18.10 à CH18.20) —
et le contrôle doit être **traçable** (journal d'usage).

## 2. Où l'IA peut aider
| Étape | Aide possible | Risque principal | Contrôle |
|---|---|---|---|
| Références / moodboard | rechercher, classer, décrire des images | droits d'auteur, style d'un artiste imité | licence de chaque image, sources notées |
| Découpage / propositions de cadrage | liste de plans, valeurs, durées | faux raccords, axe franchi, durées incohérentes | règles 180°, codes, total (correcteur) |
| Model sheets assistées | variantes de poses/expressions | incohérence d'un dessin à l'autre (proportions, costume) | redessiner à partir d'une feuille de référence unique |
| Scripts de préparation | Python qui crée caméras, marqueurs, boards | code faux, destructif ou non testé | lire, tester sur une copie, correcteur |
| Continuité | repérer des incohérences dans un texte | faux positifs / oublis | vérification humaine + mesures |

## 3. Les erreurs typiques d'une proposition générée
L'exemple du chapitre contient les quatre erreurs les plus fréquentes :
1. **code de plan en double** (SH0030 deux fois) — casse le suivi de production ;
2. **franchissement d'axe** (un plan « de dos », caméra de l'autre côté de A–B) — faux raccord ;
3. **durée impossible** (0 s) ;
4. **total ≠ cible** (10,5 s au lieu de 12 s).
Une IA écrit avec assurance : la forme est propre, l'erreur est dans le fond. D'où l'intérêt de règles
**vérifiables automatiquement**.

## 4. Les scripts écrits avec une IA
`shot_prep.py` (ce chapitre) a été écrit avec une IA puis testé par un correcteur. Bonnes pratiques :
- **lire** tout le script avant de l'exécuter (que crée-t-il ? que supprime-t-il ? — ici : il supprime
  les caméras CAM_SH* existantes avant de les recréer) ;
- l'exécuter sur une **copie** du fichier ;
- vérifier le **résultat** par des mesures (valeurs de plans, images des marqueurs), pas par l'apparence ;
- ne jamais exécuter un script téléchargé sans l'avoir lu.

## 5. Droits, transparence, confidentialité
- Les conditions d'utilisation et les licences des outils d'IA **changent** : vérifiez-les à la date
  d'usage, pour chaque outil (la phase 14 détaille cette démarche).
- N'envoyez pas un projet non publié, ni des images dont vous n'avez pas les droits, à un service en
  ligne sans en accepter consciemment les conditions.
- N'imitez pas le style d'un artiste vivant identifiable.
- **Déclarez** l'usage de l'IA dans le journal du projet (outil, date, ce qui a été accepté, refusé,
  corrigé). Ce journal protège votre travail et permet de reproduire les décisions.

## 6. Ce qui reste votre métier
Intention, rythme, émotion, continuité, choix des cadrages, dessin final : l'IA peut proposer, mais la
**responsabilité** de la planche reste la vôtre. Le storyboard « assisté contrôlé » est validé par les
mêmes critères que les chapitres précédents.
