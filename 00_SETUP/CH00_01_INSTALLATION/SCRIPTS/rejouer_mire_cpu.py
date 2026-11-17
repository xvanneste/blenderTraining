"""Rejoue les réglages et le rendu CPU de CH00.01 depuis le fichier de départ."""
import subprocess
import sys
import tempfile
from pathlib import Path

import bpy

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.dont_write_bytecode = True
from validate_ch00_01 import Report, image_mean_luminance, validate_testcard


def main():
    scene = bpy.context.scene
    assert Path(bpy.data.filepath).name == "ch00_01_testcard_starter.blend"
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.use_denoising = True
    scene.render.resolution_percentage = 100
    scene.render.filepath = "//renders/mire_"
    bpy.context.preferences.filepaths.save_version = 0

    with tempfile.TemporaryDirectory(prefix="BCMA mire ") as tmp:
        directory = Path(tmp)
        for version, samples in ((1, 128), (2, 64)):
            scene.cycles.samples = samples
            path = directory / f"ch00_01_testcard_essai_v{version:03}.blend"
            bpy.ops.wm.save_as_mainfile(filepath=str(path), relative_remap=False, compress=True)
            prefix = f"mire_cpu_v{version:03}_"
            subprocess.run(
                [bpy.app.binary_path, "-b", str(path), "-t", "8", "-o", f"//renders/{prefix}####",
                 "-F", "PNG", "-f", "1", "--", "--cycles-device", "CPU"],
                check=True,
            )
            png = directory / "renders" / f"{prefix}0001.png"
            with png.open("rb") as stream:
                assert stream.read(8) == b"\x89PNG\r\n\x1a\n"
            assert image_mean_luminance(str(png)) > 0.02
        bpy.ops.wm.open_mainfile(filepath=str(path))
        scene = bpy.context.scene
        assert scene.cycles.samples == 64
        cpu = Report()
        validate_testcard(cpu, scene, device="CPU")
        assert cpu.print() == 0
        gpu = Report()
        validate_testcard(gpu, scene, device="GPU")
        assert [ok for ok, _, _, _, mandatory in gpu.items if mandatory].count(False) == 1


if __name__ == "__main__":
    main()
