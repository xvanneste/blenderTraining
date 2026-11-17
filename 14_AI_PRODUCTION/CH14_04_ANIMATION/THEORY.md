# Théorie — IA pour l’animation

## Référence de mouvement

Un résultat vidéo-vers-animation doit être ramené à la cadence et aux unités de la scène cible.

## Retargeting et appuis

Les axes locaux et la pose de repos influencent la reprise des rotations. Un pied planté doit rester stable en monde.

## Nettoyer

Le verrouillage d’appui doit préserver le mouvement du corps et rester raccord avec le pas suivant.

Pour une application directe, suivez le [tutoriel](TUTORIAL.md).

## Cas de production

Le transfert d’une capture dépend de la cadence, de l’échelle et de l’orientation des chaînes. Exemple, une fermeture à 0,5 s apparaît douze images après le début d’un plan à 24 i/s. Pour un appui de pied, comparez une position dans le repère monde sur plusieurs images. Une position locale fixe peut quand même se déplacer avec son parent.
