# CH00.05 — Cours théorique : extensions et add-ons

## 1. Définitions
- **Add-on** : programme Python qui ajoute des fonctions à Blender (outils, panneaux,
  import/export). Certains sont **livrés avec Blender** (« cœur »).
- **Extension** : depuis Blender 4.2, format standardisé de distribution des add-ons **et
  des thèmes** : un `.zip` contenant un fichier `blender_manifest.toml` (identité, version,
  licence, permissions) et le code. Les extensions s'installent depuis des **dépôts**
  (*repositories*), le principal étant la plateforme officielle **extensions.blender.org**.
- **Dépôt** : source d'extensions. Par défaut : `extensions.blender.org` (en ligne),
  `User Default` (vos installations depuis le disque), `System` (déploiement par un
  administrateur).

**Analogie.** Blender est un smartphone ; les extensions sont les applications ;
extensions.blender.org est le magasin officiel, avec une vérification minimale.

## 2. Add-ons livrés avec Blender 5.3 (dossier `addons_core`)
| Add-on | Rôle | Phase |
|---|---|---|
| Node Wrangler | Raccourcis indispensables du Shader Editor | 4 |
| Rigify | Génération de rigs de personnages | 6 |
| Pose Library | Bibliothèque de poses (animation) | 7 |
| FBX, glTF 2.0 | Import/export vers d'autres logiciels et moteurs | 2, 16 |
| BVH | Import de motion capture | 7 |
| SVG (curves) | Import de dessins vectoriels | 2, 18 |
| UV Layout | Export d'image des UV | 4 |
| Hydra Storm | Moteur de rendu USD Hydra | 10 |
| VR Scene Inspection | Prévisualisation en réalité virtuelle | — |
| Manage UI translations | Outils de traduction de l'interface | — |
(OBJ, USD, Alembic, STL, PLY sont des formats intégrés au cœur, sans add-on.)
Beaucoup d'anciens add-ons « livrés » avant 4.2 sont désormais des extensions à
télécharger sur extensions.blender.org.

## 3. Sécurité : la règle d'or
Une extension est du **code Python exécuté avec vos droits** : elle peut lire et écrire
vos fichiers, accéder au réseau si elle le demande. Donc :
1. **Accès en ligne** : désactivé par défaut. Blender demande votre accord pour se
   connecter (*Preferences → System → Network → Allow Online Access*). Arguments :
   `--offline-mode` / `--online-mode` pour forcer.
2. Préférez **extensions.blender.org** ; ailleurs, uniquement des sources reconnues
   (dépôt du développeur, boutique connue). Jamais de version « crackée ».
3. Lisez la **licence** et les **permissions** déclarées dans le manifeste (`files`,
   `network`, `clipboard`, `camera`, `microphone`).
4. Ouvrez le `.zip` et **lisez** au moins la structure (et le code s'il est court) avant
   d'installer quelque chose d'inconnu.
5. Testez sur une **copie** de vos préférences (CH00.02) ou une installation portable.
6. Les **scripts intégrés dans un `.blend`** (drivers, Text Editor marqués *Register*) ne
   s'exécutent pas automatiquement sans votre accord : laissez *Auto Run Python Scripts*
   désactivé (*Preferences → Save & Load*) et n'autorisez que les fichiers de confiance.

## 4. Licences
- Les add-ons utilisant l'API Python de Blender doivent être **compatibles GPL** pour être
  distribués (une extension gratuite ou payante peut l'être).
- Les **thèmes** et assets peuvent avoir d'autres licences.
- Une extension payante reste sous GPL pour son code : vous pouvez l'utiliser pour des
  projets commerciaux ; respectez néanmoins les conditions du vendeur pour le support et
  les mises à jour.

## 5. Le manifeste (extrait commenté)
```toml
schema_version = "1.0.0"        # version du format de manifeste
id = "bcma_hello"                # identifiant unique (minuscules, _)
version = "1.0.0"                # version de l'extension (semver)
name = "BCMA Hello"
tagline = "Extension d'exemple…"
maintainer = "…"
type = "add-on"                  # ou "theme"
blender_version_min = "4.2.0"
license = ["SPDX:GPL-3.0-or-later"]
# [permissions] files = "…", network = "…"   ← à déclarer si nécessaire
```
Outils officiels en ligne de commande :
`blender -c extension validate <dossier>` (vérifie), `blender -c extension build`
(produit le `.zip`).

## 6. En production
- Le studio maintient une **liste blanche** d'extensions et leurs versions (reproductibilité).
- Les extensions sont déployées par un **dépôt System** ou un dépôt interne, pas installées
  individuellement.
- Toute mise à jour d'extension est testée avant d'être déployée (comme une version de Blender).
