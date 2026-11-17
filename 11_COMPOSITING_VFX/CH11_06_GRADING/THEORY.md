# CH11.06 — Cours théorique : Color grading

## 1. Trois zones
Lift : ombres ; Gamma : tons moyens ; Gain : hautes lumières. Type « Lift/Gamma/Gain » du nœud Color Balance.

## 2. Teinter
Une couleur légèrement bleue sur Lift teinte les ombres ; une couleur légèrement orange sur Gain teinte les hautes lumières.

## 3. Dans le nœud 5.3
Prises : Lift (facteur et couleur), Gamma, Gain, Offset, Power, Slope, Temperature, Tint. Les prises de couleur de Lift, Gamma, Gain sont les 4e, 6e et 8e prises.

## 4. L'exposition
Gamma modifie les tons moyens, Gain les hautes lumières : un Gain neutre trop fort ou un Gamma trop haut change la luminosité (+0,125 mesuré avec Gamma 2).

## 5. L'exercice
Départ : neutre. Solution : Lift bleu léger, Gain orange léger.

## 6. Mesurer
Moyenne RGB de deux bandes de colonnes ; luminance moyenne contre la même image avec le compositing désactivé.

## 7. Pièges
- Valeurs trop fortes : image artificielle, hautes lumières écrêtées.
- Teinter aussi les ombres en chaud (all_warm).
- Changer la luminosité en croyant changer la teinte.

## 8. Limites
Rampe de gris ; pas de courbes ni de LUT ; goût non mesuré.
