# Atelier guidé — Rendu par lot

Exécutez depuis la racine du dépôt. La troisième valeur peut désigner un dossier d’essai absolu.

```powershell
python 13_PYTHON_AUTOMATION/ASSETS_ATELIERS/rendre_lot.py "C:/Program Files/Blender Foundation/Blender 5.3/blender.exe" 13_PYTHON_AUTOMATION/ASSETS_ATELIERS/presentoir_plans.blend ./rendus_ch1305
```

[Image 1](../ASSETS_ATELIERS/RENDUS/plan_0001.png) · [Image 25](../ASSETS_ATELIERS/RENDUS/plan_0025.png)

## 1. Commande unitaire

Lancez Blender avec -b, le .blend, -o dossier/plan_####, -F PNG et enfin -f 1. Vérifiez la sortie.

**Pourquoi** Les options sont traitées dans l’ordre. Une option placée après -f ne configure pas le rendu déjà lancé.

**Contrôle** plan_0001.png ouvre correctement depuis le dossier désigné.

## 2. Lot et chemins

Dans un dossier neuf, lancez rendre_lot.py avec l’exécutable Blender, la scène et le dossier de sortie.

**Pourquoi** Une liste d’arguments subprocess traite les chemins qui contiennent des espaces.

**Contrôle** Les PNG 0001 et 0025 sont produits et le programme revient sans erreur.

## 3. Panne et reprise

Donnez d’abord un chemin .blend inexistant. Observez le code de sortie, corrigez le chemin et relancez dans le dossier de test.

**Pourquoi** Un lot doit distinguer échec d’entrée, échec Blender et absence de produit attendu.

**Contrôle** Le chemin invalide échoue et la reprise produit les deux fichiers dans un dossier séparé.

## Vérification sur une variante

Créez un dossier d’essai avec un ancien plan_0001.png. Passez un chemin de scène inexistant au lanceur et vérifiez qu’il signale l’échec sans prendre l’ancien fichier comme preuve. Relancez sur la scène valide et rouvrez les deux PNG.
