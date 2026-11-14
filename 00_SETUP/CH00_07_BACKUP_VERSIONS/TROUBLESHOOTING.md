# CH00.07 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| *Recover → Auto Save* ne liste rien | Auto Save désactivé, ou Blender fermé « proprement » (les autosaves sont nettoyés) | Activer Auto Save (CH00.02) ; utiliser *Recover → Last Session* |
| Le travail en Sculpt/Edit Mode n'est pas dans l'autosave | Limite documentée de l'Auto Save | Repasser en Object Mode régulièrement ; `Ctrl+S` |
| `Ctrl+Alt+S` crée `fichier1.blend` au lieu de `_v002` | Le nom ne se termine pas par un nombre | Nommer d'emblée `…_v001.blend` |
| Pas de `.blend1` | *Save Versions* = 0, ou fichier enregistré une seule fois | Régler Save Versions ≥ 1 ; le `.blend1` apparaît au 2ᵉ enregistrement |
| Windows refuse de renommer `.blend1` en `.blend` | Extensions masquées | Explorateur → *Affichage → Afficher → Extensions de noms de fichiers* |
| `bcma_backup.py` : « source introuvable » | Chemin mal recopié / guillemets manquants | Mettre les chemins entre guillemets |
| Archive très lourde | Rendus inclus (`--include-renders`) ou caches | Laisser les exclusions par défaut |
| Import glTF sans textures | Export en `.gltf` séparé sans les images | Exporter en `.glb` (binaire, tout-en-un) |
