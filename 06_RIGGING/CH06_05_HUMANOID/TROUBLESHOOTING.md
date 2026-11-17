# CH06.05 — Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Generate Rig n'apparaît pas | Module Rigify désactivé | Préférences > Add-ons > Rigify |
| Rig plus grand que le corps | Méta-rig non mis à l'échelle | Échelle ≈ 0,89 puis Apply Scale |
| Aucun groupe de sommets | Corps parenté au méta-rig | Parenter à RIG_Hero (généré) |
| Le pied ne suit pas | Rig décalé du corps | Rig à l'origine, sous le corps |
| Bras déformés bizarrement ; correcteur : articulation HORS du bras | Bras du méta-rig non ajustés (trop hauts, trop courts) | Edit Mode : coude et poignet au milieu du bras (face ET profil), puis Re-Generate Rig et refaire Automatic Weights |
| Peau qui « flotte » | Poids non normalisés | Normalize All |
| Génération impossible | Méta-rig avec erreur | Lire le message d'erreur Rigify |
| Rig lourd | 706 bones | Masquer les collections ; CH06.11 |
