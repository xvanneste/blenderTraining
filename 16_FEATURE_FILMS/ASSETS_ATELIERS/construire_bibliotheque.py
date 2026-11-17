"""Génère deux publications de la balise et un plan avec override local."""
import sys
from pathlib import Path

import bpy

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "SCRIPTS"))
import bcma_lib as L


def publish(version, face_width):
    scene = L.reset("Publication de la balise A03")
    col = L.collection("COL_A03_Balise")
    col["asset_id"] = "A03"
    col["publication"] = version
    dark = L.material("Ardoise", (.07, .12, .16))
    amber = L.material("Ocre", (.86, .33, .06))
    for name, position, scale, material in (
        ("GEO_A03_Coffret", (0, 0, 1.1), (.24, .17, .22), dark),
        ("GEO_A03_Fenetre", (0, -.18, 1.12), (face_width, .019, .09), amber),
        ("GEO_A03_Mat", (0, 0, .47), (.07, .07, .47), dark),
    ):
        obj = L.cube(name, col, size=2, location=position)
        for v in obj.data.vertices:
            for axis in range(3):
                v.co[axis] *= scale[axis]
        obj.data.materials.append(material)
    scene.world = bpy.data.worlds.new("Monde")
    L.save(str(HERE / f"A03_Balise_{version}.blend"))


def plan():
    scene = L.reset("SQ020_SH020 · Plan lié")
    path = HERE / "A03_Balise_v001.blend"
    # Save once so relative paths refer to the intended project directory.
    dest = HERE / "SQ020_SH020_override.blend"
    L.save(str(dest))
    with bpy.data.libraries.load(str(path), link=True, relative=True) as (_, destination):
        destination.collections = ["COL_A03_Balise"]
    linked = destination.collections[0]
    scene.collection.children.link(linked)
    local = linked.override_hierarchy_create(scene, bpy.context.view_layer, do_fully_editable=True)
    col = next((collection for collection in scene.collection.children if collection == local), None)
    if col is None:
        scene.collection.children.link(local)
    if linked.name in scene.collection.children:
        scene.collection.children.unlink(linked)
    for obj in local.objects:
        obj.location.x += 1.25
        obj.keyframe_insert(data_path="location", frame=1)
    L.instructions("Bibliothèque A03 v001. Les transformations locales sont conservées sur l’override du plan.")
    L.save(str(dest))


def main():
    publish("v001", .15)
    publish("v002", .19)
    plan()


if __name__ == "__main__":
    L.run(main)
