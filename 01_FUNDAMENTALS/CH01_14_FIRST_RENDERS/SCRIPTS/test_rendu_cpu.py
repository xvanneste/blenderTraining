"""Contrôle la voie CPU sur le corrigé sans modifier la scène sur disque."""
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.dont_write_bytecode = True
from validate_ch01_14 import L, main as validate


if __name__ == "__main__":
    bpy.context.scene.cycles.device = "CPU"
    assert validate() == 0
    luminance = L.quick_render(percent=15, samples=8, engine="CYCLES")
    assert 0.05 < luminance < .8
    print(f"Cycles CPU, rendu de contrôle : luminance {luminance:.3f}.")
