# CH03.05 — Cours théorique : la sculpture réaliste

## 1. Réaliste = mesurable
Un buste réaliste n'est pas un buste « détaillé » : c'est un buste dont les **proportions** et les
**transitions** sont justes. Un front ridé sur une tête dont les yeux sont au tiers supérieur reste faux.
On vérifie donc d'abord les rapports, avec des chiffres (le correcteur de ce chapitre les mesure).

## 2. Les proportions de la tête (repères d'approximation)
| Repère | Valeur de référence | Mesuré dans la solution |
|---|---|---|
| Hauteur menton → couronne | ≈ 23 cm (adulte, de 21 à 24) | 23,1 cm |
| Largeur / hauteur de la tête | ≈ 0,60 – 0,75 | 0,63 |
| Ligne des yeux | à mi-hauteur de la tête | 55 % |
| Écart des centres des yeux | ≈ 6 – 6,5 cm (≈ un œil entre les deux) | 6,4 cm |
| Les trois tiers du visage | racine des cheveux → sourcils → base du nez → menton, à peu près égaux | — |
| Pointe du nez | au premier tiers du visage, depuis le menton | 33 % de la tête |
| Saillie du nez | ≈ 2,5 – 3,5 cm devant la joue | 3,4 cm |
Ce sont des **moyennes artistiques**, pas des lois : un visage réel s'en écarte. Ce qui compte : savoir
de combien on s'écarte, et le faire exprès. Erreur n° 1 des débutants : les yeux trop **hauts**.

## 3. Les plans de la tête
On sculpte un visage comme un volume taillé en **plans** : front, tempes, pommettes, plan du nez, plan de
la mâchoire, menton. Quelques grandes facettes d'abord ; les courbes viennent de la **transition** entre
elles. Vérifiez de **face, de profil et de trois-quarts** : une vue seule trompe.

## 4. Transitions
Des blocs juxtaposés (nez + arcade + pommette) se lisent comme des morceaux collés. Pour les fondre :
- **Smooth** (S, ou Shift maintenu pendant un trait) sur les raccords, jamais sur les grandes masses ;
- **Relax Slide**, **Flatten/Contrast** pour reposer des plans sans changer le volume ;
- un lissage **qui préserve le volume** : dans le volume scripté de la solution, un lissage de Taubin (λ/μ) fond les
  blocs sans faire rétrécir le buste — équivalent d'un Smooth appliqué à bon escient. Un lissage naïf
  (Laplacien seul) rapetisse et efface le nez.

## 5. Primaire, secondaire, tertiaire
| Niveau | Exemples sur un visage | Échelle | Comment |
|---|---|---|---|
| **Primaire** | crâne, nez, mâchoire, arcades, cou | > 3 cm | blocage, Grab, Clay Strips |
| **Secondaire** | plis naso-géniens, sillon entre les lèvres, poches sous les yeux | 0,5 – 3 cm | Draw Sharp, Crease Sharp, Crease Polish |
| **Tertiaire** | rides fines du front, pores, grain de peau | < 3 mm | brosse fine, Multires haut niveau ou Voxel plus fin |
**Ordre : primaire → secondaire → tertiaire.** Toute modification des masses déforme les plis ; le grain,
lui, ne se « déplace » pas avec la forme : on l'ajoute en dernier.

## 6. La densité fixe la finesse
Un détail ne peut pas être plus fin que le maillage. Avec un Voxel Size de 2,5 mm (le buste fait alors
≈ 74 000 faces) on peut creuser un sillon de 1–2 mm de large, pas un pore de 0,3 mm de large ; on peut en
revanche encoder le *grain* (une amplitude de 0,2 mm) comme variation de relief. Pour du détail plus fin :
Multires (*Subdivide* puis *Sculpt Level* supérieur) ou Voxel Remesh avec un Voxel Size plus petit (Ctrl+R
remaille ; R règle la taille du voxel). **Gardez une copie** avant chaque palier de densité.

## 7. Les yeux
Deux **globes** (sphères ≈ 2,5 cm) posés dans des orbites creusées : sans eux, un visage ne se juge pas.
Une orbite se creuse par Boolean Difference (une sphère de rayon légèrement supérieur) puis remesh. Ne pas
sculpter l'œil dans le maillage du buste : on le garde à part pour le rig (CH03.10 et phase 6).

## 8. Symétrie et vie
Travaillez avec Mirror X pour les proportions ; **cassez** légèrement la symétrie à la fin (un côté de la
bouche, un sourcil) : un visage parfaitement symétrique paraît faux. Le correcteur tolère donc des écarts
de 5 mm mais refuse une tête **décalée** (symétrie < 90 %).

## 9. Ce que ce chapitre ne couvre pas
Cheveux, peau (textures, sous-surface : phase 4/10), expressions (CH03.06), oreilles détaillées.
