# CH07.03 — Cours théorique : Dope Sheet et Action

## 1. Le Dope Sheet
Une ligne par propriété animée (ou par objet) ; un losange par clé ; l'axe horizontal est le temps (images). On y déplace (G), met à l'échelle (S) et duplique les clés ; touche T : type d'interpolation (keymap par défaut). Les opérations de temps ne changent pas les valeurs.

## 2. Retimer
Pour faire durer l'action deux fois plus longtemps : curseur sur la première clé, sélectionner toutes les clés, S (×2). La mise à l'échelle part de l'image courante. Le starter a des clés à 1, 13, 25 ; après le retiming : 1, 25, 49 (valeurs 0, 2, 4 inchangées).

## 3. Décaler
G (déplacer) d'une quantité en images : décaler de 24 images la copie « Slide_Late » donne 25, 49, 73. Un décalage ne change ni les valeurs ni la durée.

## 4. Action, slot, utilisateurs
Une **action** est un bloc de données qui contient les courbes. Un **slot** (Blender 5.x) désigne les courbes de l'action qui s'appliquent à un objet : `animation_data.action` et `animation_data.action_slot`. Le compteur d'**utilisateurs** (`action.users`) indique combien d'objets la portent. Partager une action fait bouger deux objets de la même façon ; dupliquer l'action les rend indépendants.

## 5. Mesures
Solution : 33/33. A : X = 2 à l'image 25 et 4 à l'image 49. B : X = 0, 2, 4 aux images 25, 49, 73. « Slide » : 1 utilisateur. Contre-exemples : A non retimée (4,00 à l'image 25) ; pivot à 0 (clés à 2, 26, 50 : X = 1,88 à l'image 25) ; action partagée (2 utilisateurs) ; copie non décalée ; plage 1–49 ; valeurs inversées.

## 6. Pièges
- Mettre à l'échelle autour d'une image sans le savoir (le pivot est l'image courante).
- Décaler l'action partagée et croire décaler une copie.
- Oublier de renommer l'action dupliquée (« Slide.001 »).
- Oublier d'étendre la plage de la scène.
- Confondre déplacement des clés (G) et déplacement de l'objet.

## 7. Limites
Deux objets simples ; un seul canal ; l'éditeur d'actions et la gestion fine des slots (plusieurs slots par action) sont présentés mais non testés ; les menus du Dope Sheet n'ont pas été relus dans l'interface 5.3.
