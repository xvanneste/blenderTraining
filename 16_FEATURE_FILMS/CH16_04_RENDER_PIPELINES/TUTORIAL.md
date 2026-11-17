# Atelier guidé — Pipelines de rendu

Lancez depuis les ressources `python controle_pipeline.py rendus`. Les deux images fournies sont un essai de pipeline, issu du présentoir, qui utilise le numéro de plan du pilote comme étiquette de suivi. Pour faire le rendu de l’exercice, relisez [CH13.05](../../13_PYTHON_AUTOMATION/CH13_05_BATCH_RENDER/README.md).

![Rendu de détail du présentoir de démonstration](../ASSETS_ATELIERS/RENDUS_TEST/v001/plan_0025.png)

## 1. Préparer le lot

Choisissez une version du plan, le moteur, la résolution et la sortie. Calculez les frames attendues du lot. Préparez un essai de deux images avant le lancement.

**Pourquoi** Un worker traite une plage dans un environnement identifié. Les images de coupe doivent rester distinctes des plages locales avec poignées.

**Contrôle** Chaque lot indique plage, version et chemin complet de sortie.

## 2. Distinguer retour et résultat

Produisez deux PNG avec le script du présentoir. Vérifiez en-tête, dimensions et identité du lot. Retirez une image dans une copie et faites relever le trou.

**Pourquoi** Un processus peut finir sans fournir toutes les images. La présence seule ne valide ni dimensions ni provenance.

**Contrôle** L’inventaire détecte l’image manquante par son numéro.

## 3. Reprendre et publier

Rejouez la plage manquante dans un dossier d’essai, puis publiez après QC. Tenez séparés v001 et v002 et consignez le numéro repris.

**Pourquoi** L’isolation des versions protège les images approuvées et permet un retour arrière.

**Contrôle** La nouvelle version contient toutes ses images attendues et l’ancienne reste consultable.

## Vérification sur une variante

Sur le lot de démonstration, fabriquez séparément une image manquante puis une taille erronée. Vérifiez la cause donnée par le contrôleur, puis refaites la publication depuis les bons produits.
