# CH00.04 — Cours théorique : périphériques d'entrée

## 1. Pourquoi Blender insiste sur la souris à 3 boutons
Blender est conçu pour une main sur la souris, une main sur le clavier. Le **bouton du
milieu** (molette cliquable, `MMB`) pilote la navigation 3D :

| Geste | Action |
|---|---|
| `MMB` glissé | Orbiter |
| `Shift` + `MMB` glissé | Panoramique (déplacer la vue) |
| `Ctrl` + `MMB` glissé, ou molette | Zoom |
| `LMB` | Sélectionner, utiliser l'outil actif |
| `RMB` | Menu contextuel (avec la sélection au clic gauche) |

**Recommandation** : une souris filaire ou sans fil à 3 boutons (molette cliquable), avec
deux boutons latéraux si possible (assignables à des raccourcis via le logiciel du
fabricant). C'est l'investissement le plus rentable après l'écran.

## 2. Trackpad (ordinateur portable)
- *Input → Touchpad → Multi-touch Gestures* (activé par défaut) : deux doigts glissés =
  orbite, `Shift` + deux doigts = panoramique, pincer = zoom (selon le pilote du trackpad).
- *Scroll Direction* : *Traditional* ou *Natural*, selon votre habitude du système.
- Pour les gestes de souris manquants : *Input → Mouse → Emulate 3 Button Mouse*
  (`Alt` + clic gauche = bouton du milieu ; le modificateur peut être `Alt` ou la touche
  `OS` (Windows)).
- Limite honnête : on peut apprendre au trackpad, mais modéliser, animer ou sculpter
  plusieurs heures par jour sans souris ni tablette est pénible et lent.

## 3. Clavier sans pavé numérique
Le pavé numérique donne les vues : `1` face, `3` droite, `7` dessus, `Ctrl` + chiffre =
vue opposée, `5` perspective/orthographique, `0` caméra, `2 4 6 8` rotation par crans,
`.` cadrer la sélection.
Sans pavé, trois solutions :
1. **Emulate Numpad** (*Input → Keyboard*) : la rangée de chiffres devient le pavé.
   Inconvénient : en Edit Mode, `1/2/3` ne changent plus le mode de sélection.
2. **Le gizmo de navigation** (en haut à droite de la vue 3D) : cliquer sur un axe = vue
   correspondante ; glisser = orbite ; icônes main/loupe = panoramique/zoom.
3. **Le menu circulaire `` ` `` (accent grave)** — *View → Viewpoint* via un « pie menu »
   (sur un clavier AZERTY, la touche peut se trouver ailleurs : vérifiez dans
   *Preferences → Keymap*, recherche « View Pie »).
4. Un pavé numérique USB séparé (quelques euros) : la solution la plus confortable.

## 4. Tablette graphique (stylet)
Indispensable pour la **sculpture** (phase 3), la **peinture de textures** (phase 4) et
**Grease Pencil** (phase 18) : la **pression** du stylet module la taille et la force.
- *Input → Tablet → Tablet API* : *Automatic* (défaut), *Windows Ink* ou *Wintab*. Si la
  pression ne fonctionne pas, essayez l'autre API (et installez le pilote du fabricant).
- *Max Threshold* : pression maximale nécessaire pour atteindre 100 % (baisser si vous
  appuyez peu). *Softness* : courbe de réponse.
- Dans chaque brush, l'icône de pression (à côté de *Radius*/*Strength*) active la
  modulation par pression.
- Naviguer au stylet : les boutons latéraux du stylet peuvent être assignés au clic du
  milieu dans le pilote de la tablette.
- Une tablette d'entrée de gamme (sans écran) suffit largement pour débuter.

## 5. Souris 3D (NDOF)
Les souris 3D (type SpaceMouse) déplacent la vue sur 6 axes simultanément. *Input → NDOF*
règle la sensibilité et le mode (*Object*, *Fly*, *Drone*). Utile en modélisation et
layout ; facultatif et coûteux : à envisager plus tard.

## 6. Ergonomie (on parle de milliers d'heures)
- Écran à hauteur des yeux, avant-bras soutenus, pauses de 5 min toutes les 45 min.
- Alterner souris/tablette répartit l'effort.
- Les raccourcis réduisent les allers-retours souris → menus : c'est aussi de la santé.
