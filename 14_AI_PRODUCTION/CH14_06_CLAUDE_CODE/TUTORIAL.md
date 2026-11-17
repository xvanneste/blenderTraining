# Atelier guidé — Claude Code et Blender

Le script local suffit pour faire les tests. Claude Code sert à proposer ou relire un correcteur. La connexion MCP est facultative, dépend du serveur que vous avez choisi et n’est pas requise par l’atelier. Relevez la version de votre CLI et les outils autorisés.

## 1. Spécifier

Donnez un brief local pour signaler les objets hors convention, sans renommer ni enregistrer la scène. Utilisez une copie du .blend et des noms fictifs.

**Pourquoi** Les entrées, sorties et refus attendus rendent le code proposé testable.

**Contrôle** Le brief fixe version Blender, périmètre de collection et format d’un message.

## 2. Inspecter

Lisez les appels bpy du script. Repérez les mutations, les chemins d’écriture et les imports. Refusez les accès dont ce contrôle local n’a pas besoin.

**Pourquoi** Un correcteur de lecture seule peut inspecter les datablocks sans appeler d’édition ni de réseau.

**Contrôle** Le diff répond au brief, et vous justifiez chaque API importante.

## 3. Tester

Exécutez en arrière-plan sur la référence puis sur une copie avec une anomalie. Notez résultat et code de retour. Refaites le test après la correction.

**Pourquoi** Un bon résultat sur un seul fichier ne montre pas que le défaut peut être détecté.

**Contrôle** Deux journaux permettent de comparer le cas nominal et le cas fautif.

## Vérification sur une variante

Relisez le script d’exemple, relevez les appels qui lisent la scène et faites échouer un test volontairement. Conservez la sortie Blender et le code de retour de deux exécutions. Les variantes MCP se vérifient seulement si le serveur choisi est disponible et autorisé.
