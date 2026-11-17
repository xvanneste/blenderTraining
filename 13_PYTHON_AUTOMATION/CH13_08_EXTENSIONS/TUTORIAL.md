# Atelier guidé — Extensions Blender

Dans le dossier qui contient le manifeste et __init__.py, utilisez ces commandes PowerShell.

```powershell
$blender = "C:/Program Files/Blender Foundation/Blender 5.3/blender.exe"
& $blender --command extension validate
& $blender --command extension build
```

[Code de l’extension](../ASSETS_ATELIERS/__init__.py) · [Manuel Blender 5.3](https://docs.blender.org/manual/en/5.3/advanced/extensions/getting_started.html)

## 1. Préparer le paquet

Copiez uniquement le manifeste et __init__.py dans un dossier d’exercice. Vérifiez id, version, blender_version_min et licence.

**Pourquoi** L’identifiant stabilise l’installation. La version et la version minimale sont deux propriétés distinctes.

**Contrôle** Les deux fichiers sont à la racine du dossier de construction.

## 2. Valider puis construire

Depuis le dossier du paquet, lancez blender --command extension validate puis blender --command extension build.

**Pourquoi** La validation détecte les problèmes de manifeste avant l’installation.

**Contrôle** Blender crée bcma_reperes-1.0.0.zip et signale la construction.

## 3. Installer localement

Dans une session de test, utilisez Preferences → Get Extensions → Install from Disk. Activez l’extension, testez le bouton et désactivez-la.

**Pourquoi** Le scénario d’installation doit couvrir l’enregistrement et le retrait des classes.

**Contrôle** Le panneau est utilisable après activation et disparaît après désactivation.

## Vérification sur une variante

Construisez la version 1.0.1 avec un libellé changé. Comparez les deux manifestes, puis installez la nouvelle dans un profil d’essai. Activez le panneau, exécutez l’opérateur et désactivez l’extension, puis documentez le résultat.
