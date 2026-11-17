"""Extension pédagogique. La commande ajoute un repère au curseur 3D."""
import bpy


class BCMA_OT_repere(bpy.types.Operator):
    bl_idname = "bcma.ajouter_repere"
    bl_label = "Ajouter un repère"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        obj = bpy.data.objects.new("REP_Plan", None)
        obj.empty_display_type = "ARROWS"
        obj.location = context.scene.cursor.location
        context.collection.objects.link(obj)
        self.report({"INFO"}, "Repère ajouté au curseur")
        return {"FINISHED"}


class BCMA_PT_plan(bpy.types.Panel):
    bl_label = "Repères de plan"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BCMA"

    def draw(self, context):
        self.layout.operator(BCMA_OT_repere.bl_idname)


CLASSES = (BCMA_OT_repere, BCMA_PT_plan)


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(CLASSES):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
