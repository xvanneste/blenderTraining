"""
validate_ch03_02.py — Correcteur « Premier sculpt : un visage simple » (CH03.02).
Usage : … --python validate_ch03_02.py --python-exit-code 1 -- --exercise face [--render]
Compare chaque sommet de SCULPT_Head à sa position d'origine (attribut « bcma_orig ») :
déplacement le long de la normale d'origine. Vérifie : topologie conservée (pas de remesh), nez en
relief, deux orbites creusées, symétrie X, arrière du crâne masqué (.sculpt_mask) ET intact, ≥ 2 Face
Sets (.sculpt_face_set), absence de pics.
Testé avec : Blender 5.3.0.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402
import numpy as np  # noqa: E402

NOSE = np.array((0.0, -0.99, -0.08))
EYES = [np.array((0.33, -0.88, 0.17)), np.array((-0.33, -0.88, 0.17))]


def unit(v):
    return v / np.linalg.norm(v)


def main():
    r = L.Report("CH03.02 — Premier sculpt : un visage simple")
    ob = bpy.data.objects.get("SCULPT_Head")
    if not r.check(ob is not None and ob.type == "MESH", "Objet SCULPT_Head présent", "Repartez du starter.", 1):
        return r.finish()
    me = ob.data
    orig_a = me.attributes.get("bcma_orig")
    if not r.check(orig_a is not None and len(orig_a.data) == len(me.vertices),
                   f"Topologie d'origine conservée ({len(me.vertices)} sommets)",
                   "Pas de DynTopo ni de Remesh dans ce chapitre (CH03.03) : repartez du starter.", 3):
        return r.finish()
    n = len(me.vertices)
    orig = np.zeros(n * 3)
    orig_a.data.foreach_get("vector", orig)
    orig = orig.reshape(-1, 3)
    co = np.zeros(n * 3)
    me.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)
    nrm = orig / np.linalg.norm(orig, axis=1)[:, None]
    disp = np.einsum("ij,ij->i", co - orig, nrm)
    moved = np.mean(np.abs(disp) > 0.005)
    r.check(moved >= 0.03, f"Surface sculptée ({100 * moved:.1f} % des sommets déplacés de plus de 5 mm)", "Sculptez !", 1)

    def cone(v, ang=0.22):
        return np.einsum("ij,j->i", nrm, unit(v)) > np.cos(ang)

    nose = disp[cone(NOSE)].max() if cone(NOSE).any() else 0
    r.check(nose >= 0.06, f"Nez en relief ({nose * 100:.1f} cm, ≥ 6)", "Draw / Clay Strips au centre du visage (face −Y).", 3)
    eyes = [disp[cone(e)].min() for e in EYES]
    r.check(all(e <= -0.02 for e in eyes), f"Deux orbites creusées ({eyes[0] * 100:.1f} et {eyes[1] * 100:.1f} cm, ≤ −2)",
            "Ctrl + Draw pour creuser, de part et d'autre du nez.", 3)
    # symétrie : sommet miroir (x → −x) trouvé par grille de positions d'origine arrondies
    key = {tuple(np.round(p, 4)): i for i, p in enumerate(orig)}
    diffs = []
    for i, p in enumerate(orig):
        if p[1] < -0.2 and abs(disp[i]) > 0.002:
            j = key.get((round(-p[0], 4) + 0.0, round(p[1], 4), round(p[2], 4)))
            if j is not None:
                diffs.append(abs(disp[i] - disp[j]))
    sym = np.mean(np.array(diffs) <= 0.01) if diffs else 0
    r.check(sym >= 0.95, f"Symétrie gauche/droite ({100 * sym:.0f} % des sommets sculptés symétriques à 1 cm)",
            "Activez Mirror X dans l'en-tête avant de sculpter (ou Symmetrize).", 3)
    mask_a = me.attributes.get(".sculpt_mask")
    back = orig[:, 1] > 0.3
    if mask_a is not None:
        mask = np.zeros(n)
        mask_a.data.foreach_get("value", mask)
    else:
        mask = np.zeros(n)
    r.check(mask[back].mean() >= 0.8 and mask[orig[:, 1] < -0.5].mean() <= 0.3,
            f"Arrière du crâne masqué (masque moyen : arrière {mask[back].mean():.2f}, visage {mask[orig[:, 1] < -0.5].mean():.2f})",
            "Brosse Mask (M) ou B sur l'arrière ; le visage doit rester libre.", 2)
    r.check(np.abs(disp[back]).max() <= 0.003, f"Zone masquée intacte (déplacement max {np.abs(disp[back]).max() * 1000:.1f} mm)",
            "Masquez AVANT de sculpter.", 2)
    fs = me.attributes.get(".sculpt_face_set")
    nfs = 0
    if fs is not None:
        v = np.zeros(len(me.polygons), dtype=np.int32)
        fs.data.foreach_get("value", v)
        nfs = len(set(v.tolist()))
    r.check(nfs >= 2, f"{nfs} Face Set(s) (≥ 2)", "Face Set Paint ou Face Sets > Initialize Face Sets.", 2)
    r.check(np.abs(disp).max() <= 0.35, f"Pas de pic aberrant (déplacement max {np.abs(disp).max() * 100:.1f} cm)", "Lissez (Shift).", 1)
    r.check(me.use_mirror_x, "Mirror X activé sur le maillage", "En-tête du Sculpt Mode : Mirror X.", 1)
    if L.flag("--render"):
        lum = L.quick_render(15, 4)
        r.check(lum > 0.05, f"Rendu de contrôle non noir ({lum:.3f})", "", 1)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
