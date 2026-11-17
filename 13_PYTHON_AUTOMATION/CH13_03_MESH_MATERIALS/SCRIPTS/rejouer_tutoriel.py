"""Exécute uniquement les blocs Python publiés dans le tutoriel, sur le starter."""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from validate_ch13_03 import main

tutorial = HERE.parent / "TUTORIAL.md"
blocks = re.findall(r"^\x60\x60\x60python\n(.*?)^\x60\x60\x60$", tutorial.read_text(encoding="utf-8"), re.M | re.S)
assert len(blocks) == 3, "Les trois blocs Python du tutoriel sont nécessaires."
scope = {"__name__": "__main__"}
for index, block in enumerate(blocks, start=1):
    exec(compile(block, f"{tutorial.name} (bloc {index})", "exec"), scope)
assert main() == 0, "Le tutoriel doit produire la scène attendue depuis le starter."
