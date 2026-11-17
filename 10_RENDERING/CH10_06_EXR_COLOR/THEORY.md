# CH10.06 — Cours théorique : EXR et couleur

## 1. Flottants
EXR stocke des flottants linéaires : 16 bits (demi-flottant, 11 bits de mantisse) ou 32 bits (24 bits). Près de 1000, le demi-flottant a un pas de 0,5 : mesuré 1000,5 pour 1000,7.

## 2. Pourquoi des valeurs > 1
Un soleil ou une lampe dans le cadre dépasse largement 1,0 ; le compositing et le flou de lumière ont besoin de ces valeurs.

## 3. Les codecs
Sans perte : ZIP, ZIPS, PIZ, RLE, NONE (mesuré 1000,700). Quasi sans perte pour 32 bits : PXR24 (0,003). Avec perte : DWAA, DWAB (mesuré 1001,5, erreur 0,8) ; à réserver à l'image finale.

## 4. Les passes de données
La passe Depth est écrite en 32 bits (mesuré) ; les couches de couleur suivent la profondeur choisie.

## 5. Multicouche
Output Properties > Output : type de média multicouche. Un seul fichier, une partie par calque (voir CH10.04). Le fichier se relit dans le compositeur ou une application externe.

## 6. L'exercice
Départ : monocouche, 16 bits, DWAA, pas de Z. Solution : multicouche, 32 bits, ZIP, passe Z.

## 7. Pièges
- 16 bits « par défaut » pour un master HDR.
- DWAA pour un fichier qu'on retravaillera.
- Changer de type de média sans revérifier la profondeur et le codec.
- Croire que l'espace colorimétrique est évalué ici (non).

## 8. Limites
Un pixel ; pas d'espace colorimétrique ; pas de taille de fichier ; le correcteur écrit un second fichier monocouche aux mêmes réglages pour relire les valeurs.
