"""Finish the trouser hems and make a forward, world-contact walk for the fitted character."""
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Quaternion, Vector

ROOT = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT), str(ROOT.parents[1] / "SCRIPTS")]
import bcma_lib as L
from refit_boots import mask_values
from fit_shoes import smooth
from build_body_uv_rig import select_only

FPS = 24
PERIOD = 28
FRAMES = 96
STRIDE = .93
STANCE = .59
SPEED = STRIDE / PERIOD


def repair_hems(pants):
    for vertex in pants.data.vertices:
        x, y, z = vertex.co
        if not .07 < z < .267 or abs(x) < .050:
            continue
        side = math.copysign(1, x)
        w = 1.0 - smooth((z - .132) / .118)
        cx, cy = .131 * side, .010
        dx, dy = x-cx, y-cy
        length = math.hypot(dx / .042, dy / .075)
        if length > .001:
            inflate = .89 * w
            vertex.co.x += dx * (1/length - 1) * inflate
            vertex.co.y += dy * (1/length - 1) * inflate
    pants.data.update()
    # A broad signed-weight ramp lets the Mask modifier interpolate at the
    # actual cut height, instead of falling back to the midpoint of long edges.
    mask_values(pants, "Coupe textile",
                lambda p: min(1.072-p.z, p.z-(.129+.042*(p.y+.020)), .216-abs(p.x)),
                .24)


def local_rotation(pb, rotations):
    q = Quaternion()
    to_local = pb.bone.matrix_local.to_3x3().inverted()
    for axis, degrees in rotations:
        q = q @ Quaternion(to_local @ Vector(axis), math.radians(degrees))
    pb.rotation_mode = "QUATERNION"
    pb.rotation_quaternion = q


def foot_path(step, shift):
    cycle=(step-shift)/PERIOD
    n=math.floor(cycle)
    phase=cycle-n
    contact=(n*PERIOD+shift)*SPEED + STRIDE*STANCE/2
    if phase<STANCE:
        return -contact, 0.0, 0.0, True
    t=(phase-STANCE)/(1-STANCE)
    travel=t*t*t*(10+t*(-15+6*t))
    lift=.093*math.sin(math.pi*t)**1.55
    pitch=13*math.sin(2*math.pi*t)
    return -(contact+STRIDE*travel), lift, pitch, False


