"""
build_ch03_03_files.py — « Choisir sa résolution : Voxel Remesh, DynTopo, Multiresolution » (CH03.03).

  STARTER_FILES/ch03_03_remesh_starter.blend
      Les 16 masses du mannequin de CH03.01 (objets séparés qui se chevauchent).
  COMPLETED_EXAMPLES/ch03_03_remesh_solution.blend
      Cou, abdomen et épaules ajoutés (chevauchements), masses jointes (Ctrl+J) en SCULPT_Body puis Voxel Remesh (taille de voxel 0,012 m) : un seul
      volume fermé, en quads réguliers, prêt à sculpter.
  STARTER_FILES/ch03_03_multires_starter.blend
      SCULPT_HeadBase : tête de base légère (384 faces) ; texte DECISIONS (5 situations à trancher).
  COMPLETED_EXAMPLES/ch03_03_multires_solution.blend
      Modificateur Multiresolution subdivisé 5 fois (Subdivide), Sculpt = 5, Viewport = 3, Render = 5 ;
      base inchangée ; DECISIONS complété.
Usage : blender -b --factory-startup --python-exit-code 1 --python build_ch03_03_files.py
Testé avec : Blender 5.3.0.
"""
import importlib.util
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bcma_shots as S  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

CH = L.chapter_dir(__file__)
SRC01 = os.path.join(os.path.dirname(CH), "CH03_01_ARTISTIC_ANATOMY", "SCRIPTS", "build_ch03_01_files.py")
VOXEL = 0.012
DECISIONS_Q = """# DÉCISIONS — pour chaque situation, écrivez la méthode : VOXEL, DYNTOPO ou MULTIRES
# Format : numéro: MÉTHODE   (ex. « 1: VOXEL »)
# 1. Je démarre une créature à partir de boules jointes ; la topologie ne compte pas encore.
# 2. Je dois ajouter des cornes fines là où la densité manque, sans toucher au reste du sculpt.
# 3. Personnage déjà retopologisé pour l'animation : je veux des rides en gardant la base légère.
# 4. Mon sculpt a une densité chaotique ; je veux la redistribuer uniformément avant de continuer.
# 5. Je dois sculpter des détails fins sur un personnage dont les UV doivent être conservées.
"""
DECISIONS_A = DECISIONS_Q + "1: VOXEL\n2: DYNTOPO\n3: MULTIRES\n4: VOXEL\n5: MULTIRES\n"
NOTE_R = """CH03.03 — VOXEL REMESH (Object Mode)
1. Les masses doivent SE CHEVAUCHER pour fusionner : ajoutez un cou (MASS_Neck, entre tête et cage) et
   un abdomen (MASS_Abdomen, entre cage et bassin) et deux épaules (MASS_Shoulder_L/R, entre bras et cage) qui
   pénètrent dans leurs voisins.
   Sélectionnez toutes les masses MASS_* (A), Ctrl+J (Join) ; renommez l'objet SCULPT_Body (F2).
2. Object Data Properties > Remesh : Mode Voxel, Voxel Size 0,012 m ; bouton Voxel Remesh
   (en Sculpt Mode : Ctrl+R).
3. Le résultat est un seul volume fermé en quads réguliers : prêt pour la sculpture.
Vérification : SCRIPTS/validate_ch03_03.py -- --exercise remesh
"""
NOTE_M = """CH03.03 — MULTIRESOLUTION (SCULPT_HeadBase)
1. Modifier Properties > Add Modifier > Generate > Multiresolution.
2. Bouton Subdivide (Catmull-Clark) cinq fois : 5 niveaux.
3. Réglez : Levels Viewport 3 (fluidité), Sculpt 5 (détail), Render 5.
4. N'appliquez pas le modificateur : la base légère reste disponible pour le rigging.
5. Texte DECISIONS : répondez aux 5 situations (VOXEL, DYNTOPO ou MULTIRES).
Vérification : -- --exercise multires  et  -- --exercise decide
"""


def setup_view(target_z, dist):
    L.studio(subject_height=target_z * 1.6)
    cam = L.camera("CAM_View", L.collection("CAMERAS"), (dist * 0.45, -dist, target_z + 0.2), 50, make_active=True)
    S.look_at(cam, (0, 0, target_z))
    sc = L.render_defaults("BLENDER_EEVEE", 40)
    sc.camera = cam
    return sc


def bbox(name):
    o = bpy.data.objects[name]
    pts = [o.matrix_world @ v.co for v in o.data.vertices]
    return min(p.z for p in pts), max(p.z for p in pts)


