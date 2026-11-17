# Atelier guidé — Budget, planning et risques

Depuis les ressources, lancez `python controle_pipeline.py planning`. Reportez les champs debut, fin et parent en colonnes. Rejouez le calcul avec un scénario à capacité limitée sur une copie de la feuille.

## 1. Estimer la charge

Attribuez une unité cohérente à chaque poste. L’exemple utilise des jours ouvrés et une capacité dédiée par activité. Comparez charge et délai en tenant compte des activités parallèles.

**Pourquoi** Une charge s’additionne. Un délai dépend des liens entre activités et des ressources mobilisables.

**Contrôle** La feuille reproduit 24 jours-activité et 19 jours de délai théorique.

## 2. Trouver le chemin

Pour chaque tâche, calculez le début au plus tôt comme la plus grande fin parmi ses parents. Remontez depuis LIVRAISON jusqu’à l’origine.

**Pourquoi** Tout retard sur le chemin critique décale la livraison si les autres hypothèses restent identiques.

**Contrôle** Le chemin suit DEV, ANIMATIQUE, LAYOUT, ANIM, RENDU, LIVRAISON.

## 3. Réduire le risque

Ajoutez une panne de rendu de deux jours et un retard d’actif d’un jour. Chiffrez l’effet séparément. Prévoyez une réponse et un signal de déclenchement.

**Pourquoi** Un risque décrit occurrence, impact et action. Une réserve ne remplace pas le mécanisme de reprise.

**Contrôle** Le rendu retardé de 2 jours mène à 21 jours. Un jour de retard sur ASSETS ne décale pas le cas nominal.

## Vérification sur une variante

Rendez ASSETS et ANIMATIQUE incompatibles au même moment en supposant un auteur unique. Construisez l’ordre puis recalculez le début de LAYOUT. Indiquez la conséquence sur la livraison.
