"""
run_all_tests.py — Lanceur de tests de l'académie (découverte automatique).

Chaque chapitre testable possède SCRIPTS/tests.json :
{
  "build": "build_chNN_MM_files.py",              (optionnel)
  "validator": "validate_chNN_MM.py",              (optionnel)
  "cases": [ {"file": "COMPLETED_EXAMPLES/x.blend", "exercise": "ex1",
              "expect": true, "render": false} ],
  "extra": [ {"script": "autre.py", "args": ["--out", "{tmp}"], "file": null} ]
}

Usage (Python système) :
  python TOOLS/run_all_tests.py                    tous les chapitres
  python TOOLS/run_all_tests.py CH01_03 CH01_04    chapitres dont le dossier contient ces textes
  python TOOLS/run_all_tests.py --no-build         sans régénérer les .blend
  python TOOLS/run_all_tests.py --blender "C:/…/blender.exe"
Écrit TOOLS/last_test_results.json. Code de retour 0 si tout passe.
"""
import glob
import json
import os
import subprocess
import sys
import tempfile
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.3\blender.exe"


def run_blender(blender, args, timeout=900):
    cmd = [blender, "-b", "--factory-startup"] + args
    t0 = time.time()
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=timeout)
        return p.returncode, p.stdout + p.stderr, time.time() - t0
    except subprocess.TimeoutExpired:
        return 124, "TIMEOUT", time.time() - t0


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    argv = sys.argv[1:]
    blender = DEFAULT_BLENDER
    if "--blender" in argv:
        blender = argv[argv.index("--blender") + 1]
        argv = [a for a in argv if a not in ("--blender", blender)]
    no_build = "--no-build" in argv
    filters = [a for a in argv if not a.startswith("--")]
    tmp = os.path.join(tempfile.gettempdir(), "bcma_tests")
    os.makedirs(tmp, exist_ok=True)

    specs = sorted(glob.glob(os.path.join(ROOT, "*", "CH*", "SCRIPTS", "tests.json")))
    if filters:
        specs = [s for s in specs if any(f in s for f in filters)]
    results, failures = [], 0
    for spec_path in specs:
        sdir = os.path.dirname(spec_path)
        cdir = os.path.dirname(sdir)
        name = os.path.basename(cdir)
        spec = json.load(open(spec_path, encoding="utf-8"))
        print(f"\n=== {name} ===")

        def record(ok, label, out="", dt=0.0):
            nonlocal failures
            print(f"  [{'PASS' if ok else 'FAIL'}] {label} ({dt:.1f}s)")
            if not ok:
                failures += 1
                tail = "\n".join(out.strip().splitlines()[-15:])
                print("      " + tail.replace("\n", "\n      "))
            results.append({"chapter": name, "test": label, "ok": ok, "seconds": round(dt, 1)})

        if spec.get("build") and not no_build:
            code, out, dt = run_blender(blender, ["--python", os.path.join(sdir, spec["build"]),
                                                  "--python-exit-code", "1"])
            record(code == 0, f"build {spec['build']}", out, dt)
        for case in spec.get("cases", []):
            args = [os.path.join(cdir, case["file"]), "--python", os.path.join(sdir, spec["validator"]),
                    "--python-exit-code", "1", "--", "--exercise", case["exercise"]]
            if case.get("render"):
                args.append("--render")
            code, out, dt = run_blender(blender, args)
            ok = (code == 0) == case["expect"]
            record(ok, f"{case['file']} [{case['exercise']}] attendu "
                       f"{'VALIDÉ' if case['expect'] else 'REFUSÉ'}", out, dt)
        for ex in spec.get("extra", []):
            args = []
            if ex.get("file"):
                args.append(os.path.join(cdir, ex["file"]))
            args += ["--python", os.path.join(sdir, ex["script"]), "--python-exit-code", "1", "--"]
            args += [a.replace("{tmp}", tmp) for a in ex.get("args", [])]
            code, out, dt = run_blender(blender, args)
            record(code == 0, f"script {ex['script']}", out, dt)

    # Fusion avec les résultats précédents : seuls les chapitres testés maintenant sont remplacés.
    res_path = os.path.join(ROOT, "TOOLS", "last_test_results.json")
    previous = []
    if os.path.exists(res_path):
        previous = json.load(open(res_path, encoding="utf-8")).get("results", [])
    tested = {r["chapter"] for r in results}
    for r in results:
        r["date"] = time.strftime("%Y-%m-%d %H:%M")
    merged = [r for r in previous if r["chapter"] not in tested] + results
    with open(res_path, "w", encoding="utf-8") as f:
        json.dump({"date": time.strftime("%Y-%m-%d %H:%M"),
                   "failures": sum(1 for r in merged if not r["ok"]),
                   "results": merged}, f, indent=1, ensure_ascii=False)
    print(f"\n{len(results)} tests, {failures} échec(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
