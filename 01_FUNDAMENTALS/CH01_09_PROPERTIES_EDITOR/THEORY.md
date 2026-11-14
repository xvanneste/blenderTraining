# CH01.09 — Cours théorique : l'éditeur Properties

## 1. Un classeur à onglets, du plus général au plus particulier
L'éditeur **Properties** affiche les réglages par **contexte**, dans une colonne d'onglets
(icônes verticales à gauche). L'ordre suit une logique : d'abord **la scène et le rendu**,
puis **l'objet actif**, puis **ses données**, puis **ses matériaux et textures**.

| Onglet (5.3) | Contenu | Enregistré dans |
|---|---|---|
| **Tool** | Réglages de l'outil actif | Fichier / préférences d'outil |
| **Render** | Moteur (EEVEE, Cycles, Workbench), échantillons, effets, gestion des couleurs | Scène |
| **Output** | Résolution, cadence (fps), plage d'images, format et dossier de sortie | Scène |
| **Scene** | Caméra active, unités, gravité, audio, propriétés personnalisées | Scène |
| **View Layer** | Passes de rendu, filtres (phase 10) | View layer |
| **Compositor & Effects** | Effets et compositing de scène (phases 10–11) | Scène |
| **World** | Fond, éclairage d'environnement | Monde |
| **Collection** | Réglages de la collection active (export, instanciation, Line Art…) | Collection |
| **Object** | Nom, transformations, relations, collections, visibilité, affichage, propriétés personnalisées | Objet |
| **Modifiers** | Pile de modificateurs (CH01.10) | Objet |
| **Particles / Physics** | Particules, simulations (phase 8) | Objet |
| **Constraints** | Contraintes d'objet (phase 6) | Objet |
| **Data** (icône selon le type : triangle vert, caméra, ampoule…) | Données de l'objet : maillage, caméra (focale), lumière (puissance)… | Données |
| **Material** | Emplacements et matériaux (CH01.11, phase 4) | Matériau |
| **Texture** | Textures des brosses et anciens systèmes | Texture |
Les onglets visibles **changent selon l'objet actif** (une caméra n'a ni matériau ni particules).

## 2. Lire un panneau
- Les panneaux se **replient** (clic sur le titre) ; `Ctrl`+clic replie tous les autres.
- Glisser la poignée `::::` d'un panneau change son ordre.
- Un champ numérique : clic = saisie ; glisser horizontalement = valeur ; `Ctrl` en glissant
  = pas réguliers ; `Shift` = précision ; `Backspace` au survol = valeur par défaut ;
  `Ctrl+C` / `Ctrl+V` au survol = copier/coller ; `RMB` = menu (Reset to Default, Copy to
  Selected, Copy Data Path, Insert Keyframe…).
- Un **losange** à droite d'un champ = animable (phase 7) : `I` au survol insère une clé.
- L'**épingle** en haut de l'éditeur fige l'affichage sur un datablock (utile pour comparer).

## 3. Datablock en en-tête de panneau
En haut des onglets Data, Material, World, une **ligne de datablock** : menu de choix, nom,
nombre d'utilisateurs, **bouclier** (Fake User), bouton de copie, `×` (délier). C'est là
qu'on rend unique, qu'on protège, qu'on échange un matériau contre un autre (CH01.04).

## 4. Propriétés personnalisées
*Object → Custom Properties* (et Scene, Data, Material…) → **New** : ajoute une donnée de
votre choix (nombre, texte, booléen, couleur…). Usages : métadonnées de plan (`shot`,
`artist`, `version`), paramètres de rig (phase 6), informations pour les scripts (phase 13).
Bouton ⚙ pour éditer le type, les bornes, l'infobulle.

## 5. Réglages de scène essentiels (préparation d'un plan)
- **Résolution** : 1920 × 1080 (Full HD), 3840 × 2160 (UHD) ; 1280 × 720 pour tester ; le
  pourcentage réduit sans changer le format.
- **Frame Rate** : 24 fps (cinéma), 25 fps (vidéo européenne), 30 fps (vidéo US/web).
  **À fixer avant d'animer** : le changer après déplace le timing de toutes les clés.
- **Frame Range** : la durée du plan, en images (CH00.08).
- **Unités** : système métrique, longueurs en m ou cm (affichage seulement : 1 unité Blender
  reste 1 m en interne avec Unit Scale = 1).

## 6. En production
La configuration d'un plan (résolution, fps, plage d'images, caméra, propriétés `shot`) est
générée par des **scripts de création de plan** à partir de la shot list — jamais saisie à la
main 200 fois. Vous écrirez ce script en phase 13 ; ce chapitre vous apprend où se trouve
chaque réglage qu'il manipulera.
