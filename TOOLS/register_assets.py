"""
register_assets.py — Enregistre automatiquement dans ASSET_MANIFEST.json les ressources
GÉNÉRÉES d'un ou plusieurs chapitres (STARTER_FILES, COMPLETED_EXAMPLES, ASSETS, SCRIPTS).

- Les entrées existantes (même local_path) sont mises à jour, pas dupliquées.
- Le statut vaut « generated_and_tested » si le chapitre a des tests passants dans
  TOOLS/last_test_results.json, sinon « generated_untested ».
- Les ressources EXTERNES (téléchargées) ne doivent PAS passer par cet outil : elles
  sont ajoutées à la main avec leur source et leur licence vérifiée.
- Une description personnalisée peut être fournie dans <chapitre>/assets_descriptions.json
  sous la forme {"chemin/relatif/au/chapitre": "description"}.

Usage : python TOOLS/register_assets.py <dossier_chapitre> [...]   |   --all
"""
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "ASSET_MANIFEST.json")
TYPES = {".blend": "blend_scene", ".py": "python_script", ".png": "image_png", ".jpg": "image_jpg",
         ".md": "document", ".json": "data", ".wav": "audio_wav", ".csv": "data", ".txt": "document",
         ".svg": "image_svg", ".mp4": "video", ".exr": "image_exr", ".srt": "subtitles"}
SKIP = {"tests.json", "__pycache__"}


def test_ok(name):
    p = os.path.join(ROOT, "TOOLS", "last_test_results.json")
    if not os.path.exists(p):
        return False
    res = [r["ok"] for r in json.load(open(p, encoding="utf-8"))["results"] if r["chapter"] == name]
    return bool(res) and all(res)


def register(cdir, manifest):
    name = os.path.basename(cdir)
    code = name[:7]  # CHNN_MM
    meta_p = os.path.join(cdir, "chapter.json")
    chapter_code = json.load(open(meta_p, encoding="utf-8"))["code"] if os.path.exists(meta_p) else code.replace("_", ".")
    desc_p = os.path.join(cdir, "assets_descriptions.json")
    descs = json.load(open(desc_p, encoding="utf-8")) if os.path.exists(desc_p) else {}
    status = "generated_and_tested" if test_ok(name) else "generated_untested"
    by_path = {a["local_path"]: a for a in manifest["assets"]}
    n = 0
    for sub in ("STARTER_FILES", "COMPLETED_EXAMPLES", "ASSETS", "SCRIPTS"):
        for f in sorted(glob.glob(os.path.join(cdir, sub, "**", "*"), recursive=True)):
            if os.path.isdir(f) or os.path.basename(f) in SKIP or "__pycache__" in f:
                continue
            rel_ch = os.path.relpath(f, cdir).replace(os.sep, "/")
            rel = os.path.relpath(f, ROOT).replace(os.sep, "/")
            ext = os.path.splitext(f)[1].lower()
            kind = TYPES.get(ext, "file")
            is_script = ext == ".py"
            entry = by_path.get(rel, {})
            if entry and not entry.get("auto_registered", False) and entry.get("id", "").startswith("CH00_01"):
                continue  # entrées rédigées à la main : on ne les écrase pas
            idx = len([a for a in manifest["assets"] if a["id"].startswith(code + "-")]) + 1
            entry.update({
                "id": entry.get("id", f"{code}-{idx:03d}"),
                "name": os.path.basename(f),
                "description": descs.get(rel_ch, entry.get("description") or
                                         f"{'Script' if is_script else 'Fichier'} du chapitre {chapter_code} ({sub.lower()})"),
                "chapter": chapter_code,
                "type": kind,
                "source": "Généré pour l'académie (script de construction du chapitre)" if not is_script
                          else "Écrit pour l'académie",
                "license": "GPL-2.0-or-later (script utilisant l'API Blender)" if is_script
                           else "BCMA — usage personnel libre (contenu original généré)",
                "local_path": rel,
                "version": entry.get("version", "v001"),
                "verification_status": status,
                "auto_registered": True,
            })
            if rel not in by_path:
                manifest["assets"].append(entry)
                by_path[rel] = entry
            n += 1
    print(f"[register] {chapter_code}: {n} ressources ({status})")


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    manifest = json.load(open(MANIFEST, encoding="utf-8"))
    targets = sys.argv[1:]
    if targets == ["--all"]:
        targets = sorted(d for d in glob.glob(os.path.join(ROOT, "*", "CH*")) if os.path.isdir(d))
    for t in targets:
        register(os.path.abspath(t), manifest)
    manifest["updated"] = __import__("time").strftime("%Y-%m-%d")
    with open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write("\n")


if __name__ == "__main__":
    main()
