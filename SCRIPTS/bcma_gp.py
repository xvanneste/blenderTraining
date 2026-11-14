"""
bcma_gp.py — Bibliothèque Grease Pencil (v3, Blender 5.x) de l'académie.

Génère par script des dessins Grease Pencil : traits, polygones, cercles, ellipses,
grilles de perspective, volumes de construction, mannequins, cases de storyboard.
Toutes les coordonnées sont en mètres dans le plan X-Z de l'objet (Y = profondeur),
ce qui correspond à la vue de face (Num 1) et à une caméra regardant +Y.

Utilisation (depuis un script de chapitre) :
    import bcma_gp as G
    gp = G.new_object("GP_Sketch", collection)
    ink = G.material(gp, "MAT_GP_Ink", (0.05, 0.05, 0.05))
    lay = G.layer(gp, "LINES")
    G.polyline(lay, [(0, 0), (1, 0), (1, 1)], radius=0.01, mat=ink)

Testé avec : Blender 5.3.0.
"""
import math

import bpy


# ---------------------------------------------------------------------------
# Objet, matériaux, calques
# ---------------------------------------------------------------------------

def new_object(name, col, location=(0, 0, 0)):
    gp = bpy.data.grease_pencils.new(name.replace("GP_", "GPD_"))
    ob = bpy.data.objects.new(name, gp)
    ob.location = location
    col.objects.link(ob)
    return ob


def material(ob, name, color=(0.02, 0.02, 0.02), fill=None, stroke=True):
    """Matériau GP : trait (color) et/ou remplissage (fill). Renvoie l'index de slot."""
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name)
        bpy.data.materials.create_gpencil_data(mat)
    g = mat.grease_pencil
    g.color = (*color, 1.0)
    g.show_stroke = stroke
    if fill is not None:
        g.show_fill = True
        g.fill_color = (*fill, 1.0)
    else:
        g.show_fill = False
    data = ob.data
    for i, m in enumerate(data.materials):
        if m == mat:
            return i
    data.materials.append(mat)
    return len(data.materials) - 1


def layer(ob, name, frame=1):
    """Renvoie le dessin (drawing) de l'image `frame` du calque `name` (créé au besoin)."""
    gp = ob.data
    lay = gp.layers.get(name) if hasattr(gp.layers, "get") else None
    if lay is None:
        lay = next((l for l in gp.layers if l.name == name), None)
    if lay is None:
        lay = gp.layers.new(name)
    fr = next((f for f in lay.frames if f.frame_number == frame), None)
    if fr is None:
        fr = lay.frames.new(frame)
    _DRAWING_OWNER[fr.drawing.as_pointer()] = ob
    return fr.drawing


# ---------------------------------------------------------------------------
# Traits
# ---------------------------------------------------------------------------

def _pt(p):
    """(x, z) ou (x, y, z) -> (x, y, z) dans le plan X-Z."""
    return (p[0], 0.0, p[1]) if len(p) == 2 else tuple(p)


_DRAWING_OWNER = {}


def drawing_owner_materials(drawing):
    ob = _DRAWING_OWNER.get(drawing.as_pointer())
    return ob.data.materials if ob else None


def polyline(drawing, pts, radius=0.008, mat=0, cyclic=False, opacity=1.0, pressure=None):
    """Ajoute un trait passant par les points donnés. pressure : liste de facteurs de rayon."""
    pts = [_pt(p) for p in pts]
    drawing.add_strokes([len(pts)])
    s = drawing.strokes[len(drawing.strokes) - 1]
    s.cyclic = cyclic
    s.material_index = mat
    mats = drawing_owner_materials(drawing)
    if mats and mat < len(mats) and mats[mat] and mats[mat].grease_pencil.show_fill:
        s.fill_opacity = 1.0  # GP v3 : l'opacité de remplissage est portée par chaque trait
    for i, (pt, co) in enumerate(zip(s.points, pts)):
        pt.position = co
        pt.radius = radius * (pressure[i] if pressure else 1.0)
        pt.opacity = opacity
    drawing.tag_positions_changed()  # recalcul des caches (triangulation des remplissages)
    return s


def line(drawing, a, b, radius=0.008, mat=0, segments=2, opacity=1.0):
    a, b = _pt(a), _pt(b)
    pts = [tuple(a[k] + (b[k] - a[k]) * t / (segments - 1) for k in range(3)) for t in range(segments)]
    return polyline(drawing, pts, radius, mat, opacity=opacity)


