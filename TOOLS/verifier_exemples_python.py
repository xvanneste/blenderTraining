"""Analyse les blocs Python du cours et compare leurs opérateurs à l’API Blender chargée."""
import ast
import re
import sys
from pathlib import Path

import bpy

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.dont_write_bytecode = True
from academy_status import PHASE_DIRS, curriculum_chapters

FENCE = chr(96) * 3
START = re.compile(r"^\s*" + FENCE + r"(?:python|py)\s*$", re.I)


def blocks(text):
    start = None
    source = []
    for number, line in enumerate(text.splitlines(), start=1):
        if start is None:
            if START.match(line):
                start = number + 1
                source = []
            continue
        if line.strip().startswith(FENCE):
            yield start, "\n".join(source)
            start = None
        else:
            source.append(line)


def operator_name(expr):
    names = []
    while isinstance(expr, ast.Attribute):
        names.append(expr.attr)
        expr = expr.value
    if isinstance(expr, ast.Name) and expr.id == "bpy":
        names.reverse()
        if len(names) == 3 and names[0] == "ops":
            return names[1], names[2]
    return None


def inspect_file(path):
    results = []
    n_blocks = n_operators = 0
    rel = path.relative_to(ROOT)
    for first, source in blocks(path.read_text(encoding="utf-8-sig")):
        n_blocks += 1
        try:
            tree = ast.parse(source, filename=str(rel))
        except SyntaxError as err:
            results.append((rel, first + (err.lineno or 1) - 1, err.msg))
            continue
        for call in (node for node in ast.walk(tree) if isinstance(node, ast.Call)):
            name = operator_name(call.func)
            if not name:
                continue
            n_operators += 1
            category, command = name
            try:
                operator = getattr(getattr(bpy.ops, category), command)
                known = set(operator.get_rna_type().properties.keys())
            except (AttributeError, KeyError):
                results.append((rel, first + call.lineno - 1, f"{category}.{command} indisponible en configuration d’usine"))
                continue
            unknown = {arg.arg for arg in call.keywords if arg.arg and arg.arg not in known}
            if unknown:
                results.append((rel, first + call.lineno - 1,
                                f"{category}.{command}, paramètres inconnus : {', '.join(sorted(unknown))}"))
    return n_blocks, n_operators, results


def main():
    chapters = curriculum_chapters()
    totals = [0, 0]
    problems = []
    terms = ("README", "LESSON", "THEORY", "TUTORIAL", "EXERCISES", "SOLUTIONS")
    for phase, number, _ in chapters:
        folder, = (ROOT / PHASE_DIRS[phase]).glob(f"CH{phase:02}_{number:02}_*")
        for term in terms:
            n_blocks, n_operators, diagnostics = inspect_file(folder / f"{term}.md")
            totals[0] += n_blocks
            totals[1] += n_operators
            problems.extend(diagnostics)
    for path, line, message in problems:
        print(f"{path}:{line}: {message}")
    print(f"Blender {bpy.app.version_string} : {totals[0]} blocs Python analysés, "
          f"{totals[1]} appels bpy.ops littéraux, {len(problems)} point(s) à examiner.")
    return bool(problems)


if __name__ == "__main__":
    raise SystemExit(main())
