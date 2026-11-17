"""Contrôle l'état du fichier livré pour CH13.02."""
import sys
from pathlib import Path

import bpy

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "SCRIPTS"))
import bcma_lib as L


def uses_material(obj, name):
    return bool(
        obj and obj.type == "MESH" and obj.material_slots
        and obj.material_slots[0].material
        and obj.material_slots[0].material.name == name
    )


def main():
    r = L.Report("CH13.02 — L'atelier bpy")
    meshes = bpy.context.scene.objects
    a = meshes.get("GEO_Crate_A")
    b = meshes.get("GEO_Crate_B")
    marker = meshes.get("GEO_Marker")
    props = bpy.data.collections.get("COL_Props")

    r.check(a and b and a.type == b.type == "MESH", "Deux caisses présentes", points=2)
    r.check(a and b and a.data != b.data, "Maillages indépendants",
            "Copiez b.data avant de modifier ses matériaux.", points=2)
    r.check(uses_material(a, "MAT_Blue"), "A conserve MAT_Blue", points=1)
    r.check(uses_material(b, "MAT_Orange"), "B utilise MAT_Orange", points=1)
    r.check(marker and marker.type == "MESH" and len(marker.data.vertices) > 8,
            "Repère maillé présent", points=2)
    r.check(marker and max(abs(v - t) for v, t in zip(marker.location, (1.7, 0, 0.3))) < 0.01,
            "Repère à (1.7, 0, 0.3)", points=1)
    r.check(props and all(obj and props.objects.get(obj.name) == obj for obj in (a, b, marker)),
            "Les trois objets appartiennent à COL_Props", points=1)
    r.check(b and bpy.context.view_layer.objects.active == b and list(bpy.context.selected_objects) == [b],
            "B est la seule sélection et l'objet actif", points=2)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
