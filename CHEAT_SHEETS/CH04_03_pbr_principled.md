# Fiche de révision — CH04.03 Principled BSDF

Métal : Metallic 1, Base Color = couleur du reflet (jamais sombre), Roughness 0,1–0,4.
Diélectrique : Metallic 0, albedo 0,02–0,9 (jamais 0 ni 1).
Verre : Transmission Weight 1, Roughness ≤ 0,1, IOR ≈ 1,5.
Cire/peau : Subsurface Weight ≥ 0,2, Radius R > V > B ; Coat pour le vernis.
Metallic ≈ 0 ou 1 ; un métal a besoin d'un environnement clair. Correcteur : `--exercise pbr [--debug]`.
