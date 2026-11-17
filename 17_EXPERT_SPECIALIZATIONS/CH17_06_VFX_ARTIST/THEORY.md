# Théorie — VFX Artist

## Isoler puis mettre en cache

Le cache découple les choix de vue du calcul. La taille du domaine et la résolution influencent coût et détail.

## Intégrer

Un bon effet partage la profondeur, l’éclairage et la perspective du plan. Un bon contour ne suffit pas.

## Versionner et livrer

Une livraison VFX doit être refaisable ou réutilisable. Les médias intermédiaires ont une version propre.

Pour une application directe, suivez le [tutoriel](TUTORIAL.md).

## Cas de production

La simulation produit une évolution. Le cache permet de la relire après redémarrage ou changement de caméra tant que les entrées du calcul restent compatibles. Le composite intègre l’effet à la lumière et à la profondeur du plan. Un halo peut venir du traitement de l’alpha et se vérifie sur plusieurs fonds.
