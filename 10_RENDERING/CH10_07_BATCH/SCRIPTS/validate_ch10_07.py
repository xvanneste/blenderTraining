"""
validate_ch10_07.py — Correcteur « Rendu distribué » (CH10.07).
Usage : … --python-exit-code 1 --python validate_ch10_07.py -- --exercise batch [--debug]
Objets : Cube (animé 1–24), CAM, texte BATCH. Le correcteur :
  1. vérifie la scène : images 1 à 24, Overwrite désactivé et Placeholders activé (réglages sûrs pour une ferme) ;
  2. analyse le texte BATCH : une commande par ligne (les lignes # sont ignorées), chaque ligne doit commencer par « blender », avoir « {BLEND} » comme second mot et n'utiliser que les options
     -b, -o, -F, -s, -e, -a, -x, -t (liste blanche : toute autre option, comme --python-expr, rend le plan refusé et rien n'est exécuté) ; « -o » obligatoire ; au moins 3 commandes ;
  3. EXÉCUTE chaque commande avec le vrai Blender (premier mot remplacé, --factory-startup ajouté, {BLEND} = ce fichier, {OUT} = un dossier temporaire par commande) ;
  4. mesure : pour chaque commande, les images produites sont exactement celles de sa plage -s … -e (aucune hors plage : « -a » doit suivre « -s » et « -e ») ; les plages recouvrent 1 à 24 sans trou ni recouvrement.
Testé avec : Blender 5.3.0.
"""
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402

ALLOWED = {"-b": 0, "-o": 1, "-F": 1, "-s": 1, "-e": 1, "-a": 0, "-x": 1, "-t": 1}
BLENDER = os.path.abspath(bpy.app.binary_path)


def parse_line(line):
    """Renvoie (liste d'arguments, erreur) pour une ligne de commande de la liste blanche."""
    try:
        t = shlex.split(line, posix=True)
    except ValueError as e:
        return None, f"ligne illisible ({e})"
    if len(t) < 3 or os.path.basename(t[0]).lower().replace(".exe", "") != "blender":
        return None, "doit commencer par « blender »"
    if t[1] == "-b" and t[2] == "{BLEND}":
        i = 3
    elif t[1] == "{BLEND}":
        i = 2
    else:
        return None, "le fichier doit être « {BLEND} » juste après « -b » (ou en second mot)"
    args, seen = [], []
    while i < len(t):
        if t[i] not in ALLOWED:
            return None, f"option interdite ou inconnue : « {t[i]} »"
        n = ALLOWED[t[i]]
        if i + n >= len(t) and n > 0:
            return None, f"« {t[i]} » attend une valeur"
        seen.append(t[i])
        args += t[i:i + 1 + n]
        i += 1 + n
    if "-o" not in seen:
        return None, "« -o » manque (sinon l'image est écrite à côté du fichier)"
    return args, None


def main():
    debug = L.flag("--debug")
    r = L.Report("CH10.07 — Rendu distribué")
    sc = bpy.context.scene
    txt = bpy.data.texts.get("BATCH")
    if not r.check(txt is not None and bpy.data.objects.get("Cube") is not None, "Texte BATCH et Cube présents", "Partez du fichier de départ.", 2):
        return r.finish()
    r.check(sc.frame_start == 1 and sc.frame_end == 24, f"Plage de la scène : {sc.frame_start}–{sc.frame_end} (1–24)", "Ne changez pas la plage.", 3)
    r.check(sc.render.use_overwrite is False and sc.render.use_placeholder is True, f"Réglages de ferme : Overwrite {'activé' if sc.render.use_overwrite else 'désactivé'}, Placeholders {'activé' if sc.render.use_placeholder else 'désactivé'}", "Output Properties > Output : Overwrite désactivé, Placeholders activé.", 6)
    lines = [l.strip() for l in txt.as_string().splitlines() if l.strip() and not l.strip().startswith("#")]
    cmds, errs = [], []
    for l in lines:
        a, e = parse_line(l)
        if e:
            errs.append(f"{l[:48]}… : {e}")
        else:
            cmds.append(a)
    r.check(not errs and len(cmds) >= 3, f"Plan : {len(cmds)} commande(s) valides" + (f" ; erreurs : {errs[0]}" if errs else ""), "Au moins 3 commandes, options autorisées seulement (-b -o -F -s -e -a -x -t), « -o » et « {BLEND} » présents.", 8)
    if errs or len(cmds) < 3:
        return r.finish()
    ranges, produced_ok, outside = [], True, []
    base = tempfile.mkdtemp(prefix="bcma_ch1007_")
    blend = bpy.data.filepath
    for k, a in enumerate(cmds):
        out = os.path.join(base, f"c{k}")
        os.makedirs(out)
        argv = [BLENDER, "--factory-startup", "-b", blend] + [x.replace("{OUT}", out) for x in a if x != "-b"]
        # « -b » est déjà placé ; le reste garde l'ordre de l'élève
        subprocess.run(argv, capture_output=True, text=True, timeout=180)
        got = sorted(int(m.group(1)) for f in os.listdir(out) for m in [re.match(r"shot_(\d+)\.png$", f)] if m and os.path.getsize(os.path.join(out, f)) > 0) if os.path.isdir(out) else []
        s = int(a[a.index("-s") + 1]) if "-s" in a else sc.frame_start
        e = int(a[a.index("-e") + 1]) if "-e" in a else sc.frame_end
        ranges.append((s, e))
        want = list(range(s, e + 1))
        if got != want:
            produced_ok = False
            outside.append(f"commande {k + 1} : plage {s}–{e}, images produites {got[:3]}…{got[-2:]} ({len(got)})")
        if debug:
            print("[DEBUG] chunk", k + 1, (s, e), "images", len(got))
    shutil.rmtree(base, ignore_errors=True)
    r.check(produced_ok, "Chaque commande produit exactement les images de sa plage" if produced_ok else "Images hors plage ou manquantes : " + " ; ".join(outside), "« -a » doit venir APRÈS « -s » et « -e » ; sinon toute la scène est rendue.", 10)
    cover = sorted(f for s, e in ranges for f in range(s, e + 1))
    r.check(cover == list(range(1, 25)), f"Les plages couvrent 1–24 sans trou ni recouvrement : {sorted(ranges)}" if cover == list(range(1, 25)) else f"Couverture fausse : {len(cover)} images pour 24 ({sorted(ranges)})", "Trois plages contiguës : 1–8, 9–16, 17–24.", 10)
    return r.finish()


if __name__ == "__main__":
    L.run(main)
