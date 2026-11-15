# CH03.04 — Cours théorique : la sculpture stylisée

## 1. Styliser, c'est choisir
Un personnage stylisé n'est pas un personnage « simplifié par manque de temps » : c'est un
personnage dont chaque forme **sert une idée**. On part d'une intention (jovial, menaçant, timide…),
on choisit une **idée forte** de silhouette, puis on exagère ce qui la sert et on supprime le reste.

## 2. Le langage des formes
| Forme dominante | Lecture courante | Exemple |
|---|---|---|
| Cercle / courbe | doux, sympathique, jeune | tête ronde, joues pleines |
| Carré / bloc | stable, fort, têtu | mâchoire carrée, épaules massives |
| Triangle / pointe | dynamique, dangereux, rusé | menton pointu, épaules en V |
On combine : une forme dominante, une secondaire, une touche de la troisième.

## 3. Contrastes et rythme
- **Grand / moyen / petit** : trois tailles bien distinctes (tête énorme, cou fin, épaules moyennes).
  Évitez les tailles égales : elles s'annulent.
- **Droit / courbe** : un côté droit face à un côté courbe donne du rythme (dos droit, ventre rond).
- **Simple / détaillé** : concentrez le détail sur une zone (le visage) et laissez reposer l'œil ailleurs.
- **Proportions non humaines assumées** : grosse tête (≥ 40–50 % de la hauteur d'un buste), petits
  yeux très écartés, nez démesuré… L'exemple : tête = 75 % de la hauteur du buste, contraste
  tête/épaules ×1,46, nez saillant de 4,3 cm.

## 4. La silhouette d'abord
Une bonne figure stylisée se reconnaît **en ombre chinoise** (CH18.03) : vérifiez la silhouette de
face ET de profil (Num 1, Num 3) en mode d'affichage *Solid > Flat* avec une couleur unie, ou avec
un matériau noir sur fond blanc. Si la silhouette ne dit rien, aucun détail ne la sauvera.

## 5. Bloquer vite : primitives ou métaballes
- **Primitives qui se chevauchent** (ellipsoïdes, cylindres) puis *Join* + **Voxel Remesh**
  (CH03.03) : précis, prévisible, c'est la méthode de la solution.
- **Métaballes** (*Add > Metaball* : Ball, Capsule, Plane, Ellipsoid, Cube) : des volumes qui
  **fusionnent en douceur** quand ils sont proches ; un élément **Negative** (Object Data > *Active
  Element*) creuse (orbites, bouche). *Object > Convert > Mesh* les transforme en maillage. Plus
  organiques mais moins prévisibles : le rayon est un rayon d'**influence**, pas la taille visible ;
  réglez-les à l'œil dans la vue 3D.
- **Booléens** : creuser des orbites, découper un socle (Boolean *Difference*).

## 6. Le socle
Un buste se termine par une coupe nette : *Mesh > Bisect* au ras du bas (options *Clear Inner* et
*Fill*) ou un Boolean Difference avec un grand cube. Le volume reste fermé (impression 3D, rendu).

## 7. Après le blocage
Sculpt Mode : *Clay Strips* pour poser des plans francs, *Scrape/Fill* pour aplatir, *Pinch* pour
affirmer les arêtes, *Smooth* avec parcimonie (un style stylisé aime les plans nets). Gardez Mirror X ;
cassez la symétrie seulement à la fin, et volontairement (une mèche, un sourire en coin).