def author_walk(scene, rig):
    scene.frame_set(1)
    rig.animation_data.action = None
    anchors = {s:rig.data.bones["CTRL_Pied_IK."+s].head_local.copy() for s in "LR"}
    sole = {}
    for s in "LR":
        mesh = bpy.data.objects["Chaussure."+s].data
        sole[s] = [(v.co.y-anchors[s].y,v.co.z-anchors[s].z,v.co.z) for v in mesh.vertices]
    rig["Pieds IK"] = 1.0
    rig.update_tag()
    reach = {s: rig.data.bones["CTRL_Pied_IK."+s].head_local.copy() for s in "LR"}
    original_crop = {"L": 0.0, "R": PERIOD/2}
    y_axis, x_axis, z_axis=(0,1,0),(1,0,0),(0,0,1)
    for frame in range(1,FRAMES+2):
        step=frame-1
        phase=math.tau*step/PERIOD
        stride=math.cos(phase)
        sway=math.sin(phase)
        world_root=Vector((.015*sway,-SPEED*step,-.055-.021*math.cos(2*phase-.25)))
        rig.location=world_root
        rig.keyframe_insert("location",frame=frame,group="Trajectoire")
        for s in "LR":
            factor=1 if s=="L" else -1
            goal_y,lift,pitch,in_support=foot_path(step,original_crop[s])
            pb=rig.pose.bones["CTRL_Pied_IK."+s]
            target=reach[s].copy()
            target.y+=goal_y
            target.z+=lift
            if not in_support:
                # The swing shoe can pitch without passing through the floor.
                theta=math.radians(pitch)
                a,b=math.sin(theta),math.cos(theta)-1
                lowest=min(z+a*y+b*dz for y,dz,z in sole[s])
                target.z+=max(0,-lowest)
            delta=target-world_root-reach[s]
            pb.location=pb.bone.matrix_local.to_3x3().inverted()@delta
            local_rotation(pb,[(x_axis,pitch)])
            pb.keyframe_insert("location",frame=frame,group="Appui "+s)
            pb.keyframe_insert("rotation_quaternion",frame=frame,group="Appui "+s)
            rotations={
                "upperarm01."+s:[(y_axis,factor*12.5),(x_axis,factor*-21.5*stride)],
                "lowerarm01."+s:[(x_axis,-(9.0+5.5*(1+factor*stride)))],
                "wrist."+s:[(y_axis,-factor*4.5),(x_axis,-3+4*factor*sway)],
            }
            for name,parts in rotations.items():
                b=rig.pose.bones[name]
                local_rotation(b,parts)
                b.keyframe_insert("rotation_quaternion",frame=frame,group="Bras "+s)
            for n in (2,3,4,5):
                finger=rig.pose.bones.get(f"finger{n}-1.{s}")
                if finger:
                    finger.rotation_mode="XYZ"
                    finger.rotation_euler.x=math.radians(-8)
        for name,rots in {
            "root":[(z_axis,-sway*4.0),(y_axis,-sway*1.8)],
            "spine02":[(z_axis,sway*6.8),(y_axis,sway*2.4)],
            "spine01":[(z_axis,sway*2.8),(x_axis,1.8)],
            "head":[(z_axis,-sway*4.2),(y_axis,-sway*1.8),(x_axis,-1.6)],
        }.items():
            pb=rig.pose.bones[name]
            local_rotation(pb,rots)
            pb.keyframe_insert("rotation_quaternion",frame=frame,group="Bassin et buste")
    rig.animation_data.action.name="Marche avant · appuis au sol"
    scene.frame_start=1
    scene.frame_end=FRAMES
    scene.render.fps=FPS
    scene.render.fps_base=1.0
    scene.timeline_markers.clear()
    for frame in range(1,FRAMES+1,PERIOD//2):
        side="gauche" if (frame-1)%PERIOD==0 else "droit"
        scene.timeline_markers.new("Contact "+side,frame=frame)
    scene.frame_set(1)


def validate_walk(scene, rig):
    targets = {"L": [], "R": []}
    worst_slide=0.0
    max_error=0.0
    min_sole=1.0
    max_support=0.0
    min_any=1.0
    for frame in range(1,FRAMES+1):
        scene.frame_set(frame)
        dg=bpy.context.evaluated_depsgraph_get()
        re=rig.evaluated_get(dg)
        for s in "LR":
            shift=0 if s=="L" else PERIOD/2
            _,_,_,support=foot_path(frame-1,shift)
            shoe=bpy.data.objects["Chaussure."+s].evaluated_get(dg)
            floor=min((shoe.matrix_world @ v.co).z for v in shoe.data.vertices)
            min_any=min(min_any,floor)
            if not support:
                targets[s]=[]
                continue
            target=re.matrix_world @ re.pose.bones["CTRL_Pied_IK."+s].head
            ankle=re.matrix_world @ re.pose.bones["foot."+s].head
            error=(target-ankle).length
            max_error=max(error,max_error)
            min_sole=min(min_sole,floor)
            max_support=max(max_support,floor)
            targets[s].append(ankle)
            worst_slide=max(worst_slide,(ankle-targets[s][0]).length)
    stats={"images":FRAMES,"fps":FPS,"erreur_ik_max_mm":round(max_error*1000,2),
           "glissement_max_appui_mm":round(worst_slide*1000,2),
           "semelle_appui_min_mm":round(min_sole*1000,2),
           "semelle_appui_max_mm":round(max_support*1000,2),
           "semelle_tout_cycle_min_mm":round(min_any*1000,2)}
    print("MARCHE",stats)
    assert max_error<.020,stats
    assert worst_slide<.020,stats
    assert -.001<min_any and -.015<min_sole<.015 and max_support<.020,stats
    scene.frame_set(1)
    return stats


def film_camera(scene,rig):
    old=bpy.data.objects["CAM_Trois_Quarts"]
    studio=old.users_collection[0]
    cam=L.camera("CAM_Marche",studio,make_active=True)
    cam.data.type="ORTHO"
    cam.data.ortho_scale=2.38
    for frame in (1,FRAMES):
        y=-(frame-1)*SPEED
        cam.location=(3.8,y-2.7,1.58)
        direction=Vector((0,y-.09,.94))-cam.location
        cam.rotation_euler=direction.to_track_quat("-Z","Y").to_euler()
        cam.keyframe_insert("location",frame=frame)
    # Match camera translation to the linear forward speed.
    action=cam.animation_data.action
    bag=action.layers[0].strips[0].channelbag(cam.animation_data.action_slot)
    for fc in bag.fcurves:
        for point in fc.keyframe_points:
            point.interpolation="LINEAR"
    scene.frame_set(1)
    for name in ("Key","Fill","Rim"):
        lamp=bpy.data.objects.get(name)
        if not lamp:
            continue
        orig=lamp.location.copy()
        for frame in (1,FRAMES):
            lamp.location=(orig.x,orig.y-(frame-1)*SPEED,orig.z)
            lamp.keyframe_insert("location",frame=frame)
        bag=lamp.animation_data.action.layers[0].strips[0].channelbag(lamp.animation_data.action_slot)
        for fc in bag.fcurves:
            for point in fc.keyframe_points:
                point.interpolation="LINEAR"
    scene.frame_set(1)


def settings(scene):
    scene.render.engine="BLENDER_EEVEE"
    scene.eevee.taa_render_samples=14
    scene.render.resolution_x=832
    scene.render.resolution_y=832
    scene.render.resolution_percentage=100
    scene.render.image_settings.media_type="VIDEO"
    scene.render.ffmpeg.format="MPEG4"
    scene.render.ffmpeg.codec="H264"
    scene.render.ffmpeg.constant_rate_factor="MEDIUM"
    scene.render.ffmpeg.audio_codec="NONE"
    scene.render.filepath="//marche_personnage_"


def main():
    bpy.ops.wm.open_mainfile(filepath=str(ROOT/"personnage_final_pieds_ajustes.blend"))
    scene=bpy.context.scene
    rig=bpy.data.objects["RIG_Personnage_FK"]
    pants=bpy.data.objects["Pantalon droit"]
    repair_hems(pants)
    author_walk(scene,rig)
    stats=validate_walk(scene,rig)
    (ROOT/"verification_marche.json").write_text(json.dumps(stats,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    film_camera(scene,rig)
    settings(scene)
    select_only(rig)
    note=bpy.data.texts.new("LIRE · Marche")
    note.write("Marche avant à 24 i/s. Les pieds IK tiennent une position monde fixe pendant l’appui. Les repères de la chronologie indiquent les contacts. Le scan de contrôle a mesuré les écarts sur chaque image, voir verification_marche.json. La scène précédente est conservée dans un autre fichier.")
    L.save(str(ROOT/"personnage_marche.blend"))
    scene.frame_set(8)
    scene.render.image_settings.media_type="IMAGE"
    scene.render.image_settings.file_format="PNG"
    scene.render.filepath="//marche_apercu.png"
    bpy.ops.render.render(write_still=True)


if __name__=="__main__":
    L.run(main)
