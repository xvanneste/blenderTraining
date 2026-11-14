"""
bcma_create_project.py — Crée l'arborescence standard d'un projet de film (CH00.06).

Fonctionne avec le Python système OU dans Blender. Dans Blender 5.3, crée en plus un
« Blender Project » (dossier .blender_project/project.toml) à la racine.

Usage (Python système) :
  python bcma_create_project.py --root "G:/Films" --name "mon_court" [--sequences 3] [--shots 4]
Usage (Blender, avec projet Blender 5.3) :
  blender -b --factory-startup --python bcma_create_project.py -- --root "G:/Films" --name mon_court

Le script ne supprime ni n'écrase rien : les dossiers existants sont conservés.
Testé avec : Python 3.14 (système) et Blender 5.3.0.
"""
import datetime
import os
import re
import sys

TREE = [
    "00_admin",                      # planning, budget, contrats, notes de production
    "01_preprod/script",             # scénario, versions
    "01_preprod/design",             # concept art, model sheets, color script
    "01_preprod/storyboard",         # planches (Grease Pencil, images)
    "01_preprod/animatic",           # animatique (.blend + vidéos exportées)
    "01_preprod/references",         # images et vidéos de référence (avec licences)
    "02_assets/characters",
    "02_assets/props",
    "02_assets/sets",
    "02_assets/materials",
    "02_assets/textures",
    "02_assets/hdri",
    "02_assets/rigs",
    "04_edit",                       # montage
    "05_sound/dialogue",
    "05_sound/sfx",
    "05_sound/music",
    "06_deliveries",                 # masters, exports finaux
    "99_archive",
]
SHOT_TASKS = ["layout", "anim", "fx", "lighting", "comp", "render"]

README = """# {name}

Projet créé le {date} avec la structure BCMA.

| Dossier | Contenu |
|---|---|
| 00_admin | Planning, budget, notes |
| 01_preprod | Scénario, design, storyboard, animatique, références |
| 02_assets | Personnages, props, décors, matériaux, textures, HDRI, rigs |
| 03_shots/sqNNN/shNNNN/<tâche> | Un dossier par plan et par tâche |
| 04_edit | Montage |
| 05_sound | Dialogues, bruitages, musique |
| 06_deliveries | Livrables finaux |
| 99_archive | Versions archivées |

Nommage : `{name}_sq010_sh0010_anim_v001.blend` · assets : `{name}_chr_<nom>_v001.blend`
Chemins relatifs uniquement (`//`).
"""


def args():
    a = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]

    def opt(n, d=None):
        return a[a.index(n) + 1] if n in a else d
    return opt("--root", "."), opt("--name", "mon_projet"), int(opt("--sequences", "2")), int(opt("--shots", "3"))


def create(root, name, n_seq, n_shots):
    if not re.fullmatch(r"[a-z0-9_]+", name):
        raise SystemExit(f"Nom invalide '{name}' : minuscules, chiffres et _ uniquement.")
    base = os.path.join(root, name)
    made = []
    for d in TREE:
        p = os.path.join(base, *d.split("/"))
        os.makedirs(p, exist_ok=True)
        made.append(p)
    for s in range(1, n_seq + 1):
        for k in range(1, n_shots + 1):
            for t in SHOT_TASKS:
                p = os.path.join(base, "03_shots", f"sq{s * 10:03d}", f"sh{k * 10:04d}", t)
                os.makedirs(p, exist_ok=True)
                made.append(p)
    readme = os.path.join(base, "README.md")
    if not os.path.exists(readme):
        with open(readme, "w", encoding="utf-8") as f:
            f.write(README.format(name=name, date=datetime.date.today().isoformat()))
    return base, made


def blender_project(base, name):
    """Crée un Blender Project 5.3 si on est dans Blender."""
    try:
        import bpy
    except ImportError:
        return False
    if os.path.exists(os.path.join(base, ".blender_project", "project.toml")):
        return True
    bpy.ops.project.new(name=name, directory=base)
    p = bpy.data.project
    if p:
        print(f"[BCMA] Blender Project créé : {p.name} → {p.root_path}")
    return bool(p)


def main():
    root, name, n_seq, n_shots = args()
    base, made = create(root, name, n_seq, n_shots)
    bp = blender_project(base, name)
    print(f"[BCMA] {len(made)} dossiers prêts dans {base}")
    print(f"[BCMA] Blender Project : {'oui' if bp else 'non (lancé hors de Blender)'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
