"""Tests nominaux et contre-exemples du pilote et du mini-pipeline."""
import shutil
import sys
import tempfile
import wave
import zipfile
from contextlib import contextmanager
from pathlib import Path

import bpy

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.dont_write_bytecode = True
import controle_pipeline as C


@contextmanager
def refus(expected):
    try:
        yield
    except (ValueError, FileNotFoundError) as error:
        assert expected.casefold() in str(error).casefold(), error
    else:
        raise AssertionError(f"Refus attendu : {expected}")


def plans():
    rows = C.read_rows(HERE / "plans_pilote.csv")
    assets = {row["item"] for row in C.read_rows(HERE / "assets_pilote.csv")}
    assert C.valider_plans(rows, assets) == 2880
    assert len(rows) == 12
    with refus("chevauchement"):
        C.valider_plans([rows[0], {**rows[1], "debut": "264"}, *rows[2:]], assets)
    with refus("répété"):
        C.valider_plans([rows[0], {**rows[1], "plan": rows[0]["plan"]}, *rows[2:]], assets)
    with refus("inconnus"):
        C.valider_plans([{**rows[0], "actifs": "A01+ABSENT"}, *rows[1:]], assets)

    bpy.ops.wm.open_mainfile(filepath=str(HERE / "pilote_timeline.blend"))
    scene = bpy.context.scene
    assert (scene.frame_end, scene.render.fps) == (2880, 24)
    expected = {row["plan"]: int(row["debut"]) for row in rows}
    assert {marker.name: marker.frame for marker in scene.timeline_markers} == expected
    layer = scene.objects["GP_Planches"].data.layers["Vignettes"]
    assert {frame.frame_number for frame in layer.frames} == set(expected.values())


def bibliotheque():
    with tempfile.TemporaryDirectory(prefix="bcma_link_") as tmp:
        directory = Path(tmp)
        for name in ("A03_Balise_v001.blend", "A03_Balise_v002.blend", "SQ020_SH020_override.blend"):
            shutil.copy2(HERE / name, directory / name)
        bpy.ops.wm.open_mainfile(filepath=str(directory / "SQ020_SH020_override.blend"))
        scene = bpy.context.scene
        obj = scene.objects["GEO_A03_Coffret"]
        assert obj.override_library and abs(obj.location.x - 1.25) < 1e-5
        source = obj.override_library.reference
        assert source.library.filepath == "//A03_Balise_v001.blend"
        assert abs(source.location.x) < 1e-5
        assert Path(bpy.path.abspath(source.library.filepath)).parent == directory
        bpy.ops.wm.open_mainfile(filepath=str(directory / "A03_Balise_v002.blend"))
        assert abs(bpy.data.objects["GEO_A03_Fenetre"].dimensions.x - .38) < .001


def lots():
    rows = C.read_rows(HERE / "lots_rendu.csv")
    assert C.valider_lots(rows, HERE, (640, 360)) == 2
    with tempfile.TemporaryDirectory() as tmp:
        dst = Path(tmp)
        expected = dst / rows[0]["sortie"]
        expected.parent.mkdir(parents=True)
        with refus("plan_0001.png"):
            C.valider_lots(rows, dst, (640, 360))
        expected.write_text("Rendu incomplet", encoding="utf-8")
        with refus("PNG invalide"):
            C.valider_lots(rows, dst, (640, 360))
    with refus("Dimensions incorrectes"):
        C.valider_lots(rows, HERE, (320, 180))


def planning():
    rows = C.read_rows(HERE / "charges_pilote.csv")
    report = C.planifier(rows)
    assert report["charge"] == 24 and report["delai"] == 19
    assert report["chemin"] == ["DEV", "ANIMATIQUE", "LAYOUT", "ANIM", "RENDU", "LIVRAISON"]
    for target, new_duration, expected in (("RENDU", 5, 21), ("ASSETS", 4, 19)):
        mutated = [{**row, "jours": str(new_duration)} if row["tache"] == target else row for row in rows]
        assert C.planifier(mutated)["delai"] == expected
    with refus("Cycle"):
        C.planifier([{**rows[0], "parents": "LIVRAISON"}, *rows[1:]])


def archive():
    original = HERE / "livraison_demo.zip"
    report = C.verifier_archive(original)
    assert report == {"version": "v001", "pieces": 10, "sous_titres": 2}
    with tempfile.TemporaryDirectory(prefix="bcma_reception_") as tmp:
        target = Path(tmp)
        with zipfile.ZipFile(original) as source:
            source.extractall(target)
            bad = target / "alteree.zip"
            with zipfile.ZipFile(bad, "w") as altered:
                for filename in source.namelist():
                    altered.writestr(filename, "altération".encode("utf-8") if filename == "LIRE.md" else source.read(filename))
        with refus("Empreinte"):
            C.verifier_archive(bad)
        with refus("Bornes"):
            C.verifier_srt("1\n00:00:14,000 --> 00:00:15,050\n[Signal]", 15000)

        scene_file = target / "Projet/sur_le_quai_animatique.blend"
        bpy.ops.wm.open_mainfile(filepath=str(scene_file))
        scene = bpy.context.scene
        assert (scene.frame_end, scene.render.fps) == (360, 24)
        for strip in scene.sequence_editor.strips:
            if strip.type == "IMAGE":
                assert (Path(bpy.path.abspath(strip.directory)) / strip.elements[0].filename).is_file()
            if strip.type == "SOUND":
                assert Path(bpy.path.abspath(strip.sound.filepath)).is_file()
        master = bpy.data.movieclips.load(str(target / "Master/sur_le_quai.mkv"))
        web = bpy.data.movieclips.load(str(target / "Revue/sur_le_quai.mp4"))
        try:
            for clip in (master, web):
                assert tuple(clip.size) == (640, 360) and clip.frame_duration == 360, (
                    clip.name, tuple(clip.size), clip.frame_duration)
        finally:
            bpy.data.movieclips.remove(master)
            bpy.data.movieclips.remove(web)
            bpy.ops.wm.read_factory_settings(use_empty=True)
        with wave.open(str(target / "Master/mix.wav"), "rb") as mix:
            assert abs(mix.getnframes() / mix.getframerate() - 15) < .05


if __name__ == "__main__":
    cases = {"plans": plans, "bibliotheque": bibliotheque, "lots": lots,
             "planning": planning, "archive": archive}
    case = sys.argv[sys.argv.index("--") + 1]
    cases[case]()
    print(f"Pilote {case} · vérifié")
