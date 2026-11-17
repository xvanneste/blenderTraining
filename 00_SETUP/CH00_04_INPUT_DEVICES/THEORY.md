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

Une souris avec molette cliquable permet de mobiliser les gestes par défaut. Si ce geste est inconfortable ou indisponible, le gizmo de navigation et le menu View proposent les mêmes objectifs.

## 2. Trackpad (ordinateur portable)
- *Input → Touchpad → Multi-touch Gestures* (activé par défaut) : deux doigts glissés =
  orbite, `Shift` + deux doigts = panoramique, pincer = zoom (selon le pilote du trackpad).
- *Scroll Direction* : *Traditional* ou *Natural*, selon votre habitude du système.
- Pour les gestes de souris manquants : *Input → Mouse → Emulate 3 Button Mouse*
  (`Alt` + clic gauche = bouton du milieu ; le modificateur peut être `Alt` ou la touche
  `OS` (Windows)).
- Les gestes disponibles varient avec le matériel, le pilote et le système. En cas de conflit avec Alt, choisissez un geste différent ou passez par le gizmo.

## 3. Clavier sans pavé numérique
Le pavé numérique donne les vues : `1` face, `3` droite, `7` dessus, `Ctrl` + chiffre =
vue opposée, `5` perspective/orthographique, `0` caméra, `2 4 6 8` rotation par crans,
`.` cadrer la sélection.
Sans pavé, plusieurs solutions :
1. **Emulate Numpad** (*Input → Keyboard*) : la rangée de chiffres devient le pavé.
   Inconvénient : en Edit Mode, `1/2/3` ne changent plus le mode de sélection.
2. **Le gizmo de navigation** (en haut à droite de la vue 3D) : cliquer sur un axe = vue
   correspondante ; glisser = orbite ; icônes main/loupe = panoramique/zoom.
3. **Le menu circulaire `` ` `` (accent grave)** — *View → Viewpoint* via un « pie menu »
   (sur un clavier AZERTY, la touche peut se trouver ailleurs : vérifiez dans
   *Preferences → Keymap*, recherche « View Pie »).
4. Un pavé numérique externe permet de retrouver les touches de la configuration par défaut.

## 4. Tablette graphique (stylet)
Utile pour la **sculpture** (phase 3), la **peinture de textures** (phase 4) et
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
règle la sensibilité et le mode (*Object*, *Fly*, *Drone*). Utile en modélisation et layout. Le parcours principal peut se suivre avec les commandes de la vue 3D.

## 6. Ergonomie (on parle de milliers d'heures)
- Écran à hauteur des yeux, avant-bras soutenus, pauses de 5 min toutes les 45 min.
- Alterner souris/tablette répartit l'effort.
- Les raccourcis réduisent les allers-retours souris → menus : c'est aussi de la santé.
