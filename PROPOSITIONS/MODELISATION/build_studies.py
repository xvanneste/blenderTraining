"""Build the two original Blender studies for the modeling audit."""
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT.parents[1] / "SCRIPTS"))
import bcma_lib as L


def box(name, collection, loc, dims, mat, radius):
    ob = L.cube(name, collection, mat, size=1, location=loc)
    ob.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    bevel = ob.modifiers.new("Rayons de fabrication", "BEVEL")
    bevel.width, bevel.segments = radius, 4
    normal = ob.modifiers.new("Normales pondérées", "WEIGHTED_NORMAL")
    return ob


def typography(name, value, loc, size, mat, col, align="LEFT"):
    font = bpy.data.curves.new(name, "FONT")
    font.body, font.size, font.align_x = value, size, align
    ob = bpy.data.objects.new(name, font)
    col.objects.link(ob)
    ob.location = loc
    ob.rotation_euler.x = math.pi / 2
    font.materials.append(mat)
    return ob


def setup(name):
    L.reset(name)
    col = L.collection("ASSET")
    studio = L.collection("STUDIO")
    L.world((0.12, 0.15, 0.20), 0.42)
    return col, studio


def show(studio, target, eye, framing, backdrop, size=(1120, 900)):
    cam = L.camera("CAM_Review", studio, location=eye)
    cam.rotation_euler = (Vector(target) - cam.location).to_track_quat("-Z", "Y").to_euler()
    cam.data.type, cam.data.ortho_scale = "ORTHO", framing
    ground = L.plane("Studio_Fond", studio, backdrop, size=200)
    ground.location.z = -0.035

    for name, loc, power, scale, color in (
        ("Key", (-4, -4, 7), 900, 4.5, (1.0, 0.86, 0.73)),
        ("Fill", (5, -2, 4), 520, 4, (0.68, 0.82, 1.0)),
        ("Rim", (1, 5, 6), 1050, 3, (1.0, 0.92, 0.78)),
    ):
        lamp = L.light(name, studio, location=loc, energy=power, size=scale, color=color)
        lamp.rotation_euler = (Vector(target) - lamp.location).to_track_quat("-Z", "Y").to_euler()
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 16
    scene.cycles.use_denoising = True
    scene.render.resolution_x, scene.render.resolution_y = size
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.view_settings.view_transform = "AgX"
    return scene


