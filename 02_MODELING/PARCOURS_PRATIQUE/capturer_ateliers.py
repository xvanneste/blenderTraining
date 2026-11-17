"""Capture the actual Blender UI. Run in a separate foreground Blender instance."""
from pathlib import Path
import sys
import traceback
import bpy
from mathutils import Vector

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
OUT = ASSETS / "captures"
REF = HERE.parents[1] / "PROPOSITIONS" / "RECONSTRUCTION_2_VUES"
OUT.mkdir(exist_ok=True)

jobs = [
    ("01-modes-objet", None, "Cube", (0,0,0), 5, (1,-2,1.2), "OBJECT", ""),
    ("01-modes-selections", None, "Cube", (0,0,0), 5, (1,-2,1.2), "VERT", ""),
    ("02-inset-extrude", ASSETS/"caisse.blend", "Cuve creuse", (0,0,.20), .98, (1,-2,2.4), "FACE", ""),
    ("03-miroir-couture", ASSETS/"epee.blend", "Demi-lame · Mirror", (0,0,.5), 1.5, (0,-1,0), "VERT", "MODIFIER"),
    ("04-images-ortho", REF/"personnage_deux_vues.blend", "Référence face", (0,0,.91), 2.7, (0,-1,0), "REF", "DATA"),
    ("04-images-profil", REF/"personnage_deux_vues.blend", "Référence profil", (0,0,.91), 2.7, (1,0,0), "REF", "DATA"),
    ("05-extrusion-bras", ASSETS/"cage_humain.blend", "GEO_Cage_Humaine", (.26,0,1.27), 1.02, (.25,-1,.26), "ARM", ""),
    ("06-visage-cage", REF/"visage_recale.blend", "GEO_Buste_Recalé", (0,-.035,1.64), .37, (0,-1,0), "VERT", ""),
    ("07-coude-poids", ASSETS/"cage_humain.blend", "GEO_Cage_Humaine", (.24,-.02,1.24), .99, (.27,-1,.29), "WEIGHT", ""),
    ("08-reimport-export", ASSETS/"projet_humain"/"verification_import.blend", bpy.types.Armature, (0,0,.92), 2.65, (.25,-1,.1), "OBJECT", ""),
]

if "--" in sys.argv:
    names = set(sys.argv[sys.argv.index("--") + 1:])
    jobs = [job for job in jobs if job[0] in names]

index = -1
phase = 0


def configure(w, job):
    name, _, identifier, position, distance, direction, mode, panel = job
    area = next(a for a in w.screen.areas if a.type == "VIEW_3D")
    region = next(r for r in area.regions if r.type == "WINDOW")
    space = area.spaces.active
    view = space.region_3d
    view.view_perspective = "ORTHO"
    view.view_location = position
    view.view_distance = distance
    view.view_rotation = Vector(direction).to_track_quat("Z", "Y")
    space.shading.type = "SOLID"
    space.shading.color_type = "MATERIAL"
    space.overlay.show_overlays = True
    space.overlay.show_relationship_lines = False
    space.show_region_ui = False
    space.show_region_toolbar = True
    with bpy.context.temp_override(window=w, area=area, region=region):
        bpy.ops.object.select_all(action="DESELECT")
        if isinstance(identifier, str):
            obj = bpy.data.objects.get(identifier)
            if obj is None and mode == "REF":
                obj = next(o for o in bpy.context.scene.objects if o.type == "EMPTY"
                           and o.empty_display_type == "IMAGE"
                           and name.rsplit("-", 1)[-1].replace("ortho", "face") in o.name.lower())
        else:
            obj = next(o for o in bpy.context.scene.objects if o.type == "ARMATURE")
            obj.data.display_type = "STICK"
            obj.data.show_bone_custom_shapes = False
            obj.show_in_front = True
        if mode == "REF":
            for o in bpy.context.scene.objects:
                if o.type == "MESH":
                    o.hide_set(True)
        obj.hide_set(False)
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        if mode in {"VERT", "FACE", "ARM"}:
            for face in obj.data.polygons:
                face.select = False
            for edge in obj.data.edges:
                edge.select = False
            for v in obj.data.vertices:
                v.select = ((mode == "ARM" and .34 < v.co.x < .46)
                            or (name == "01-modes-selections" and v.co.z > 0))
            bpy.context.scene.tool_settings.mesh_select_mode = (mode != "FACE", False, mode == "FACE")
            bpy.ops.object.mode_set(mode="EDIT")
        if mode == "WEIGHT":
            bpy.context.scene.frame_set(25)
            obj.vertex_groups.active_index = obj.vertex_groups["avantbras.L"].index
            bpy.ops.object.mode_set(mode="WEIGHT_PAINT")
        if panel:
            props = next(a for a in w.screen.areas if a.type == "PROPERTIES")
            props.spaces.active.context = panel


def tick():
    global index, phase
    try:
        if phase == 0:
            index += 1
            if index == len(jobs):
                bpy.ops.wm.quit_blender()
                return None
            _, file, *_ = jobs[index]
            phase = 1
            if file:
                bpy.ops.wm.open_mainfile(filepath=str(file), load_ui=False)
            else:
                bpy.ops.wm.read_factory_settings()
            return 1.0
        w = bpy.context.window_manager.windows[0]
        job = jobs[index]
        if phase == 1:
            configure(w, job)
            phase = 2
            return 1.0
        area = next(a for a in w.screen.areas if a.type == "VIEW_3D")
        with bpy.context.temp_override(window=w, area=area):
            print(job[0], bpy.ops.screen.screenshot(filepath=str(OUT / (job[0] + ".png"))), flush=True)
    except Exception:
        traceback.print_exc()
    phase = 0
    return .3


bpy.app.timers.register(tick, first_interval=1, persistent=True)