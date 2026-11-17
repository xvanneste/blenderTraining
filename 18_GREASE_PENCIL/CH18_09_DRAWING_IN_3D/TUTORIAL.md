# CH18.09 — Tutoriels pas à pas

Ouvrez `STARTER_FILES/ch18_09_set_starter.blend` : un sol, la caméra `CAM_Layout` (Y = −12,
focale 28 mm), une image de référence `REF_Concept` (à gauche), un objet `GP_Set` vide avec les
calques GROUND, BG, MID, FG.

## Tutoriel 1 — Préparer l'espace de dessin
1. Sélectionnez `GP_Set`, `Ctrl+Tab` → Draw Mode, `Num 0`.
2. Viewport Overlays → **Canvas** → cochez **Use Grid** (grille du plan de dessin).
3. En-tête : **Stroke Placement : 3D Cursor**.

## Tutoriel 2 — L'arrière-plan à 14 m
1. `N` → onglet **View** → **3D Cursor** → Location : X 0, Y **14**, Z 0.
2. **Drawing Plane : Front (X-Z)**. Calque **BG**.
3. En vue caméra, dessinez des montagnes **grandes** (elles sont loin). Au moins 4 traits.
4. Orbitez (molette) : les montagnes sont un « décor de théâtre » à 14 m.

## Tutoriel 3 — Plan moyen et premier plan
1. Curseur à Y = **3** ; calque **MID** : maison, arbres, personnage (au moins 4 traits).
2. Curseur à Y = **−5** ; calque **FG** : grand arbre sur un bord, buissons (au moins 4 traits).
   À 7 m de la caméra, dessinez petit : ces éléments couvrent vite l'écran.

## Tutoriel 4 — Le sol à plat
1. Curseur à Y = 0, **Z = 0** ; **Drawing Plane : Top (X-Y)** ; calque **GROUND**.
2. La grille du Canvas est maintenant couchée sur le sol. Dessinez une route de l'avant vers le
   fond (de Y ≈ −8 à Y ≈ +12), des touffes d'herbe. Au moins 3 traits.
3. Orbitez : la route est posée sur le sol ; vue caméra, elle fuit vers l'horizon toute seule.

## Tutoriel 5 — Finitions et vérification
1. Calques : décochez **Lights** (sous la liste des calques) pour des couleurs plates.
2. **Properties → View Layer → Passes → Data → Z**.
3. `F12` : comparez avec `COMPLETED_EXAMPLES/ch18_09_set_reference.png` ; la vue de dessus
   `ch18_09_set_top.png` montre les plans de dessin vus d'en haut (traits fins = plans verticaux).
4. Enregistrez `ch18_09_set_<prenom>_v001.blend`, puis :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch18_09_set_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch18_09.py" -- --exercise set --render
```

## Variante de contrôle

Contrôlez votre dessin dans une vue latérale en plus de la caméra. Déplacez un élément de fond en profondeur et comparez le recouvrement apparent. **Preuve** Le plan présente le même ordre de lecture et le placement en espace est explicite.
