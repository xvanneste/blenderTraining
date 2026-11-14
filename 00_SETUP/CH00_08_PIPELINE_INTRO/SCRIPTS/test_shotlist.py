"""
test_shotlist.py — Teste SCRIPTS/bcma_shotlist_check.py sur les fichiers du chapitre CH00.08.
Attendu : la solution est VALIDÉE (30 s ± 3), le fichier « broken » est REFUSÉ avec
au moins 6 erreurs. Fonctionne avec le Python système ou Blender (-b --python).
Testé avec : Blender 5.3.0.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "SCRIPTS"))
import bcma_shotlist_check as S  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

CH = os.path.dirname(HERE)
err, n, secs = S.check(os.path.join(CH, "COMPLETED_EXAMPLES", "ch00_08_shotlist_solution.csv"), 24, 30, 3)
assert not err and n == 8 and abs(secs - 30) < 0.01, (err, n, secs)
err2, n2, _ = S.check(os.path.join(CH, "STARTER_FILES", "ch00_08_shotlist_broken.csv"))
print("[BCMA] erreurs détectées dans le fichier cassé :", len(err2))
for e in err2:
    print("   ", e)
assert len(err2) >= 6, err2
print("[BCMA] bcma_shotlist_check : OK")
sys.exit(0)