def recorder():
    col, studio = setup("Balise de terrain")
    amber = L.material("ABS ocre", (0.67, 0.21, 0.031), 0.36)
    rubber = L.material("Elastomère graphite", (0.035, 0.043, 0.049), 0.63)
    metal = L.material("Aluminium anodisé", (0.20, 0.24, 0.27), 0.34, 0.78)
    recess = L.material("Cavités", (0.012, 0.019, 0.022), 0.53)
    glass = L.material("Verre fumé", (0.021, 0.075, 0.097), 0.24, 0.36)
    green = L.material("Afficheur", (0.36, 0.78, 0.62), emission=(0.36, 0.78, 0.62), emission_strength=0.55)
    ivory = L.material("Sérigraphie", (0.78, 0.82, 0.74), 0.65)

    box("Coque arrière", col, (0, 0.09, 1.54), (2.06, 0.69, 2.91), amber, 0.14)
    box("Joint périphérique", col, (0, -0.24, 1.54), (2.07, 0.09, 2.88), rubber, 0.12)
    box("Face avant", col, (0, -0.33, 1.54), (1.98, 0.17, 2.83), amber, 0.10)
    box("Bouclier bas", col, (0, -0.015, 0.19), (2.17, 0.94, 0.36), rubber, 0.12)
    box("Bouclier haut", col, (0, -0.015, 2.87), (2.17, 0.94, 0.34), rubber, 0.12)
    box("Interface encastrée", col, (0, -0.424, 1.97), (1.67, 0.08, 1.20), rubber, 0.09)
    box("Écran", col, (0, -0.474, 2.10), (1.46, 0.035, 0.79), glass, 0.07)
    box("Bandeau boutons", col, (0, -0.428, 1.04), (1.45, 0.075, 0.43), rubber, 0.065)
    for x, label, mat in [(-0.50, "REC", amber), (0.0, "MARK", metal), (0.50, "PLAY", metal)]:
        box("Bouton " + label, col, (x, -0.49, 1.035), (0.39, 0.10, 0.25), mat, 0.04)
        typography("Label " + label, label, (x, -0.547, 1.005), 0.086, ivory, col, "CENTER")
    box("Fond de grille", col, (0, -0.422, 0.58), (1.31, 0.055, 0.36), recess, 0.05)
    for i in range(9):
        x = (i - 4) * 0.133
        box("Ajoure de grille", col, (x, -0.457, 0.58), (0.078, 0.040, 0.28), metal, 0.021)

    for x in (-0.86, 0.86):
        for z in (0.58, 2.53):
            ob = L.cylinder("Tête de vis", col, metal, vertices=32, radius=0.048, depth=0.016, location=(x, -0.423, z))
            ob.rotation_euler.x = math.pi / 2
            box("Empreinte de vis", col, (x, -0.433, z), (0.063, 0.007, 0.011), recess, 0.003)
    for x in (-0.54, 0.54):
        L.cylinder("Prise haute", col, metal, vertices=48, radius=0.16, depth=0.18, location=(x, 0.035, 3.08))
        L.cylinder("Noyau de prise", col, recess, vertices=48, radius=0.103, depth=0.018, location=(x, 0.035, 3.175))
    for i in range(14):
        x = -0.56 + i * 0.083
        height = 0.04 + 0.19 * abs(math.sin(i * 1.13)) * math.sin((i + 1) * math.pi / 16)
        box("Barre du signal", col, (x, -0.496, 1.99 + height / 2), (0.039, 0.018, height), green, 0.006)
    typography("Statut", "REC   00:18:42", (-0.58, -0.503, 2.36), 0.126, green, col)
    typography("Mode", "FIELD AUDIO   /   48k", (-0.57, -0.503, 1.82), 0.087, green, col)
    typography("Marquage", "ATLAS   /   R-07", (0, -0.434, 2.63), 0.108, ivory, col, "CENTER")
    for i in range(5):
        box("Strie latérale", col, (1.04, 0.13, 1.41 + i * 0.135), (0.058, 0.36, 0.08), rubber, 0.025)

    scene = show(studio, (0, 0, 1.52), (4.5, -9, 5.6), 4.55,
                 L.material("Fond ardoise", (0.105, 0.14, 0.18), 0.75))
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 0.06
    return scene


def loft(name, col, sections, sides=24):
    """Sweep elliptical sections along an authored path."""
    verts = []
    for i, (center, width, depth) in enumerate(sections):
        c = Vector(center)
        direction = Vector(sections[min(i+1, len(sections)-1)][0]) - Vector(sections[max(0,i-1)][0])
        direction.normalize()
        u = direction.cross(Vector((0, 0, 1))).normalized()
        v = u.cross(direction).normalized()
        for k in range(sides):
            angle = 2 * math.pi * k / sides
            verts.append(c + u * (width * math.cos(angle)) + v * (depth * math.sin(angle)))
    faces = []
    for i in range(len(sections)-1):
        for k in range(sides):
            j = (k + 1) % sides
            faces.append((i*sides+k, (i+1)*sides+k, (i+1)*sides+j, i*sides+j))
    faces.extend([tuple(range(sides)), tuple(reversed(range(len(verts)-sides, len(verts))))])
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    ob = bpy.data.objects.new(name, mesh)
    col.objects.link(ob)
    mod = ob.modifiers.new("Interpolation des sections", "SUBSURF")
    mod.levels = 2
    return ob


