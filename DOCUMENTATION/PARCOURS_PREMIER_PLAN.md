# Du premier rendu au premier plan animé

Choisissez un objet simple et gardez-le d'un jalon à l'autre. Une caisse qui glisse sous un projecteur suffit pour travailler la composition, le mouvement et le montage. Comptez **12 à 20 h de travail actif**, hors installation et temps de calcul. Ces durées sont des cibles à ajuster après les premières séances.

| Jalon | Temps indicatif | Livrable | À refaire sans le pas-à-pas |
|---|---:|---|---|
| Première image, dès la première séance | 1–2 h | Deux PNG de la même scène | Modifiez le cadrage de la caméra pour mieux montrer le sujet, puis exportez l'image. |
| Petite scène personnelle | 3–5 h | Un fichier Blender et une image avec trois objets simples | Changez de point de vue et déplacez une lumière. Vérifiez que le sujet reste lisible. |
| Premier mouvement | 3–5 h | Une scène qui montre un départ, une pause et un retour | Décalez la reprise du mouvement sans changer les positions de départ et d'arrivée. Vérifiez la pause en lecture. |
| Premier plan livré | 5–8 h | Un fichier Blender et un MP4 de 10 à 20 secondes | Exportez une version où l'action démarre plus tôt. Vérifiez le résultat dans un lecteur vidéo. |

## 1. Faire une première image

Installez Blender avec le [chapitre d'installation](../00_SETUP/CH00_01_INSTALLATION/README.md). Si Blender est déjà prêt, ouvrez directement la scène fournie dans le [chapitre du premier rendu](../01_FUNDAMENTALS/CH01_14_FIRST_RENDERS/TUTORIAL.md), enregistrez une copie, puis rendez et sauvegardez une image. Le [chapitre caméra](../01_FUNDAMENTALS/CH01_12_CAMERAS/TUTORIAL.md) montre comment changer le cadrage. Comparez vos deux PNG et choisissez celui qui montre le mieux le sujet.

## 2. Construire une petite scène

Dans une copie du fichier, placez trois formes simples sur le sol. Utilisez les [transformations](../01_FUNDAMENTALS/CH01_03_SELECTION_TRANSFORM/TUTORIAL.md), puis le [tutoriel d'éclairage](../01_FUNDAMENTALS/CH01_13_LIGHTING_BASICS/TUTORIAL.md). Rendez une image. Quand vous regardez la miniature, vous devez pouvoir désigner le sujet sans l'ouvrir en grand. La [nature morte P1](../01_FUNDAMENTALS/PROJECT_P1/README.md) permet d'approfondir cette étape avec un brief et une grille complète.

## 3. Animer un mouvement

Entraînez-vous sur la caisse du [chapitre des images clés](../07_ANIMATION/CH07_02_KEYFRAMES/TUTORIAL.md). Retrouvez les clés de position dans le Dope Sheet et décalez celle qui termine la pause. Rejouez l'animation depuis le début. Réutilisez le principe dans votre scène sur un objet visible par la caméra. Gardez la caméra fixe pour cette première version.

## 4. Exporter le plan

À 24 images par seconde, une plage de 1 à 240 donne 10 secondes. Répartissez la durée entre préparation, mouvement et pause. Testez d'abord quelques images et la lecture dans la vue caméra. Reprenez les réglages MP4/H.264 du [chapitre d'export](../12_EDITING_SOUND/CH12_06_EXPORT/TUTORIAL.md) en gardant votre plage de 240 images. Dans Output Properties, choisissez un chemin de sortie, par exemple `//renders/premier_plan_`. Lancez *Render → Render Animation*. Ouvrez le MP4 dans un lecteur et vérifiez sa durée, le cadrage ainsi que la lisibilité du départ et de l'arrêt.

Après chaque jalon, notez le fichier obtenu, ce que vous avez refait seul et le geste à réviser dans le [suivi](../PROGRESS.md#jalons-du-premier-plan).
