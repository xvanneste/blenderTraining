"""Contrôle les objets de la collection de production et les images externes."""
from pathlib import Path
import bpy


def relever(scene):
    findings = []
    collection = scene.collection.children.get("COL_Presentoir")
    if not collection or not collection.objects:
        return [("COLLECTION_ABSENTE", "COL_Presentoir")]
    for obj in collection.objects:
        if obj.type == "MESH":
            if not obj.name.startswith("GEO_"):
                findings.append(("NOM", obj.name))
            if any(abs(value - 1.0) > 1e-4 for value in obj.scale):
                findings.append(("ECHELLE", obj.name))
    for image in bpy.data.images:
        if image.users and image.source == "FILE" and not image.packed_file:
            path = bpy.path.abspath(image.filepath, library=image.library)
            if not Path(path).is_file():
                findings.append(("IMAGE_ABSENTE", image.name))
    return sorted(findings)


if __name__ == "__main__":
    result = relever(bpy.context.scene)
    for code, name in result:
        print(code, name)
    print(f"{len(result)} anomalie(s)")
