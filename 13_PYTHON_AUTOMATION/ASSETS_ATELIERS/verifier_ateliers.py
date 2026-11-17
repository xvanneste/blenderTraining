"""Tests des livrables techniques CH13.04 à CH13.09 sous Blender 5.3."""
import importlib.util
import runpy
import subprocess
import sys
import tempfile
import tomllib
import zipfile
from pathlib import Path

import bpy

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def plans():
    source = REPO / "13_PYTHON_AUTOMATION/CH13_03_MESH_MATERIALS/COMPLETED_EXAMPLES/ch13_03_presentoir_solution.blend"
    bpy.ops.wm.open_mainfile(filepath=str(source))
    runpy.run_path(str(HERE / "preparer_plans.py"))
    scene = bpy.context.scene
    assert set(bpy.data.collections["COL_Plans"].objects.keys()) == {"PLAN_010", "PLAN_020"}
    for frame, camera in ((1, "PLAN_010"), (24, "PLAN_010"), (25, "PLAN_020"), (48, "PLAN_020")):
        scene.frame_set(frame)
        assert scene.camera.name == camera
    assert (scene.render.resolution_x, scene.render.resolution_y, scene.render.fps) == (640, 360, 24)


def lot():
    render = runpy.run_path(str(HERE / "rendre_lot.py"))["rendre"]
    scene = HERE / "presentoir_plans.blend"
    with tempfile.TemporaryDirectory(prefix="BCMA essais ") as directory:
        dst = Path(directory)
        render(bpy.app.binary_path, scene, dst)
        first, second = (dst / "plan_0001.png").read_bytes(), (dst / "plan_0025.png").read_bytes()
        assert first != second and len(second) > 10000
        try:
            render(bpy.app.binary_path, dst / "absent.blend", dst)
        except (FileNotFoundError, subprocess.CalledProcessError):
            pass
        else:
            raise AssertionError("Le lot ne doit pas accepter un fichier d’entrée absent.")
        assert (dst / "plan_0001.png").read_bytes() == first


def qc():
    bpy.ops.wm.open_mainfile(filepath=str(HERE / "presentoir_plans.blend"))
    scene = bpy.context.scene
    relever = runpy.run_path(str(HERE / "controler_scene.py"))["relever"]
    assert relever(scene) == []
    bpy.data.objects["GEO_Bloc_1_1"].name = "BOX_01"
    obj = bpy.data.objects["GEO_Bloc_1_2"]
    obj.scale.x = 1.2
    image = bpy.data.images.new("Texture manquante", 8, 8)
    image.source = "FILE"
    image.filepath = "//__bcma_texture_absente__.png"
    image.use_fake_user = True
    assert set(relever(scene)) == {("NOM", "BOX_01"), ("ECHELLE", obj.name),
                                   ("IMAGE_ABSENTE", image.name)}


def operator(namespace):
    namespace["register"]()
    try:
        cursor = bpy.context.scene.cursor
        cursor.location = (0.4, 1.3, 0.8)
        assert bpy.ops.bcma.ajouter_repere.poll()
        assert bpy.ops.bcma.ajouter_repere() == {"FINISHED"}
        obj = bpy.context.collection.objects["REP_Plan"]
        assert obj.empty_display_type == "ARROWS" and (obj.location - cursor.location).length < 1e-5
        bpy.ops.mesh.primitive_cube_add()
        bpy.ops.object.mode_set(mode="EDIT")
        try:
            assert not bpy.ops.bcma.ajouter_repere.poll()
        finally:
            bpy.ops.object.mode_set(mode="OBJECT")
    finally:
        namespace["unregister"]()
    assert not hasattr(bpy.types, "BCMA_PT_plan")


def panel():
    operator(runpy.run_path(str(HERE / "__init__.py")))


def archive():
    package = HERE / "bcma_reperes-1.0.0.zip"
    result = subprocess.run([bpy.app.binary_path, "--command", "extension", "validate", str(package)],
                            check=True, capture_output=True)
    assert b"bcma_reperes" in result.stdout + result.stderr
    with zipfile.ZipFile(package) as zipped:
        assert set(zipped.namelist()) == {"__init__.py", "blender_manifest.toml"}
        assert tomllib.loads(zipped.read("blender_manifest.toml").decode("utf-8-sig"))["version"] == "1.0.0"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "__init__.py"
            path.write_bytes(zipped.read("__init__.py"))
            operator(runpy.run_path(str(path)))


def timings():
    measure = runpy.run_path(str(HERE / "mesurer.py"))["mesure"]
    for size in (25, 250, 5000):
        result = measure(size)
        assert result.keys() == {"parcours", "index"} and all(time > 0 for time in result.values())


if __name__ == "__main__":
    cases = {"13.04": plans, "13.05": lot, "13.06": qc, "13.07": panel, "13.08": archive, "13.09": timings}
    case = sys.argv[sys.argv.index("--") + 1]
    cases[case]()
    print(f"BCMA {case} · contrôle réussi")
