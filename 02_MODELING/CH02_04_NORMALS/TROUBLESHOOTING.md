# CH02.04 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Taches noires, ombrage inversé par endroits | Faces retournées | Face Orientation ; `Shift+N` |
| Je ne trouve pas « Auto Smooth » dans Object Data | Supprimé depuis Blender 4.1 | *Object → Shade Auto Smooth* (modificateur Smooth by Angle) |
| Couvercles « gonflés » | Shade Smooth sans arêtes vives | Shade Auto Smooth (30°) ou Mark Sharp |
| Weighted Normal sans effet | Objet en Shade Flat | Shade Smooth d'abord |
| Taches restantes avec Weighted Normal | Weight trop bas, modificateur trop tôt dans la pile | Weight 75–100 ; mettre le modificateur en dernier |
| Normales personnalisées perdues | Géométrie modifiée après application | Garder Weighted Normal en modificateur (non appliqué) |
| Solidify épaissit vers l'intérieur | Normales retournées | Recalculate Outside, ou *Flip* dans Solidify |
| Recalculate échoue sur une partie | Maillage non-manifold, parties séparées | Réparer (CH02.01), sélectionner chaque partie (`L`) |
