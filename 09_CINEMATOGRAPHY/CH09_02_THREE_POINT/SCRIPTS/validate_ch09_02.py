"""
validate_ch09_02.py — Correcteur « Trois points et variantes » (CH09.02).
Usage : … --python-exit-code 1 --python validate_ch09_02.py -- --exercise three_point [--debug]
Objets : Subject (sphère), CAM, LIGHT_Key, LIGHT_Fill, LIGHT_Rim (lampes de zone). Le correcteur rend lui-même 3 images Cycles (96 × 96, 48 échantillons, EXR linéaire, fichier temporaire) :
  toutes les lampes ; sans la Rim ; sans la Fill ; et lit la luminance de trois zones du sujet : flanc gauche (éclairé), flanc droit (ombre), bande du haut (contre-jour).
  Configuration : Key à gauche devant (x ≤ −1, y < 0), Fill du côté opposé (x ≥ 1), Rim derrière (y ≥ 0,5) et haute (z ≥ 2) ; puissance de la Key au moins 2 fois celle de la Fill ; chaque lampe visée sur le sujet (Track To).
  Mesures : ratio flanc éclairé / flanc d'ombre de 2 à 5 ; la Fill apporte au moins 20 % de la luminance du flanc d'ombre ; la Rim apporte au moins 15 % de la luminance de la bande du haut et au moins 0,02.
Testé avec : Blender 5.3.0.
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402


def render(hide=(), res=96, samples=48):
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.use_denoising = False
    sc.cycles.samples = samples
    sc.render.resolution_x = sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    for n in ("LIGHT_Key", "LIGHT_Fill", "LIGHT_Rim"):
        bpy.data.objects[n].hide_render = n in hide
    sc.render.image_settings.file_format = "OPEN_EXR"
    sc.render.image_settings.color_depth = "32"
    p = os.path.join(tempfile.gettempdir(), "bcma_ch0902_val.exr")
    sc.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    px = np.array(im.pixels[:], np.float32).reshape(res, res, 4)[..., :3].copy()
    bpy.data.images.remove(im)
    return px[..., 0] * 0.2126 + px[..., 1] * 0.7152 + px[..., 2] * 0.0722


def zones(Y):
    c = Y.shape[0] // 2
    return float(Y[c - 8:c + 8, c - 25:c - 10].mean()), float(Y[c - 8:c + 8, c + 10:c + 25].mean()), float(Y[c + 22:c + 27, c - 8:c + 8].mean())


def main():
    debug = L.flag("--debug")
    r = L.Report("CH09.02 — Trois points")
    names = ("Subject", "CAM", "LIGHT_Key", "LIGHT_Fill", "LIGHT_Rim")
    obs = {n: bpy.data.objects.get(n) for n in names}
    if not r.check(all(obs.values()) and all(obs[n].type == "LIGHT" for n in names[2:]), "Subject, CAM et les trois lampes présents", "Partez du fichier de départ.", 2):
        return r.finish()
    k, f, m = (obs[n].matrix_world.translation for n in names[2:])
    r.check(k.x <= -1 and k.y < 0 and f.x >= 1 and m.y >= 0.5 and m.z >= 2, f"Positions : Key ({k.x:.1f}, {k.y:.1f}, {k.z:.1f}) à gauche devant, Fill ({f.x:.1f}, {f.y:.1f}, {f.z:.1f}) à droite, Rim ({m.x:.1f}, {m.y:.1f}, {m.z:.1f}) derrière et haute", "Ne déplacez pas les lampes du fichier de départ.", 5)
    ek, ef, er = (obs[n].data.energy for n in names[2:])
    r.check(ek >= 2 * ef and ef > 0, f"Puissances : Key {ek:.0f} W, Fill {ef:.0f} W (Key ≥ 2 × Fill, Fill > 0), Rim {er:.0f} W", "La Key domine, la Fill déboucle.", 5)
    r.check(all(any(c.type == "TRACK_TO" and c.target for c in obs[n].constraints) for n in names[2:]), "Chaque lampe vise le sujet (Track To)", "Ne retirez pas les contraintes.", 3)
    a = zones(render())
    nr = zones(render(hide=("LIGHT_Rim",)))
    nf = zones(render(hide=("LIGHT_Fill",)))
    ratio = a[0] / max(a[1], 1e-9)
    fillpart = (a[1] - nf[1]) / max(a[1], 1e-9)
    rimpart = (a[2] - nr[2]) / max(a[2], 1e-9)
    r.check(2.0 <= ratio <= 5.0, f"Ratio flanc éclairé / flanc d'ombre : {ratio:.2f} (2 à 5)", "Key 250 W, Fill 35 W : ratio ≈ 2,9.", 8)
    r.check(fillpart >= 0.2, f"La Fill apporte {100 * fillpart:.0f} % de la luminance du flanc d'ombre (≥ 20 %)", "Fill > 0 : elle déboucle l'ombre.", 6)
    r.check(rimpart >= 0.15 and a[2] - nr[2] >= 0.02, f"La Rim apporte {100 * rimpart:.0f} % de la bande du haut (≥ 15 %), soit {a[2] - nr[2]:.3f} (≥ 0,02)", "Rim 300 W : le bord haut se détache.", 8)
    if debug:
        print("[DEBUG] lit/shade/top", [round(v, 4) for v in a], "ratio", round(ratio, 2), "fillpart", round(fillpart, 2), "rimpart", round(rimpart, 2))
    return r.finish()


if __name__ == "__main__":
    L.run(main)
