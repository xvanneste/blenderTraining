"""Vérifie les dates de coupe, le layout, les médias du VSE et l’export de revue."""
import csv
import sys
from pathlib import Path

import bpy

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "12_EDITING_SOUND/CH12_06_EXPORT/SCRIPTS"))
from mp4probe import analyse


def feuille():
    with (HERE / "plans.csv").open(encoding="utf-8-sig", newline="") as src:
        rows = [(s["plan"], int(s["debut"]), int(s["fin"])) for s in csv.DictReader(src)]
    assert rows == [("S010", 1, 120), ("S020", 121, 216), ("S030", 217, 360)]
    return rows


def animatique():
    bpy.ops.wm.open_mainfile(filepath=str(HERE / "sur_le_quai_animatique.blend"))
    scene = bpy.context.scene
    assert (scene.frame_start, scene.frame_end, scene.render.fps) == (1, 360, 24)
    strips = scene.sequence_editor.strips
    for name, first, last in feuille():
        strip = strips[name]
        assert (strip.frame_final_start, strip.frame_final_end) == (first, last + 1)
        png = Path(bpy.path.abspath(strip.directory)) / strip.elements[0].filename
        assert png.is_file() and png.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"
    hit = strips["Signal"]
    assert hit.frame_final_start == 217 and Path(bpy.path.abspath(hit.sound.filepath)).is_file()


def layout():
    bpy.ops.wm.open_mainfile(filepath=str(HERE / "sur_le_quai_layout.blend"))
    scene = bpy.context.scene
    for name, first, last in feuille():
        for frame in (first, last):
            scene.frame_set(frame)
            assert scene.camera.name == name
    hand = scene.objects["Main de layout"]
    button = scene.objects["Bouton"]
    scene.frame_set(172)
    before = (hand.location - button.location).length
    scene.frame_set(204)
    during = (hand.location - button.location).length
    scene.frame_set(245)
    after = (hand.location - button.location).length
    assert before > .5 and during < .08 and after > .5
    glow = next(n for n in bpy.data.materials["Signal"].node_tree.nodes if n.type == "BSDF_PRINCIPLED").inputs["Emission Strength"]
    scene.frame_set(216)
    assert glow.default_value == 0
    scene.frame_set(217)
    assert glow.default_value == 3


def export():
    animatique()
    result = analyse(str(HERE / "sur_le_quai_animatique_0001-0360.mp4"))
    video = next(track for track in result["tracks"] if track["kind"] == "vide")
    audio = next(track for track in result["tracks"] if track["kind"] == "soun")
    assert abs(result["duration"] - 15) < .05, result
    assert (video["width"], video["height"], video["codec"], audio["codec"]) == (640, 360, "avc1", "mp4a")


if __name__ == "__main__":
    case = sys.argv[sys.argv.index("--")+1]
    {"animatique":animatique,"layout":layout,"export":export}[case]()
    print(f"Sur le quai · {case} vérifié")
