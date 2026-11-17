"""
validate_ch13_01.py — Correcteur « Python pour artistes » (CH13.01).
Usage : … --python-exit-code 1 --python validate_ch13_01.py -- --exercise python [--debug]
Le fichier contient un texte « exercise.py ». Le correcteur le COMPILE et l'EXÉCUTE (dans Blender : bpy disponible), puis teste chaque fonction avec des cas précis ; chaque appel est limité à 5 s (fil d'exécution séparé) ; une erreur est rapportée sans empêcher les autres tests :
  clamp : clamp(5, 0, 3) = 3 ; clamp(−2, 0, 3) = 0 ; clamp(1, 0, 3) = 1 ; clamp(7.5, 0, 10) = 7.5 ;
  average : [1, 2, 3] → 2.0 ; [10] → 10.0 ; [] → 0.0 (sans erreur) ; [0.5, 1.5] → 1.0 ;
  grid_positions : (2, 2, 3) → [(0,0,0), (3,0,0), (0,3,0), (3,3,0)] ; (3, 1, 1) → [(0,0,0), (1,0,0), (2,0,0)] ; (0, 5, 1) → [] ;
  numbered_names : ("Rock", 3) → Rock_001 à Rock_003 ; ("A", 0) → [] ; ("B", 12) → dernier B_012 ;
  make_cubes : trois positions → trois objets MESH Cube_000, Cube_001, Cube_002 (8 sommets), location = la position (± 1 mm), dans la scène.
Testé avec : Blender 5.3.0.
"""
import os
import sys
import threading
import traceback

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "SCRIPTS"))
import bcma_lib as L  # noqa: E402
import bpy  # noqa: E402


def call(fn, *args, threaded=True):
    """Appelle fn(*args) ; fonctions pures : fil séparé avec 5 s de délai ; fonctions bpy (threaded=False) : fil principal (bpy.context n'existe pas dans un autre fil). Renvoie (valeur, erreur)."""
    box = {}
    if not threaded:
        try:
            return fn(*args), None
        except Exception as e:  # noqa: BLE001
            return None, f"{type(e).__name__} : {e}"

    def run():
        try:
            box["v"] = fn(*args)
        except Exception as e:  # noqa: BLE001
            box["e"] = f"{type(e).__name__} : {e}"
    th = threading.Thread(target=run, daemon=True)
    th.start()
    th.join(5.0)
    if th.is_alive():
        return None, "délai dépassé (5 s) : boucle infinie ?"
    return box.get("v"), box.get("e")


def norm(seq):
    return [tuple(round(float(c), 6) for c in p) for p in seq]


def main():
    debug = L.flag("--debug")
    r = L.Report("CH13.01 — Python pour artistes")
    t = bpy.data.texts.get("exercise.py")
    if not r.check(t is not None, "Texte exercise.py présent", "Partez du fichier de départ.", 2):
        return r.finish()
    ns = {"bpy": bpy, "__name__": "exercise"}
    try:
        exec(compile(t.as_string(), "exercise.py", "exec"), ns)
        syntax = None
    except Exception:  # noqa: BLE001
        syntax = traceback.format_exc().strip().splitlines()[-1]
    if not r.check(syntax is None, "exercise.py s'exécute sans erreur de syntaxe" if syntax is None else f"Erreur dans exercise.py : {syntax}", "Corrigez l'erreur (Run Script dans le Text Editor).", 4):
        return r.finish()

    def have(name):
        return callable(ns.get(name))

    def check_fn(name, cases, label, hint, pts):
        if not have(name):
            r.check(False, f"{label} : fonction {name} absente", hint, pts)
            return
        bad = []
        for args, want in cases:
            v, e = call(ns[name], *args)
            if e:
                bad.append(f"{name}{args} → erreur {e}")
            elif v != want and (not isinstance(want, float) or v is None or abs(v - want) > 1e-9):
                bad.append(f"{name}{args} → {v!r} (attendu {want!r})")
        r.check(not bad, f"{label} : {len(cases)} cas justes" if not bad else f"{label} : {bad[0]}", hint, pts)

    check_fn("clamp", [((5, 0, 3), 3), ((-2, 0, 3), 0), ((1, 0, 3), 1), ((7.5, 0, 10), 7.5)], "clamp", "max(bas, min(haut, valeur)).", 6)
    check_fn("average", [(([1, 2, 3],), 2.0), (([10],), 10.0), (([],), 0.0), (([0.5, 1.5],), 1.0)], "average", "sum(valeurs) / len(valeurs), sauf liste vide : 0.0.", 8)
    if have("grid_positions"):
        cases = [((2, 2, 3), [(0, 0, 0), (3, 0, 0), (0, 3, 0), (3, 3, 0)]), ((3, 1, 1), [(0, 0, 0), (1, 0, 0), (2, 0, 0)]), ((0, 5, 1), [])]
        bad = []
        for args, want in cases:
            v, e = call(ns["grid_positions"], *args)
            if e:
                bad.append(f"grid_positions{args} → erreur {e}")
            else:
                try:
                    if norm(v) != norm(want):
                        bad.append(f"grid_positions{args} → {v!r} (attendu {want!r})")
                except Exception as ex:  # noqa: BLE001
                    bad.append(f"grid_positions{args} → valeur inattendue ({type(ex).__name__}) : {v!r}")
        r.check(not bad, "grid_positions : 3 cas justes" if not bad else f"grid_positions : {bad[0]}", "Deux boucles : y (lent) puis x (rapide) ; (x × spacing, y × spacing, 0.0).", 10)
    else:
        r.check(False, "grid_positions : fonction absente", "Deux boucles imbriquées.", 10)
    check_fn("numbered_names", [(("Rock", 3), ["Rock_001", "Rock_002", "Rock_003"]), (("A", 0), []), (("B", 12), [f"B_{i:03d}" for i in range(1, 13)])], "numbered_names", "f\"{prefix}_{i:03d}\" pour i de 1 à count.", 8)
    if have("make_cubes"):
        before = {o.name for o in bpy.data.objects}
        pos = [(0, 0, 0), (2, 1, 0), (4, 2, 3)]
        v, e = call(ns["make_cubes"], pos, threaded=False)
        new = [o for o in bpy.data.objects if o.name not in before]
        names = sorted(o.name for o in new)
        ok = e is None and names == ["Cube_000", "Cube_001", "Cube_002"] and all(o.type == "MESH" and len(o.data.vertices) == 8 for o in new)
        ok2 = ok and all((bpy.data.objects[f"Cube_{i:03d}"].location - __import__("mathutils").Vector(p)).length < 1e-3 for i, p in enumerate(pos))
        ok3 = ok and v is not None and len(v) == 3 and all(o in new for o in v)
        r.check(ok, f"make_cubes : {len(new)} objet(s) créé(s) : {names}" if e is None else f"make_cubes : erreur {e}", "Un cube de 1 m par position, nommé Cube_000, Cube_001, …", 8)
        r.check(ok2, "make_cubes : chaque cube est à sa position (± 1 mm)", "primitive_cube_add(location=position).", 6)
        r.check(ok3, "make_cubes : la fonction renvoie la liste des trois objets", "return cubes.", 4)
    else:
        r.check(False, "make_cubes : fonction absente", "Une boucle et primitive_cube_add.", 18)
    if debug:
        print("[DEBUG] fonctions :", [n for n in ("clamp", "average", "grid_positions", "numbered_names", "make_cubes") if have(n)])
    return r.finish()


if __name__ == "__main__":
    L.run(main)
