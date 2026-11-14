# CH01.04 — Solutions

<!-- QUIZ_ANSWERS_START -->
## Réponses du quiz

| Q | Réponse | Explication |
|---|---|---|
| Q1 | **b** — Dans l'objet | La transformation appartient à l'objet ; la géométrie au maillage. |
| Q2 | — | Tout élément de données d'un .blend (objet, maillage, matériau, image, caméra…), avec un nom et un nombre d'utilisateurs. |
| Q3 | — | Il est supprimé (orphelin), sauf s'il a un Fake User. |
| Q4 | — | À donner un utilisateur fictif pour conserver une donnée non utilisée. |
| Q5 | — | Blender File. |
| Q6 | **b** — Alt+D | Alt+D partage les données. |
| Q7 | — | Tous les objets qui partagent ce maillage sont modifiés. |
| Q8 | — | Object Data : cliquer le nombre d'utilisateurs (Make Single User), ou Object > Relations > Make Single User. |
| Q9 | — | Shift+R. |
| Q10 | **b** — L'objet actif | L'objet actif garde son nom, son origine, ses modificateurs. |
| Q11 | **c** — By Loose Parts | By Loose Parts. |
| Q12 | — | Des collections ou le parentage. |
<!-- QUIZ_ANSWERS_END -->

## Exercice 2
À la réouverture, seul le matériau **utilisé** et celui avec **Fake User** existent ; le
troisième (0 utilisateur) a été supprimé à l'enregistrement.

## Exercice 3
Fichier : `COMPLETED_EXAMPLES/ch01_04_farm_solution.blend`. Séquence : `Alt+D` `X 1 Entrée`,
`Shift+R` ×6, renommer ; `GEO_Post_08` → Make Single User → Edit Mode → 4 sommets du haut
`G Z -0.4` ; sélection pieds + plateau actif → `Ctrl+J` → `F2` GEO_Table ; `GEO_Rocks` →
`Tab` `A` `P` *By Loose Parts* → renommer.

## Défi 2
Par défaut, le matériau est lié aux **données** (le maillage) : tous les piquets partageant
`ME_Post` changent. Dans l'onglet Material, le menu *Link* (Data/Object) permet de lier un
matériau à l'**objet** pour qu'un objet lié ait un matériau différent.
