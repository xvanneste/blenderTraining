# CH01.04 — Tutoriels pas à pas

## Tutoriel 1 — Voir les données
1. Ouvrez `STARTER_FILES/ch01_04_farm_starter.blend`, cliquez `GEO_Post_01`.
2. *Properties* → onglet **Object** (carré orange) : nom de l'**objet**.
3. Onglet **Object Data** (triangle vert) : nom du **maillage** `ME_Post`.
4. Outliner → menu *Display Mode* (en-tête) → **Blender File** : dépliez *Meshes*,
   *Materials*, *Objects*. Revenez en *View Layer*.

## Tutoriel 2 — La clôture en duplication liée
1. `GEO_Post_01` sélectionné, `Alt+D`, puis `X 1 Entrée` : un 2ᵉ piquet 1 m plus loin.
2. Avec la dernière copie toujours sélectionnée, faites six fois `Alt+D`, `X`, `1`, `Entrée`.
   La duplication crée le piquet et le déplacement le place à un mètre du précédent.
3. Object Data : à côté de `ME_Post`, le nombre **8**.
4. Renommez les copies `GEO_Post_02` … `GEO_Post_08` (`F2`) — Blender les a nommées
   `GEO_Post_01.001`…
5. Passez en Edit Mode sur un piquet (`Tab`), `A`, `S Z 1.1 Entrée` : **les 8** grandissent.
   `Ctrl+Z` pour annuler (en Edit Mode, annulez avant de ressortir).

## Tutoriel 3 — Rendre un piquet unique et le casser
1. Sélectionnez `GEO_Post_08`. Sous *Object Data*, cliquez sur le nombre **8** à côté du nom
   du maillage. Blender attribue une copie du maillage au piquet actif. Vérifiez que les
   autres piquets continuent d’utiliser `ME_Post` et que son compteur affiche **7**.
2. `Tab` (Edit Mode), mode sommets (`1`), sélectionnez les 4 sommets du haut (vue de face
   `Numpad 1`, `B` + rectangle autour du haut, avec *X-Ray* `Alt+Z` pour attraper ceux de
   derrière).
3. `G Z -0.4 Entrée`, `Tab`.
   ✅ Seul le piquet 8 est cassé.

## Tutoriel 4 — Joindre la table
1. Sélectionnez les 4 pieds puis, **en dernier**, `GEO_TableTop` (actif).
2. `Ctrl+J`. ✅ Un seul objet `GEO_TableTop` ; renommez-le `GEO_Table` (`F2`).

## Tutoriel 5 — Séparer les rochers
1. Sélectionnez `GEO_Rocks`, `Tab`, `A`.
2. `P` → **By Loose Parts**. `Tab`.
   ✅ Deux objets : `GEO_Rocks` et `GEO_Rocks.001`. Renommez-les `GEO_Rock_A`, `GEO_Rock_B`.

## Tutoriel 6 — Vérifier
Enregistrez `ch01_04_farm_<prenom>_v001.blend`, puis :
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.3\blender.exe" -b --factory-startup `
  "STARTER_FILES\ch01_04_farm_<prenom>_v001.blend" `
  --python-exit-code 1 --python "SCRIPTS\validate_ch01_04.py" -- --exercise farm
```
✅ 17/17.

## Contrôle de transfert

En mode Objet, modifiez la hauteur d’un piquet par son échelle. Seul ce piquet change. En mode Édition, modifiez ensuite sur une copie de travail le maillage d’un piquet lié et observez la propagation. Vérifiez le compteur d’utilisateurs avant de retoucher GEO_Post_08. **Réussite** Modifiez la forme du dernier piquet, gardez les autres formes et indiquez ce qui appartient à l’objet et au maillage.
