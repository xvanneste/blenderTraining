"""Construit le layout, les trois vignettes et une animatique statique de 15 s."""
import math
import struct
import sys
import wave
from pathlib import Path

import bpy
from mathutils import Vector

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "SCRIPTS"))
import bcma_lib as L


def cube(name, col, location, scale, mat):
    obj = L.cube(name, col, size=2, location=location)
    obj.scale = scale
    obj.data.materials.append(mat)
    return obj


def viser(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()


def layout():
    scene = L.reset("Sur le quai · layout")
    scene.frame_end = 360
    scene.render.fps = 24
    dock = L.collection("A01_Quai")
    person = L.collection("A02_Silhouette")
    prop = L.collection("A03_Balise")
    studio = L.collection("Plans et lumière")
    deck = L.material("Ardoise", (.11, .19, .23))
    sea = L.material("Eau sombre", (.025, .07, .10), roughness=.24)
    blue = L.material("Imperméable", (.035, .14, .21))
    dark = L.material("Boîtier", (.055, .065, .085))
    skin = L.material("Main", (.41, .24, .17))
    amber = L.material("Signal", (.1, .075, .05), emission=(1, .43, .07), emission_strength=0.0)

    cube("Quai", dock, (0, 0, -.2), (3.9, 1.3, .2), deck)
    cube("Eau", dock, (0, 0, -.43), (20, 20, .1), sea)
    for x in (-3, -1.8, 1.8, 3):
        cube("Poteau", dock, (x, 1.08, .35), (.055, .055, .35), dark)
    cube("Garde-corps", dock, (0, 1.08, .70), (3, .045, .035), dark)
    cube("Pied de balise", prop, (.65, 0, .50), (.12, .11, .50), dark)
    cube("Boîtier", prop, (.65, 0, 1.01), (.24, .18, .22), dark)
    cube("Fenêtre du signal", prop, (.65, -.187, 1.11), (.16, .015, .075), amber)
    cube("Bouton", prop, (.397, -.07, 1.00), (.02, .05, .055), amber)

    # Silhouette de layout en volumes simples. Les proportions se lisent à la caméra.
    cube("Torse", person, (-.76, 0, 1.14), (.21, .14, .29), blue)
    for y in (-.10, .10):
        cube("Jambe", person, (-.76, y, .43), (.075, .065, .43), blue)
        cube("Pied", person, (-.70, y, .04), (.145, .068, .04), dark)
    head = L.sphere("Tête", person, radius=.15, location=(-.72, 0, 1.62))
    head.data.materials.append(skin)
    hand = L.sphere("Main de layout", person, radius=.073, location=(-.40, -.1, .9))
    hand.data.materials.append(skin)
    arm = cube("Avant-bras", person, (-.33, -.1, .95), (.3, .055, .055), blue)
    joint = Vector((-.63, -.10, 1.32))
    for frame, endpoint in ((1, (-.42,-.10,.86)), (121,(-.13,-.10,1.13)),
                            (172,(-.28,-.10,1.16)), (204,(.329,-.10,1.00)),
                            (217,(.329,-.10,1.00)), (245,(-.33,-.10,.99)), (360,(-.42,-.10,.86))):
        position = Vector(endpoint)
        hand.location = position
        hand.keyframe_insert("location", frame=frame)
        delta = position - joint
        arm.location = joint + delta / 2
        arm.rotation_euler = delta.to_track_quat("X", "Z").to_euler()
        arm.scale.x = delta.length / 2
        for channel in ("location", "rotation_euler", "scale"):
            arm.keyframe_insert(channel, frame=frame)

    glow = next(n for n in amber.node_tree.nodes if n.type == "BSDF_PRINCIPLED").inputs["Emission Strength"]
    for frame, value in ((1, 0), (216, 0), (217, 3), (360, 3)):
        glow.default_value = value
        glow.keyframe_insert("default_value", frame=frame)
    for name, location, energy, size in (
        ("Clé froide", (-3,-4,5), 760, 4), ("Fond", (2,3,4), 980, 3)
    ):
        lamp = L.light(name, studio, location=location, energy=energy, size=size)
        viser(lamp, (0, 0, .8))
    for name, position, target, scale, frame in (
        ("S010",(-3.8,-7,3.15),(0,0,.55),5.6,1),
        ("S020",(-.2,-4,2.0),(.15,0,1.04),1.95,121),
        ("S030",(2.1,-5,1.85),(.23,0,1.0),3.25,217),
    ):
        cam = L.camera(name, studio, location=position)
        cam.data.type = "ORTHO"
        cam.data.ortho_scale = scale
        viser(cam, target)
        scene.timeline_markers.new(name, frame=frame).camera = cam
    scene.frame_set(1)
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 12
    scene.cycles.use_denoising = True
    scene.render.resolution_x, scene.render.resolution_y = 640, 360
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    L.instructions("Sur le quai · Exercices CH15.02–06. Layout de travail. Les plans et la main sont animés. "
                   "La sortie de champ et la réaction complète restent à faire pendant l’atelier.")
    L.save(str(HERE / "sur_le_quai_layout.blend"))
    for name, frame in (("S010", 75), ("S020", 204), ("S030", 245)):
        scene.frame_set(frame)
        assert scene.camera.name == name
        scene.render.filepath = str(HERE / f"{name}.png")
        bpy.ops.render.render(write_still=True)


def animatique():
    sound = HERE / "signal.wav"
    with wave.open(str(sound), "wb") as handle:
        handle.setparams((1, 2, 48000, 0, "NONE", "not compressed"))
        handle.writeframes(b"".join(
            struct.pack("<h", int(11500 * (1 - i / 5760) ** 2 * math.sin(math.tau * 660 * i / 48000)))
            for i in range(5760)
        ))
    scene = L.reset("Sur le quai · animatique")
    scene.frame_end = 360
    scene.render.fps = 24
    scene.render.resolution_x, scene.render.resolution_y = 640, 360
    scene.render.resolution_percentage = 100
    editor = scene.sequence_editor_create()
    for name, start, duration in (("S010", 1, 120), ("S020", 121, 96), ("S030", 217, 144)):
        strip = editor.strips.new_image(name, str(HERE / f"{name}.png"), 1, start)
        strip.directory = "//"
        strip.frame_final_duration = duration
        scene.timeline_markers.new(name, frame=start)
    strip = editor.strips.new_sound("Signal", str(sound), 2, 217)
    strip.sound.filepath = "//signal.wav"

    scene.render.image_settings.media_type = "VIDEO"
    scene.render.ffmpeg.format = "MPEG4"
    scene.render.ffmpeg.codec = "H264"
    scene.render.ffmpeg.audio_codec = "AAC"
    scene.render.filepath = "//sur_le_quai_animatique_"
    L.save(str(HERE / "sur_le_quai_animatique.blend"))
    bpy.ops.render.render(animation=True)


if __name__ == "__main__":
    def main():
        layout()
        animatique()
    L.run(main)