def ellipse(drawing, center, rx, rz, radius=0.008, mat=0, n=48, angle=0.0, fill_mat=None):
    cx, cz = center
    ca, sa = math.cos(angle), math.sin(angle)
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        x, z = rx * math.cos(t), rz * math.sin(t)
        pts.append((cx + x * ca - z * sa, cz + x * sa + z * ca))
    s = polyline(drawing, pts, radius, mat if fill_mat is None else fill_mat, cyclic=True)
    return s


def circle(drawing, center, r, radius=0.008, mat=0, n=48, fill_mat=None):
    return ellipse(drawing, center, r, r, radius, mat, n, fill_mat=fill_mat)


def hatch_ellipse(drawing, center, rx, rz, spacing=0.05, angle=0.8, radius=0.004, mat=0, opacity=1.0):
    """Hachures parallèles limitées à une ellipse (valeurs d'ombre au trait).
    Note : les remplissages (Fill) de traits créés PAR SCRIPT ne s'affichent pas au rendu en
    mode arrière-plan dans Blender 5.3 (constaté) ; les hachures servent donc aux exemples
    générés. Dans l'interface, l'outil Fill fonctionne normalement."""
    cx, cz = center
    ca, sa = math.cos(angle), math.sin(angle)
    R = max(rx, rz)
    t = -R
    while t <= R:
        pts = []
        for k in range(41):
            u = -R + 2 * R * k / 40
            x, z = cx + t * -sa + u * ca, cz + t * ca + u * sa
            if ((x - cx) / rx) ** 2 + ((z - cz) / rz) ** 2 <= 1.0:
                pts.append((x, z))
        if len(pts) >= 2:
            polyline(drawing, [pts[0], pts[-1]], radius, mat, opacity=opacity)
        t += spacing


def rect(drawing, x0, z0, x1, z1, radius=0.008, mat=0):
    return polyline(drawing, [(x0, z0), (x1, z0), (x1, z1), (x0, z1)], radius, mat, cyclic=True)


def arrow(drawing, a, b, radius=0.008, mat=0, head=0.08):
    line(drawing, a, b, radius, mat)
    ang = math.atan2(b[1] - a[1], b[0] - a[0])
    for d in (2.6, -2.6):
        line(drawing, b, (b[0] + head * math.cos(ang + d), b[1] + head * math.sin(ang + d)), radius, mat)


# ---------------------------------------------------------------------------
# Constructions de dessin
# ---------------------------------------------------------------------------

def perspective_grid(drawing, horizon_z, vps, x_range=(-3, 3), n_rays=12, radius=0.003, mat=0, fan=4.0):
    """Ligne d'horizon + faisceaux de lignes de fuite vers chaque point de fuite (x)."""
    line(drawing, (x_range[0] - 2, horizon_z), (x_range[1] + 2, horizon_z), radius * 1.5, mat)
    for vx in vps:
        base = -math.pi / 2 if vx <= 0 else math.pi / 2  # les fuyantes partent vers le centre
        for i in range(n_rays):
            a = base + math.pi * (i + 0.5) / n_rays
            end = (vx + fan * math.cos(a) * 2, horizon_z + fan * math.sin(a))
            line(drawing, (vx, horizon_z), end, radius, mat, opacity=0.5)
        circle(drawing, (vx, horizon_z), 0.04, radius * 2, mat, n=16)


def box_two_point(drawing, base_x, base_z, h, w_left, w_right, vp_l, vp_r, horizon_z, radius=0.008, mat=0):
    """Boîte en perspective à 2 points de fuite (arête verticale avant en base_x)."""
    def toward(p, vp_x, frac):
        return (p[0] + (vp_x - p[0]) * frac, p[1] + (horizon_z - p[1]) * frac)
    f_bot, f_top = (base_x, base_z), (base_x, base_z + h)
    l_bot, l_top = toward(f_bot, vp_l, w_left), toward(f_top, vp_l, w_left)
    r_bot, r_top = toward(f_bot, vp_r, w_right), toward(f_top, vp_r, w_right)
    for a, b in [(f_bot, f_top), (f_bot, l_bot), (f_top, l_top), (f_bot, r_bot), (f_top, r_top),
                 (l_bot, l_top), (r_bot, r_top)]:
        line(drawing, a, b, radius, mat)
    # coin arrière du dessus = intersection des fuyantes (l_top -> PF droit) et (r_top -> PF gauche)
    def inter(p1, p2, p3, p4):
        x1, y1 = p1; x2, y2 = p2; x3, y3 = p3; x4, y4 = p4
        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if abs(den) < 1e-9:
            return (l_top[0] + r_top[0] - f_top[0], l_top[1] + r_top[1] - f_top[1])
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))
    back = inter(l_top, (vp_r, horizon_z), r_top, (vp_l, horizon_z))
    line(drawing, l_top, back, radius * 0.7, mat)
    line(drawing, r_top, back, radius * 0.7, mat)