def hand():
    col, studio = setup("Étude de main")
    blocks = L.collection("01_Construction", col)
    palm = [
        ((-0.10,-1.74,0.43),0.43,0.21), ((-0.10,-1.40,0.43),0.50,0.25),
        ((-0.10,-1.05,0.45),0.55,0.27), ((-0.06,-0.63,0.48),0.70,0.30),
        ((0.01,-0.13,0.51),0.83,0.31), ((0.06,0.30,0.51),0.80,0.25),
        ((0.06,0.58,0.49),0.70,0.20), ((0.08,0.76,0.48),0.66,0.145),
    ]
    parts=[loft("Paume et carpe",blocks,palm)]
    digits = [
        ("Pouce", [((-0.54,-0.58,0.45),0.33,0.24),((-0.86,-0.38,0.49),0.32,0.22),((-1.12,-0.03,0.52),0.27,0.19),((-1.43,0.16,0.57),0.21,0.17),((-1.68,0.31,0.60),0.16,0.14),((-1.76,0.39,0.60),0.021,0.021)]),
        ("Index", [((-0.56,0.41,0.52),0.23,0.20),((-0.54,0.78,0.54),0.22,0.19),((-0.57,1.26,0.53),0.19,0.17),((-0.63,1.62,0.43),0.17,0.15),((-0.71,1.91,0.38),0.145,0.12),((-0.75,2.05,0.39),0.022,0.023)]),
        ("Majeur", [((-0.09,0.53,0.55),0.23,0.21),((-0.06,0.94,0.55),0.22,0.19),((-0.03,1.48,0.50),0.19,0.16),((-0.045,1.91,0.37),0.165,0.138),((-0.085,2.15,0.31),0.141,0.117),((-0.115,2.29,0.32),0.022,0.022)]),
        ("Annulaire", [((0.36,0.47,0.51),0.22,0.19),((0.42,0.88,0.52),0.21,0.17),((0.49,1.31,0.43),0.177,0.149),((0.51,1.74,0.28),0.158,0.129),((0.49,1.93,0.22),0.128,0.111),((0.46,2.06,0.23),0.020,0.023)]),
        ("Auriculaire", [((0.68,0.31,0.47),0.19,0.18),((0.82,0.61,0.46),0.172,0.15),((0.98,0.93,0.39),0.143,0.131),((1.02,1.22,0.26),0.137,0.11),((1.02,1.40,0.22),0.108,0.095),((0.99,1.52,0.23),0.018,0.019)]),
    ]
    for name, sections in digits:
        parts.append(loft(name, blocks, sections))
    parts.append(loft("Commissure majeur–annulaire", blocks, [
        ((0.16,0.31,0.49),0.26,0.16), ((0.17,0.57,0.47),0.245,0.155),
        ((0.18,0.79,0.47),0.205,0.13), ((0.20,0.94,0.47),0.13,0.095),
        ((0.22,1.03,0.47),0.035,0.035),
    ]))
    clay = L.material("Argile mate", (0.46,0.22,0.145), 0.70)
    for ob in parts:
        ob.data.materials.append(clay)
    # Keep the editable lofts as a hidden, inspectable construction stage.
    result = L.collection("02_Etude", col)
    duplicates = []
    for ob in parts:
        dupe = ob.copy()
        dupe.data = ob.data.copy()
        result.objects.link(dupe)
        bpy.context.view_layer.objects.active = dupe
        bpy.ops.object.modifier_apply(modifier=dupe.modifiers[0].name)
        duplicates.append(dupe)
    bpy.ops.object.select_all(action="DESELECT")
    for ob in duplicates:
        ob.select_set(True)
    bpy.context.view_layer.objects.active = duplicates[0]
    bpy.ops.object.join()
    study = bpy.context.object
    study.name = "GEO_Main_Etude"
    study.data.remesh_voxel_size = 0.028
    bpy.ops.object.voxel_remesh()
    polish = study.modifiers.new("Adoucir uniquement le raccord du blocage", "SMOOTH")
    polish.factor, polish.iterations = 0.82, 8
    bpy.ops.object.modifier_apply(modifier=polish.name)
    study.data.materials.clear()
    study.data.materials.append(clay)
    for poly in study.data.polygons:
        poly.use_smooth = True

    # Dorsal relief: restrained metacarpal planes and knuckles on the fused mesh.
    for vert in study.data.vertices:
        x, y, z = vert.co
        upward = max(0.0, min(1.0, (vert.normal.z - 0.25) / 0.65))
        dorsal = min(1.0, max(0.0, (z - 0.48) / 0.19)) * upward
        ridge = sum(0.033 * math.exp(-((x - cx) / 0.12)**2 - ((y - 0.14) / 0.48)**2)
                    for cx in (-0.42, -0.10, 0.25))
        joints = sum(0.064 * math.exp(-((x - cx) / 0.165)**2 - ((y - cy) / 0.15)**2)
                     for cx, cy in ((-0.56,0.71), (-0.065,0.84), (0.38,0.68), (0.76,0.48)))
        vert.co.z += dorsal * (ridge + joints)
    study.data.update()

    details = L.collection("03_Ongles", col)
    nail_mat = L.material("Argile claire · ongles", (0.58,0.31,0.23), 0.63)
    for name, sections in digits:
        tip = Vector(sections[-1][0])
        base = Vector(sections[-2][0])
        direction = (tip - base)
        direction.z = 0
        direction.normalize()
        across = Vector((direction.y, -direction.x, 0))
        center = base - 0.082 * direction
        width, length = sections[-2][1] * 0.57, 0.083
        vertices, faces = [], []
        # A projected nail surface, with an inset contour and a raised center.
        for ring in range(1, 5):
            r = ring / 4
            for n in range(24):
                angle = math.tau * n / 24
                a, b = math.cos(angle), math.sin(angle)
                a = math.copysign(abs(a)**0.77, a)
                b = math.copysign(abs(b)**0.77, b)
                point = center + across * (r * width * a) + direction * (r * length * b)
                hit, loc, _normal, _index = study.ray_cast(Vector((point.x,point.y,5)), Vector((0,0,-1)))
                if not hit:
                    break
                vertices.append((loc.x, loc.y, loc.z + 0.006 + 0.020 * (1.0-r*r)))
        if len(vertices) != 96:
            continue
        faces.append(tuple(range(24)))
        for r in range(3):
            for n in range(24):
                nxt = (n+1) % 24
                faces.append((24*r+n, 24*(r+1)+n, 24*(r+1)+nxt, 24*r+nxt))
        mesh = bpy.data.meshes.new("Ongle " + name)
        mesh.from_pydata(vertices, [], faces)
        mesh.update()
        nail = bpy.data.objects.new(mesh.name,mesh)
        details.objects.link(nail)
        mesh.materials.append(nail_mat)
        for poly in mesh.polygons:
            poly.use_smooth = True

    blocks.hide_viewport = blocks.hide_render = True
    scene = show(studio, (-0.10, 0.18, 0.41), (1.6,-3.7,7.5), 5.15,
                 L.material("Fond ivoire", (0.46,0.43,0.36), 0.80), size=(1000,1050))
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 0.048
    for name, eye in (("CAM_Dessus", (0.02,0.16,8)), ("CAM_Profil", (7.8,-0.5,2.7))):
        cam = L.camera(name, studio, location=eye, make_active=False)
        cam.rotation_euler = (Vector((-0.10,0.18,0.41)) - cam.location).to_track_quat("-Z", "Y").to_euler()
        cam.data.type, cam.data.ortho_scale = "ORTHO", 5.05
    return scene


def main():
    targets = L.args_after_dashdash()
    for name, builder in (("atlas_r07", recorder), ("main_etude", hand)):
        if targets and name not in targets:
            continue
        scene = builder()
        bpy.ops.object.select_all(action="DESELECT")
        for screen in bpy.data.screens:
            for area in screen.areas:
                if area.type == "VIEW_3D" and area.spaces.active.region_3d:
                    area.spaces.active.region_3d.view_perspective = "CAMERA"
        scene.render.filepath = f"//{name}.png"
        L.save(str(OUT / f"{name}.blend"))
        bpy.ops.render.render(write_still=True)
        if name == "main_etude":
            scene.camera = bpy.data.objects["CAM_Profil"]
            scene.render.filepath = "//main_profil.png"
            bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    L.run(main)