def add_bridges():
    """Cou et abdomen : des masses qui CHEVAUCHENT tête/cage et cage/bassin, sinon le remesh
    produit des morceaux séparés (tête, buste, jambes)."""
    col = bpy.data.collections["MASSES"]
    skin = bpy.data.materials["MAT_Mass"]
    h0, _h1 = bbox("MASS_Head")
    _r0, r1 = bbox("MASS_Ribcage")
    r0, _ = bbox("MASS_Ribcage")
    _p0, p1 = bbox("MASS_Pelvis")
    L.cylinder("MASS_Neck", col, skin, radius=0.068, depth=(h0 + 0.05) - (r1 - 0.06), vertices=16,
               location=(0, 0.01, ((h0 + 0.05) + (r1 - 0.06)) / 2))
    L.sphere("MASS_Abdomen", col, skin, radius=1, location=(0, 0, (r0 + p1) / 2),
             scale=(0.13, 0.1, ((r0 + 0.08) - (p1 - 0.06)) / 2))
    for side in ("L", "R"):                          # deltoïdes : relient bras et cage
        arm = bpy.data.objects[f"MASS_UpperArm_{side}"]
        pts = [arm.matrix_world @ v.co for v in arm.data.vertices]
        top = max(pts, key=lambda q: q.z)
        L.sphere(f"MASS_Shoulder_{side}", col, skin, radius=1, location=(top.x * 0.85, 0, top.z - 0.04),
                 scale=(0.075, 0.06, 0.065))


def remesh(sol):
    spec = importlib.util.spec_from_file_location("b0301", SRC01)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    L.reset("SC_Remesh")
    mod.figure()
    if sol:
        add_bridges()
        objs = [o for o in bpy.data.objects if o.name.startswith("MASS_")]
        for o in objs:
            o.select_set(True)
        bpy.context.view_layer.objects.active = objs[0]
        bpy.ops.object.join()
        body = bpy.context.active_object
        body.name, body.data.name = "SCULPT_Body", "ME_SCULPT_Body"
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        body.data.remesh_voxel_size = VOXEL
        bpy.ops.object.voxel_remesh()
        for p in body.data.polygons:
            p.use_smooth = True
        print(f"[BCMA] SCULPT_Body : {len(body.data.vertices)} sommets, {len(body.data.polygons)} faces")
    sc = setup_view(0.9, 4.2)
    L.instructions(NOTE_R)
    return sc


def multires(sol):
    L.reset("SC_Multires")
    bpy.ops.mesh.primitive_cube_add(size=2)
    ob = bpy.context.active_object
    ob.name, ob.data.name = "SCULPT_HeadBase", "ME_SCULPT_HeadBase"
    m = ob.modifiers.new("Subdivision", "SUBSURF")
    m.levels = 3
    bpy.ops.object.modifier_apply(modifier="Subdivision")
    me = ob.data
    co = np.zeros(len(me.vertices) * 3)
    me.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)
    co /= np.linalg.norm(co, axis=1)[:, None]
    co *= np.array((0.8, 0.95, 1.05))                  # crâne un peu ovale
    me.vertices.foreach_set("co", (co * 0.12).ravel())  # tête de 24 cm environ
    me.update()
    ob.location.z = 1.0
    ob.data.materials.append(L.material("MAT_Clay", (0.72, 0.55, 0.45), 0.55))
    if sol:
        mr = ob.modifiers.new("Multires", "MULTIRES")
        for _ in range(5):
            bpy.ops.object.multires_subdivide(modifier="Multires", mode="CATMULL_CLARK")
        mr.levels, mr.sculpt_levels, mr.render_levels = 3, 5, 5
    L.instructions(DECISIONS_A if sol else DECISIONS_Q, "DECISIONS")
    sc = setup_view(1.0, 1.4)
    L.instructions(NOTE_M)
    return sc


def main():
    out = os.path.join(CH, "COMPLETED_EXAMPLES")
    remesh(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch03_03_remesh_starter.blend"))
    sc = remesh(True)
    L.save(os.path.join(out, "ch03_03_remesh_solution.blend"))
    for o in bpy.data.objects:                         # rendu de contrôle en fil de fer + surface
        if o.type == "MESH" and o.name == "SCULPT_Body":
            o.show_wire = True
    sc.render.filepath = os.path.join(out, "ch03_03_remesh_reference.png")
    bpy.ops.render.render(write_still=True)
    multires(False)
    L.save(os.path.join(CH, "STARTER_FILES", "ch03_03_multires_starter.blend"))
    multires(True)
    L.save(os.path.join(out, "COUNTER_EXAMPLES", "ch03_03_multires_nosculpt.blend"))      # Multires bien réglé mais JAMAIS sculpté
    if os.path.exists(os.path.join(out, ".sculpted_with_mcp")):
        print("[BCMA] solution Multires sculptée à la brosse (Blender 5.2 via MCP) conservée : non régénérée")
    else:
        L.save(os.path.join(out, "ch03_03_multires_solution.blend"))                   # repli scripté (sans sculpt)


if __name__ == "__main__":
    L.run(main)