def cylinder_sketch(drawing, cx, cz, rx, rz, h, radius=0.008, mat=0):
    ellipse(drawing, (cx, cz + h), rx, rz, radius, mat)
    # demi-ellipse basse visible
    pts = [(cx + rx * math.cos(t), cz + rz * math.sin(t)) for t in [math.pi + math.pi * i / 24 for i in range(25)]]
    polyline(drawing, pts, radius, mat)
    line(drawing, (cx - rx, cz), (cx - rx, cz + h), radius, mat)
    line(drawing, (cx + rx, cz), (cx + rx, cz + h), radius, mat)


def mannequin(drawing, x, z, scale=1.0, pose="stand", radius=0.008, mat=0):
    """Mannequin simplifié (tête ovale, cage thoracique, bassin, membres en segments).
    Proportions : ~7,5 têtes de haut. pose : 'stand', 'walk', 'reach', 'sit'."""
    H = scale / 7.5  # une tête
    head_c = (x, z + 7.0 * H)
    ellipse(drawing, head_c, 0.42 * H, 0.52 * H, radius, mat)
    neck = (x, z + 6.4 * H)
    chest_c = (x, z + 5.3 * H)
    ellipse(drawing, chest_c, 0.75 * H, 0.95 * H, radius, mat)
    pelvis_c = (x, z + 3.8 * H)
    ellipse(drawing, pelvis_c, 0.7 * H, 0.45 * H, radius, mat)
    line(drawing, neck, (x, z + 6.25 * H), radius, mat)
    line(drawing, (x, z + 6.25 * H), pelvis_c, radius * 0.6, mat)   # ligne d'action (colonne)
    sh_l, sh_r = (x - 0.8 * H, z + 6.0 * H), (x + 0.8 * H, z + 6.0 * H)
    hip_l, hip_r = (x - 0.45 * H, z + 3.7 * H), (x + 0.45 * H, z + 3.7 * H)
    poses = {
        "stand": dict(el_l=(-1.0, 4.6), wr_l=(-1.1, 3.4), el_r=(1.0, 4.6), wr_r=(1.1, 3.4),
                      kn_l=(-0.5, 1.9), an_l=(-0.5, 0.0), kn_r=(0.5, 1.9), an_r=(0.5, 0.0)),
        "walk": dict(el_l=(-1.1, 4.7), wr_l=(-1.6, 3.7), el_r=(1.0, 4.6), wr_r=(1.5, 3.6),
                     kn_l=(-0.3, 1.9), an_l=(-0.9, 0.1), kn_r=(0.6, 2.0), an_r=(1.0, 0.0)),
        "reach": dict(el_l=(-1.2, 4.7), wr_l=(-1.2, 3.5), el_r=(1.6, 6.6), wr_r=(2.2, 7.6),
                      kn_l=(-0.6, 1.9), an_l=(-0.8, 0.0), kn_r=(0.7, 1.9), an_r=(0.9, 0.0)),
        "sit": dict(el_l=(-1.0, 4.6), wr_l=(-0.6, 3.6), el_r=(1.0, 4.6), wr_r=(0.6, 3.6),
                    kn_l=(-1.1, 3.4), an_l=(-1.1, 1.4), kn_r=(1.1, 3.4), an_r=(1.1, 1.4)),
    }[pose]
    P = {k: (x + v[0] * H, z + v[1] * H) for k, v in poses.items()}
    for a, b in [(sh_l, P["el_l"]), (P["el_l"], P["wr_l"]), (sh_r, P["el_r"]), (P["el_r"], P["wr_r"]),
                 (hip_l, P["kn_l"]), (P["kn_l"], P["an_l"]), (hip_r, P["kn_r"]), (P["kn_r"], P["an_r"]),
                 (sh_l, sh_r)]:
        line(drawing, a, b, radius, mat)
    for j in (P["el_l"], P["el_r"], P["kn_l"], P["kn_r"]):
        circle(drawing, j, 0.12 * H, radius * 0.7, mat, n=12)


