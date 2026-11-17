"""
build_p4_reference.py — Bibliothèque de RÉFÉRENCE du projet P4 : 25 matériaux procéduraux, publiés comme assets.
Écrit dans 04_MATERIALS/PROJECT_P4/REFERENCE/ :
  p4_library_reference.blend      (25 matériaux MAT_<Catégorie>_<Nom>, assets : description, auteur, licence, 2 tags, catalogue, aperçu)
  blender_assets.cats.txt         (6 catalogues Materials/<Catégorie>)
  renders/p4_contact_sheet.png    (grille 5 x 5 de sphères, 1920 x 1080, EEVEE)
Catégories : Metal 5, Stone 5, Wood 3, Plastic 4, Glass 3, Organic 5.
Usage : blender -b --factory-startup --python-exit-code 1 --python build_p4_reference.py
Testé avec : Blender 5.3.0.
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bcma_shots as S  # noqa: E402
import bpy  # noqa: E402

OUT = os.path.join(HERE, "REFERENCE")
CATS = {"Metal": "6b0d7a10-0000-4000-8000-000000000001", "Stone": "6b0d7a10-0000-4000-8000-000000000002", "Wood": "6b0d7a10-0000-4000-8000-000000000003",
        "Plastic": "6b0d7a10-0000-4000-8000-000000000004", "Glass": "6b0d7a10-0000-4000-8000-000000000005", "Organic": "6b0d7a10-0000-4000-8000-000000000006"}


class M:
    """Petit constructeur de matériau."""

    def __init__(self, cat, name, desc, tags):
        self.cat, self.name, self.desc, self.tags = cat, name, desc, tags
        self.mat = bpy.data.materials.new(f"MAT_{cat}_{name}")
        self.nt = self.mat.node_tree
        self.b = self.nt.nodes["Principled BSDF"]
        self.tc = None
        self.x = -900

    def set(self, **kw):
        for k, v in kw.items():
            key = k.replace("_", " ")
            if isinstance(v, tuple) and len(v) == 3 and key in ("Base Color", "Emission Color", "Sheen Tint", "Coat Tint"):
                v = (*v, 1.0)
            self.b.inputs[key].default_value = v
        return self

    def coord(self):
        if self.tc is None:
            self.tc = self.nt.nodes.new("ShaderNodeTexCoord")
            self.tc.location = (-1100, 0)
        return self.tc

    def node(self, kind, y=0, **props):
        n = self.nt.nodes.new(kind)
        n.location = (self.x, y)
        self.x += 220
        for k, v in props.items():
            setattr(n, k, v)
        return n

    def link(self, a, b):
        self.nt.links.new(a, b)

    def ramp(self, a, b, pa=0.35, pb=0.65, y=0):
        r = self.node("ShaderNodeValToRGB", y)
        r.color_ramp.elements[0].position = pa
        r.color_ramp.elements[0].color = (*a, 1)
        r.color_ramp.elements[1].position = pb
        r.color_ramp.elements[1].color = (*b, 1)
        return r

    def noise_color(self, c1, c2, scale=5.0, detail=6.0, pa=0.35, pb=0.65, vec=None):
        nz = self.node("ShaderNodeTexNoise", 100)
        nz.inputs["Scale"].default_value = scale
        nz.inputs["Detail"].default_value = detail
        self.link(self.coord().outputs["Object"], nz.inputs["Vector"] if vec is None else vec)
        r = self.ramp(c1, c2, pa, pb, 100)
        self.link(nz.outputs["Fac"], r.inputs["Fac"])
        self.link(r.outputs["Color"], self.b.inputs["Base Color"])
        return nz, r

    def noise_bump(self, scale=40.0, strength=0.3, detail=6.0):
        nz = self.node("ShaderNodeTexNoise", -250)
        nz.inputs["Scale"].default_value = scale
        nz.inputs["Detail"].default_value = detail
        self.link(self.coord().outputs["Object"], nz.inputs["Vector"])
        bp = self.node("ShaderNodeBump", -250)
        bp.inputs["Strength"].default_value = strength
        self.link(nz.outputs["Fac"], bp.inputs["Height"])
        self.link(bp.outputs["Normal"], self.b.inputs["Normal"])
        return nz

    def rough_from(self, nz, lo, hi):
        mr = self.node("ShaderNodeMapRange", -450)
        mr.inputs["To Min"].default_value = lo
        mr.inputs["To Max"].default_value = hi
        self.link(nz.outputs["Fac"], mr.inputs["Value"])
        self.link(mr.outputs["Result"], self.b.inputs["Roughness"])


def library():
    mats = []

    def new(cat, name, desc, tags):
        m = M(cat, name, desc, tags)
        mats.append(m)
        return m
    # ---- Metal ----
    m = new("Metal", "Gold", "Or poli", ("métal", "précieux"))
    m.set(Base_Color=(1.0, 0.77, 0.34), Metallic=1.0, Roughness=0.25)
    m = new("Metal", "Copper", "Cuivre légèrement oxydé", ("métal", "cuivre"))
    m.set(Base_Color=(0.95, 0.64, 0.54), Metallic=1.0)
    nz = m.noise_bump(60.0, 0.05)
    m.rough_from(nz, 0.25, 0.4)
    m = new("Metal", "BrushedSteel", "Acier brossé anisotrope", ("métal", "acier", "brossé"))
    m.set(Base_Color=(0.75, 0.76, 0.78), Metallic=1.0, Anisotropic=0.6)
    mp = m.node("ShaderNodeMapping", -450)
    mp.inputs["Scale"].default_value = (1.0, 60.0, 1.0)
    m.link(m.coord().outputs["Object"], mp.inputs["Vector"])
    nz = m.node("ShaderNodeTexNoise", -450)
    nz.inputs["Scale"].default_value = 8.0
    m.link(mp.outputs["Vector"], nz.inputs["Vector"])
    m.rough_from(nz, 0.2, 0.45)
    m = new("Metal", "AnodizedBlue", "Aluminium anodisé bleu", ("métal", "aluminium"))
    m.set(Base_Color=(0.40, 0.55, 0.80), Metallic=1.0, Roughness=0.4)
    m.noise_bump(120.0, 0.1)
    m = new("Metal", "RustyIron", "Fer rouillé (acier + rouille par masque)", ("métal", "rouille", "usé"))
    m.set(Roughness=0.7)
    nz = m.node("ShaderNodeTexNoise", 100)
    nz.inputs["Scale"].default_value = 6.0
    nz.inputs["Detail"].default_value = 8.0
    m.link(m.coord().outputs["Object"], nz.inputs["Vector"])
    cr = m.ramp((1, 1, 1), (0, 0, 0), 0.45, 0.62, 100)
    m.link(nz.outputs["Fac"], cr.inputs["Fac"])
    mx = m.node("ShaderNodeMix", 100)
    mx.data_type = "RGBA"
    next(i for i in mx.inputs if i.identifier == "A_Color").default_value = (0.45, 0.15, 0.05, 1)
    next(i for i in mx.inputs if i.identifier == "B_Color").default_value = (0.50, 0.52, 0.55, 1)
    m.link(cr.outputs["Color"], next(i for i in mx.inputs if i.identifier == "Factor_Float"))
    m.link(next(o for o in mx.outputs if o.identifier == "Result_Color"), m.b.inputs["Base Color"])
    m.link(cr.outputs["Color"], m.b.inputs["Metallic"])
    # ---- Stone ----
    m = new("Stone", "Granite", "Granit moucheté", ("pierre", "granit"))
    m.set(Roughness=0.55)
    m.noise_color((0.15, 0.15, 0.16), (0.65, 0.63, 0.60), 60.0, 3.0, 0.4, 0.6)
    m.noise_bump(80.0, 0.15)
    m = new("Stone", "Marble", "Marbre blanc veiné", ("pierre", "marbre"))
    m.set(Roughness=0.2)
    wv = m.node("ShaderNodeTexWave", 100)
    wv.wave_type = "BANDS"
    wv.inputs["Scale"].default_value = 3.0
    wv.inputs["Distortion"].default_value = 8.0
    wv.inputs["Detail"].default_value = 4.0
    m.link(m.coord().outputs["Object"], wv.inputs["Vector"])
    r = m.ramp((0.55, 0.56, 0.58), (0.88, 0.88, 0.86), 0.35, 0.6, 100)
    m.link(wv.outputs["Fac"], r.inputs["Fac"])
    m.link(r.outputs["Color"], m.b.inputs["Base Color"])
    m = new("Stone", "Brick", "Mur de briques", ("pierre", "brique", "mur"))
    m.set(Roughness=0.8)
    br = m.node("ShaderNodeTexBrick", 100)
    br.offset = 0.5
    br.inputs["Scale"].default_value = 3.0
    br.inputs["Mortar Size"].default_value = 0.03
    br.inputs["Color1"].default_value = (0.35, 0.10, 0.06, 1)
    br.inputs["Color2"].default_value = (0.22, 0.07, 0.05, 1)
    br.inputs["Mortar"].default_value = (0.55, 0.52, 0.47, 1)
    m.link(m.coord().outputs["Object"], br.inputs["Vector"])
    m.link(br.outputs["Color"], m.b.inputs["Base Color"])
    bp = m.node("ShaderNodeBump", -250)
    bp.inputs["Strength"].default_value = 0.8
    m.link(br.outputs["Fac"], bp.inputs["Height"])
    m.link(bp.outputs["Normal"], m.b.inputs["Normal"])
    m = new("Stone", "Concrete", "Béton brut", ("pierre", "béton"))
    m.set(Roughness=0.9)
    m.noise_color((0.30, 0.30, 0.30), (0.50, 0.50, 0.49), 8.0, 8.0, 0.3, 0.7)
    m.noise_bump(60.0, 0.25)
    m = new("Stone", "Cobblestone", "Pavés irréguliers", ("pierre", "pavé", "sol"))
    m.set(Roughness=0.8)
    vr = m.node("ShaderNodeTexVoronoi", 100)
    vr.inputs["Scale"].default_value = 5.0
    m.link(m.coord().outputs["Object"], vr.inputs["Vector"])
    r = m.ramp((0.12, 0.12, 0.12), (0.50, 0.48, 0.45), 0.05, 0.5, 100)
    m.link(vr.outputs["Distance"], r.inputs["Fac"])
    m.link(r.outputs["Color"], m.b.inputs["Base Color"])
    bp = m.node("ShaderNodeBump", -250)
    bp.inputs["Strength"].default_value = 1.0
    m.link(vr.outputs["Distance"], bp.inputs["Height"])
    m.link(bp.outputs["Normal"], m.b.inputs["Normal"])
    # ---- Wood ----
    def wood(name, desc, c1, c2, rough, scale=6.0):
        m = new("Wood", name, desc, ("bois", name.lower()))
        m.set(Roughness=rough)
        mp = m.node("ShaderNodeMapping", 100)
        mp.inputs["Scale"].default_value = (1.0, 1.0, 0.15)
        m.link(m.coord().outputs["Object"], mp.inputs["Vector"])
        wv = m.node("ShaderNodeTexWave", 100)
        wv.wave_type = "BANDS"
        wv.inputs["Scale"].default_value = scale
        wv.inputs["Distortion"].default_value = 4.0
        wv.inputs["Detail"].default_value = 3.0
        m.link(mp.outputs["Vector"], wv.inputs["Vector"])
        r = m.ramp(c1, c2, 0.2, 0.8, 100)
        m.link(wv.outputs["Fac"], r.inputs["Fac"])
        m.link(r.outputs["Color"], m.b.inputs["Base Color"])
    wood("Oak", "Chêne clair", (0.30, 0.17, 0.08), (0.62, 0.42, 0.22), 0.45)
    wood("Walnut", "Noyer sombre", (0.10, 0.05, 0.03), (0.28, 0.15, 0.08), 0.4)
    wood("Plywood", "Contreplaqué clair", (0.55, 0.40, 0.22), (0.75, 0.58, 0.35), 0.6, 14.0)
    # ---- Plastic ----
    m = new("Plastic", "RedGloss", "Plastique rouge verni", ("plastique", "rouge"))
    m.set(Base_Color=(0.80, 0.05, 0.04), Roughness=0.3, Coat_Weight=0.5)
    m = new("Plastic", "BlackRubber", "Caoutchouc noir", ("caoutchouc", "noir"))
    m.set(Base_Color=(0.05, 0.05, 0.05), Roughness=0.75)
    m.noise_bump(150.0, 0.08)
    m = new("Plastic", "WhiteABS", "ABS blanc cassé", ("plastique", "blanc"))
    m.set(Base_Color=(0.80, 0.80, 0.78), Roughness=0.35)
    m = new("Plastic", "Wax", "Cire translucide", ("cire", "translucide"))
    m.set(Base_Color=(0.85, 0.70, 0.48), Roughness=0.45, Subsurface_Weight=0.6, Subsurface_Radius=(1.0, 0.5, 0.25), Subsurface_Scale=0.05, Coat_Weight=0.2)
    # ---- Glass ----
    m = new("Glass", "Clear", "Verre clair", ("verre", "transparent"))
    m.set(Base_Color=(1, 1, 1), Roughness=0.02, Transmission_Weight=1.0, IOR=1.5)
    m = new("Glass", "Frosted", "Verre dépoli", ("verre", "dépoli"))
    m.set(Base_Color=(1, 1, 1), Roughness=0.35, Transmission_Weight=1.0, IOR=1.5)
    m = new("Glass", "GreenTint", "Verre teinté vert", ("verre", "vert"))
    m.set(Base_Color=(0.5, 0.9, 0.6), Roughness=0.03, Transmission_Weight=1.0, IOR=1.52)
    # ---- Organic ----
    m = new("Organic", "Skin", "Peau avec sous-surface et pores", ("peau", "personnage"))
    m.set(Base_Color=(0.65, 0.42, 0.34), Roughness=0.45, Subsurface_Weight=1.0, Subsurface_Radius=(1.0, 0.2, 0.1), Subsurface_Scale=0.05)
    m.noise_bump(250.0, 0.15, 3.0)
    m = new("Organic", "Cotton", "Coton avec trame", ("tissu", "coton"))
    m.set(Base_Color=(0.75, 0.72, 0.65), Roughness=0.85, Sheen_Weight=0.4)
    wv = m.node("ShaderNodeTexWave", -250)
    wv.wave_type = "BANDS"
    wv.inputs["Scale"].default_value = 120.0
    wv.inputs["Distortion"].default_value = 0.0
    m.link(m.coord().outputs["Object"], wv.inputs["Vector"])
    bp = m.node("ShaderNodeBump", -250)
    bp.inputs["Strength"].default_value = 0.4
    m.link(wv.outputs["Fac"], bp.inputs["Height"])
    m.link(bp.outputs["Normal"], m.b.inputs["Normal"])
    m = new("Organic", "Leather", "Cuir brun grené", ("cuir", "brun"))
    m.set(Base_Color=(0.22, 0.10, 0.05), Roughness=0.5)
    vr = m.node("ShaderNodeTexVoronoi", -250)
    vr.inputs["Scale"].default_value = 60.0
    m.link(m.coord().outputs["Object"], vr.inputs["Vector"])
    bp = m.node("ShaderNodeBump", -250)
    bp.inputs["Strength"].default_value = 0.5
    m.link(vr.outputs["Distance"], bp.inputs["Height"])
    m.link(bp.outputs["Normal"], m.b.inputs["Normal"])
    m = new("Organic", "Velvet", "Velours bordeaux", ("tissu", "velours"))
    m.set(Base_Color=(0.30, 0.04, 0.08), Roughness=0.9, Sheen_Weight=1.0, Sheen_Roughness=0.35)
    m.noise_bump(200.0, 0.15, 2.0)
    m = new("Organic", "Paper", "Papier blanc cassé", ("papier", "clair"))
    m.set(Base_Color=(0.80, 0.78, 0.72), Roughness=0.9)
    m.noise_bump(300.0, 0.1, 2.0)
    return mats


def write_catalogs(folder):
    lines = ["# This is an Asset Catalog Definition file for Blender.", "#",
             "# Empty lines and lines starting with `#` will be ignored.",
             "# The first non-ignored line should be the version indicator.",
             '# Other lines are of the format "UUID:catalog/path/for/assets:simple catalog name"', "", "VERSION 1", ""]
    for name, uid in CATS.items():
        lines.append(f"{uid}:Materials/{name}:Materials-{name}")
    with open(os.path.join(folder, "blender_assets.cats.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")


def build():
    L.reset("SC_P4")
    L.studio(subject_height=1.0)
    L.world((0.30, 0.33, 0.38), 1.0)
    c = L.collection("CAMERAS")
    cam = L.camera("CAM_Sheet", c, (0, -16.0, 3.0), 50, make_active=True)
    S.look_at(cam, (0, 0, 2.8))
    sc = L.render_defaults("BLENDER_EEVEE", 50)
    sc.camera = cam
    sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
    sc.render.resolution_percentage = 100
    mats = library()
    for i, m in enumerate(mats):
        r, col = divmod(i, 5)
        ob = L.sphere(f"SPH_{m.cat}_{m.name}", L.collection("OBJETS"), None, radius=0.5, location=((col - 2) * 1.5, 0, (4 - r) * 1.15 + 0.5), segments=48, ring_count=24)
        ob.data.materials.append(m.mat)
        m.mat.asset_mark()
        a = m.mat.asset_data
        a.description = m.desc
        a.author = "Blender Cinema Master Academy"
        a.license = "BCMA (usage personnel de formation)"
        a.catalog_id = CATS[m.cat]
        for t in m.tags:
            a.tags.new(t)
    for m in mats:
        m.mat.asset_generate_preview()
    return mats


def main():
    os.makedirs(os.path.join(OUT, "renders"), exist_ok=True)
    build()
    L.save(os.path.join(OUT, "p4_library_reference.blend"))
    write_catalogs(OUT)
    bpy.context.scene.render.filepath = os.path.join(OUT, "renders", "p4_contact_sheet.png")
    bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    L.run(main)
