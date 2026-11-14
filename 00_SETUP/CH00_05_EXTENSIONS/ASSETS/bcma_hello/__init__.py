# SPDX-License-Identifier: GPL-3.0-or-later
"""BCMA Hello — extension d'exemple (CH00.05).

Ajoute un onglet « BCMA » dans la sidebar (N) de la vue 3D, avec :
- le nombre d'objets de la scène et d'objets sélectionnés ;
- un bouton qui renomme les objets sélectionnés avec un préfixe de type
  (GEO_, CAM_, LGT_, EMP_…) selon les conventions de l'académie.
"""
import bpy

PREFIX = {"MESH": "GEO_", "CAMERA": "CAM_", "LIGHT": "LGT_", "EMPTY": "EMP_",
          "CURVE": "CRV_", "ARMATURE": "RIG_", "GREASEPENCIL": "GP_", "FONT": "TXT_"}


class BCMA_OT_prefix_names(bpy.types.Operator):
    """Ajoute le préfixe de type BCMA aux objets sélectionnés"""
    bl_idname = "bcma.prefix_names"
    bl_label = "Préfixer les noms (BCMA)"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        n = 0
        for ob in context.selected_objects:
            p = PREFIX.get(ob.type)
            if p and not ob.name.startswith(p):
                ob.name = p + ob.name
                n += 1
        self.report({"INFO"}, f"{n} objet(s) renommé(s)")
        return {"FINISHED"}


class BCMA_PT_hello(bpy.types.Panel):
    bl_label = "BCMA Hello"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BCMA"

    def draw(self, context):
        col = self.layout.column()
        col.label(text=f"Objets : {len(context.scene.objects)}")
        col.label(text=f"Sélectionnés : {len(context.selected_objects)}")
        col.operator(BCMA_OT_prefix_names.bl_idname, icon="SORTALPHA")


CLASSES = (BCMA_OT_prefix_names, BCMA_PT_hello)


def register():
    for c in CLASSES:
        bpy.utils.register_class(c)


def unregister():
    for c in reversed(CLASSES):
        bpy.utils.unregister_class(c)
