"""
bcma_system_report.py — Rapport système Blender (CH00.01, leçon L5).

Collecte : version et build de Blender, Python embarqué, système, CPU, RAM,
backend GPU de l'interface, périphériques Cycles (CPU/CUDA/OptiX/HIP/oneAPI),
dossiers de configuration, réglages de sauvegarde. Écrit un rapport Markdown
et un rapport JSON.

Usage — ligne de commande (avec VOS préférences) :
  blender -b --python bcma_system_report.py -- --out "C:/chemin/dossier"
Usage — ligne de commande (préférences d'usine, pour comparer) :
  blender -b --factory-startup --python bcma_system_report.py -- --out "..."
Usage — dans Blender : workspace Scripting > Open > ce fichier > Run Script
  (le rapport est alors écrit dans le dossier de ce script, sous-dossier reports/).

Testé avec : Blender 5.3.0 (Windows 11, RTX 3080).
Le script ne modifie aucune préférence de façon permanente : il ne sauvegarde pas
les préférences (il restaure le type de calcul Cycles qu'il trouve).
"""
import ctypes
import datetime as _dt
import json
import os
import platform
import sys

import bpy


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    out = None
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    return out


def total_ram_gb():
    """RAM physique totale (Windows : GlobalMemoryStatusEx ; sinon sysconf)."""
    try:
        if sys.platform == "win32":
            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                            ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                            ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                            ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                            ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
            st = MEMORYSTATUSEX()
            st.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(st))
            return round(st.ullTotalPhys / 1024 ** 3, 1)
        return round(os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / 1024 ** 3, 1)
    except Exception:
        return None


def cycles_devices():
    """Liste les périphériques visibles pour chaque API de calcul Cycles."""
    result = {}
    addon = bpy.context.preferences.addons.get("cycles")
    if addon is None:
        return {"error": "add-on Cycles non chargé"}
    cp = addon.preferences
    original = cp.compute_device_type
    # L'énumération compute_device_type est dynamique (elle dépend de la plateforme) :
    # on essaie donc chaque API connue et on ignore celles qui n'existent pas.
    for api in ("CUDA", "OPTIX", "HIP", "ONEAPI", "METAL"):
        try:
            cp.compute_device_type = api
            cp.refresh_devices()
            devs = cp.get_devices_for_type(api)
            result[api] = [{"name": d.name, "type": d.type, "use": d.use} for d in devs
                           if d.type == api]
        except Exception as exc:  # API absente sur cette plateforme
            result[api] = {"error": str(exc).splitlines()[-1][:120]}
    try:
        cp.compute_device_type = original
    except Exception:
        pass
    result["_selected_api"] = original
    return result


def collect():
    prefs = bpy.context.preferences
    fp = prefs.filepaths
    sysp = prefs.system
    data = {
        "generated_at": _dt.datetime.now().isoformat(timespec="seconds"),
        "blender": {
            "version": bpy.app.version_string,
            "build_hash": bpy.app.build_hash.decode(),
            "build_date": bpy.app.build_date.decode(),
            "build_branch": bpy.app.build_branch.decode(),
            "binary": bpy.app.binary_path,
            "factory_startup": bpy.app.factory_startup,
            "background": bpy.app.background,
            "online_access": bpy.app.online_access,
        },
        "python": sys.version.split()[0],
        "system": {
            "os": platform.platform(),
            "cpu": platform.processor(),
            "logical_cpus": os.cpu_count(),
            "ram_gb": total_ram_gb(),
        },
        "gpu_ui_backend": getattr(sysp, "gpu_backend", "n/a"),
        "cycles_devices": cycles_devices(),
        "paths": {
            "user_config": bpy.utils.resource_path("USER"),
            "system": bpy.utils.resource_path("SYSTEM"),
            "local": bpy.utils.resource_path("LOCAL"),
            "temp": bpy.app.tempdir,
        },
        "save_settings": {
            "auto_save": fp.use_auto_save_temporary_files,
            "auto_save_minutes": fp.auto_save_time,
            "save_versions": fp.save_version,
            "relative_paths": fp.use_relative_paths,
            "file_compression": fp.use_file_compression,
            "undo_steps": prefs.edit.undo_steps,
        },
        "extensions_repos": [{"name": r.name, "enabled": r.enabled, "remote": r.remote_url}
                             for r in prefs.extensions.repos],
    }
    return data


