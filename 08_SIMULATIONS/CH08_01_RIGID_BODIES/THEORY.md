# CH08.01 — Cours théorique : Rigid Bodies

## 1. Actif et passif
**Active** : le corps tombe, rebondit, glisse (masse, friction, forme). **Passive** : obstacle fixe (le sol), éventuellement animé. Un objet sans corps rigide traverse tout.

## 2. Paramètres utiles
Masse (kg), friction (0 à 1), rebond (Bounciness), forme de collision (Box, Sphere, Convex Hull, Mesh), marge (Margin). Formes simples = simulation rapide et stable.

## 3. Marge
Chaque forme est épaissie d'une marge (0,04 m par défaut) ; sur des briques de 30 cm elle crée des chevauchements : marge à 0 (Margin cochée, valeur 0).

## 4. Animated
La case Animated (propriété `kinematic`) fait suivre au corps son animation au lieu de la physique. Cochée à l'image 1 puis décochée à l'image 21 (deux clés), la boule arrive de x = −6 à x = −1 puis est lâchée et continue sur sa lancée.

## 5. Le monde
Scene > Rigid Body World : cache de l'image 1 à 150 ; sous-étapes par image (10 par défaut) ; itérations du solveur. La simulation avance image après image depuis le début du cache.

## 6. L'exercice
Sol 60 × 60 m ; mur de 30 briques (6 rangs × 5, décalées) ; boule (cube de 0,8 m, 20 kg). Mesures de la solution : 47/47 ; déplacement avant impact 8 mm ; 21 briques déplacées de plus de 0,6 m ; z minimal 0,15 m ; boule avancée de 5,7 m ; mur au repos (5 mm entre les images 140 et 150).

## 7. Pièges
- Sol non rigide.
- Marge trop grande sur de petits objets (explosion au départ).
- Boule trop légère.
- Friction nulle (glissement sans fin).
- Cache trop court.
- Sauter à une image sans simuler depuis le début.

## 8. Limites
Un seul type de collision (boîtes), pas de contraintes (charnières) ni de destruction (CH08.07) ; le résultat de l'impact est déterministe mais sensible aux paramètres : les seuils du correcteur sont qualitatifs (10 briques déplacées, aucune sous le sol). Une colonne de cubes de 1 m glisse au lieu de s'effondrer : le mur de briques décalées est le cas retenu.
