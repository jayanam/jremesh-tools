import bpy
from bpy.types import Panel

class JRT_PT_Panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Remesh settings"
    bl_category = "JRemesh"
    
    def draw(self, context):
       
        layout = self.layout
        scene = context.scene

        # UI
        row = layout.row()
        col = row.column()
        col.prop(context.scene, "deterministic")

        row = layout.row()
        col = row.column()
        col.prop(context.scene, "dominant")

        row = layout.row()
        col = row.column()
        col.prop(context.scene, "intrinsic")

        row = layout.row()
        col = row.column()
        col.prop(context.scene, "boundaries")

        row = layout.row()
        col = row.column()
        col.prop(context.scene, "smooth")

        row = layout.row()
        col = row.column()
        col.prop(context.scene, "crease")

        row = layout.row()
        col = row.column()
        col.prop(context.scene, "vertex_count")

        # Start remesh
        row = layout.row()
        col = row.column()
        col.operator('object.jrt_remesh_op', icon='MOD_BOOLEAN', text="Remesh")