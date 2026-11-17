# Atelier guidé — Technical Artist

Ouvrez l’espace Geometry Nodes. Montez une table de tests avec paramètres en colonnes et temps, géométrie, artefacts en sorties. La [référence P5](../../05_GEOMETRY_NODES/PROJECT_P5/README.md) donne un outil et son correcteur.

## 1. Contrat d’interface

Exposez densité, graine et collection source. Fixez un défaut utilisable et des valeurs limites. Testez la densité à zéro et maximale.

**Pourquoi** Une interface résiste aux valeurs limites et communique l’unité, la valeur par défaut et l’effet attendu.

**Contrôle** Un utilisateur peut relancer le même résultat sans ouvrir l’arbre.

## 2. Sondes visuelles

Construisez une entrée de shader de variation et comparez deux valeurs sur les mêmes instances. Gardez fixes cadrage et lumière.

**Pourquoi** Un test isolé renseigne sur la causalité. Un paramètre peut changer aspect ou géométrie, deux effets à mesurer séparément.

**Contrôle** Deux rendus et un graphe montrent la chaîne de données jusqu’au matériau.

## 3. Profilage et diffusion

Mesurez deux configurations, faible et forte densité. Rejouez chacune trois fois, rapportez médiane, compteur de géométrie et version Blender.

**Pourquoi** Les mesures d’échauffement diffèrent des suivantes. Un rapport reproductible donne méthode et conditions.

**Contrôle** L’outil a un budget défini, un cas limite documenté et un rapport de trois mesures par cas.

## Vérification sur une variante

Réalisez une grille de neuf cas avec trois densités et trois états de collection. Choisissez deux graines de contrôle et consignez celui qui doit rester stable après réouverture.
