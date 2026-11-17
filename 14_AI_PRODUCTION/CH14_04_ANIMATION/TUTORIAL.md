# Atelier guidé — IA pour l’animation

La marche fournie est animée dans Blender. Utilisez-la pour pratiquer le diagnostic des appuis. Si vous apportez un mouvement obtenu depuis une vidéo, joignez aussi les données de source, sa cadence, les noms d’os et les limites observées. Aucune comparaison de prestataires n’est nécessaire.

## 1. Référence de mouvement

Ouvrez la marche et repérez contact, appui et décollement sur un pied. Notez la cadence de la scène et les images de contact.

**Pourquoi** Un résultat vidéo-vers-animation doit être ramené à la cadence et aux unités de la scène cible.

**Contrôle** Un tableau par pied associe trois événements aux images de la timeline.

## 2. Retargeting et appuis

Dans une copie, dessinez la correspondance bassin, cuisse, tibia, pied d’une source et de la cible. Introduisez une dérive d’environ 5 cm sur un contrôleur de pied pendant l’appui.

**Pourquoi** Les axes locaux et la pose de repos influencent la reprise des rotations. Un pied planté doit rester stable en monde.

**Contrôle** Le glissement est visible en vue latérale et mesurable sur deux images de l’appui.

## 3. Nettoyer

Corrigez les clés du contrôleur pendant l’appui et adoucissez la sortie. Comparez la trajectoire du bassin et la flexion du genou avant et après.

**Pourquoi** Le verrouillage d’appui doit préserver le mouvement du corps et rester raccord avec le pas suivant.

**Contrôle** Le glissement baisse et le genou ne saute pas au raccord.

## Vérification sur une variante

Choisissez un contact de la marche fournie. Notez deux positions monde avant et après la correction du pied. Au raccord du pas, vérifiez la courbe du bassin et la flexion du genou. Faites le même test sur une autre cadence en convertissant d’abord le temps.
