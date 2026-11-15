# CH02.09 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Zones du rocher non couvertes | Cage trop petite avant Shrinkwrap | Mettre la cage à l'échelle pour envelopper la forme |
| Les sommets s'aimantent à la cage elle-même | *Include Active* coché | Snapping → Target Selection → décocher Include Active |
| Les sommets ne collent pas à la surface | Snap désactivé ou mauvais élément | `Shift+Tab` ; Snap Target for Individual Elements : Face Project |
| Cage invisible, cachée dans la sculpture | Cage sous la surface | Overlay Retopology ; Shrinkwrap Offset 0,005 |
| Je modifie la sculpture par erreur | Sculpture sélectionnable | Outliner : désactiver la sélection ; ou la verrouiller |
| Poly Build crée des triangles | `Ctrl+clic` près d'un seul sommet | Créer des faces entre 4 sommets ; vérifier *Faces by Sides* |
| Cage plissée dans les creux | Nearest Surface Point sur une forme concave | Wrap Method Project, ou densifier localement |
| Statistics énormes | La sculpture est comptée | Statistics en Edit Mode sur la cage seule |