def checks(data):
    """Diagnostic pédagogique : chaque ligne = (statut, message)."""
    out = []
    ver = bpy.app.version
    out.append(("OK" if ver >= (5, 3, 0) else "ATTENTION",
                f"Version {data['blender']['version']} (cible de l'académie : 5.3)"))
    gpus = [d for api, lst in data["cycles_devices"].items()
            if api in ("CUDA", "OPTIX", "HIP", "ONEAPI", "METAL") and isinstance(lst, list)
            for d in lst]
    if any(d["type"] == "OPTIX" for d in gpus):
        out.append(("OK", "GPU NVIDIA RTX compatible OptiX détecté : utilisez OptiX pour Cycles."))
    elif gpus:
        out.append(("OK", f"GPU compatible Cycles détecté ({gpus[0]['type']})."))
    else:
        out.append(("ATTENTION", "Aucun GPU compatible Cycles : rendu sur CPU uniquement."))
    ram = data["system"]["ram_gb"] or 0
    out.append(("OK" if ram >= 16 else "ATTENTION", f"RAM : {ram} Go (16 Go conseillés, 32+ pour la production)."))
    s = data["save_settings"]
    out.append(("OK" if s["auto_save"] else "ATTENTION",
                f"Auto Save : {'actif' if s['auto_save'] else 'INACTIF'} toutes les {s['auto_save_minutes']} min."))
    out.append(("OK" if s["save_versions"] >= 1 else "ATTENTION",
                f"Versions de sauvegarde (.blend1…) : {s['save_versions']}."))
    if data["blender"]["factory_startup"]:
        out.append(("INFO", "Lancé avec --factory-startup : ce sont les réglages d'usine, pas les vôtres."))
    return out


def to_markdown(data, diag):
    lines = ["# Rapport système BCMA", "",
             f"Généré le {data['generated_at']}", "",
             "## Diagnostic", "", "| Statut | Message |", "|---|---|"]
    lines += [f"| {s} | {m} |" for s, m in diag]
    lines += ["", "## Blender", ""]
    lines += [f"- **{k}** : `{v}`" for k, v in data["blender"].items()]
    lines += [f"- **python** : `{data['python']}`", f"- **gpu_ui_backend** : `{data['gpu_ui_backend']}`",
              "", "## Système", ""]
    lines += [f"- **{k}** : `{v}`" for k, v in data["system"].items()]
    lines += ["", "## Périphériques Cycles", ""]
    for api, lst in data["cycles_devices"].items():
        if api.startswith("_"):
            continue
        if isinstance(lst, list):
            names = ", ".join(d["name"] for d in lst) or "aucun"
            lines.append(f"- **{api}** : {names}")
        else:
            lines.append(f"- **{api}** : {lst.get('error')}")
    lines += [f"- API sélectionnée dans les préférences : `{data['cycles_devices'].get('_selected_api')}`",
              "", "## Dossiers", ""]
    lines += [f"- **{k}** : `{v}`" for k, v in data["paths"].items()]
    lines += ["", "## Sauvegarde", ""]
    lines += [f"- **{k}** : `{v}`" for k, v in data["save_settings"].items()]
    lines += ["", "## Dépôts d'extensions", ""]
    lines += [f"- {r['name']} — activé : {r['enabled']} — {r['remote'] or 'local'}"
              for r in data["extensions_repos"]]
    return "\n".join(lines) + "\n"


def main():
    out_dir = parse_args() or os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
    os.makedirs(out_dir, exist_ok=True)
    data = collect()
    diag = checks(data)
    stamp = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    md_path = os.path.join(out_dir, f"system_report_{stamp}.md")
    js_path = os.path.join(out_dir, f"system_report_{stamp}.json")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(to_markdown(data, diag))
    with open(js_path, "w", encoding="utf-8") as f:
        json.dump({"data": data, "diagnostic": diag}, f, indent=2, ensure_ascii=False)
    for s, m in diag:
        print(f"[BCMA][{s}] {m}")
    print(f"[BCMA] Rapport écrit : {md_path}")
    return md_path


if __name__ == "__main__":
    main()