def storyboard_page(drawing, cols=3, rows=4, panel_w=1.6, ratio=16 / 9, gap=0.25, note_h=0.35,
                    origin=(0, 0), radius=0.006, mat=0):
    """Planche de storyboard : cases au format `ratio`, espace de notes sous chaque case.
    Renvoie la liste des rectangles (x0, z0, x1, z1) des cases, de gauche à droite, haut en bas."""
    ph = panel_w / ratio
    rects = []
    ox, oz = origin
    for r in range(rows):
        for c in range(cols):
            x0 = ox + c * (panel_w + gap)
            z1 = oz - r * (ph + note_h + gap)
            z0 = z1 - ph
            rect(drawing, x0, z0, x0 + panel_w, z1, radius, mat)
            line(drawing, (x0, z0 - note_h * 0.5), (x0 + panel_w, z0 - note_h * 0.5), radius * 0.4, mat, opacity=0.4)
            rects.append((x0, z0, x0 + panel_w, z1))
    return rects


# ---------------------------------------------------------------------------
# Lecture (correcteurs)
# ---------------------------------------------------------------------------

def layer_stats(ob, name):
    """(nombre d'images clés, nombre total de traits, nombre de points) d'un calque."""
    lay = next((l for l in ob.data.layers if l.name == name), None)
    if lay is None:
        return None
    n_str = n_pts = 0
    for fr in lay.frames:
        d = fr.drawing
        n_str += len(d.strokes)
        n_pts += sum(len(s.points) for s in d.strokes)
    return len(lay.frames), n_str, n_pts


def strokes_bbox(ob, name, frame=None):
    lay = next((l for l in ob.data.layers if l.name == name), None)
    if lay is None:
        return None
    xs, zs = [], []
    for fr in lay.frames:
        if frame is not None and fr.frame_number != frame:
            continue
        for s in fr.drawing.strokes:
            for p in s.points:
                w = ob.matrix_world @ __import__("mathutils").Vector(p.position)
                xs.append(w.x)
                zs.append(w.z)
    if not xs:
        return None
    return min(xs), max(xs), min(zs), max(zs)


# ---------------------------------------------------------------------------
# Feuille de dessin prête à l'emploi (exercices de la phase 18)
# ---------------------------------------------------------------------------

def sheet(name="GP_Practice", width=12.0, height=6.75, guide_layers=("GUIDE",), user_layers=("USER",),
          paper=(0.97, 0.96, 0.93)):
    """Crée : fond « papier » (monde clair, vue Standard), caméra orthographique CAM_Sheet
    cadrant la zone (width × height, centrée sur l'origine, plan X-Z), objet GP `name` avec
    les calques guides (verrouillés) et les calques de l'apprenant (vides, image 1).
    Renvoie (objet GP, caméra, {nom_calque: drawing})."""
    import bcma_lib as L
    col = L.collection("DRAWING")
    ob = new_object(name, col)
    material(ob, "MAT_GP_Ink", (0.02, 0.02, 0.025))
    drawings = {}
    for lname in list(guide_layers) + list(user_layers):
        drawings[lname] = layer(ob, lname)
    for lay in ob.data.layers:
        if lay.name in guide_layers:
            lay.lock = True
            lay.opacity = 0.6
    cam = L.camera("CAM_Sheet", L.collection("CAMERAS"), (0, -10, 0), 50, make_active=True)
    cam.rotation_euler = (math.radians(90), 0, 0)
    cam.data.type = "ORTHO"
    cam.data.ortho_scale = width
    sc = bpy.context.scene
    sc.render.resolution_x = 1920
    sc.render.resolution_y = int(1920 * height / width)
    sc.render.engine = "BLENDER_EEVEE"
    sc.view_settings.view_transform = "Standard"
    L.world(paper, 1.0, "WO_Paper")
    return ob, cam, drawings
