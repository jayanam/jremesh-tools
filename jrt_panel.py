import bpy
from bpy.types import Panel

class JRT_PT_Panel(Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_label = "Remesh settings"
    bl_category = "JRemesh"
    
    def draw(self, context):
       
        layout = self.layout

        # UI
        row = layout.row()
        split = row.split(factor=0.4)
        col = split.column()
        col.label(text="Remesher")
        col = split.column()
        col.prop(context.scene, "remesher", text="")
        
        if context.scene.remesher == "Instant Meshes":

            row = layout.row()
            row.prop(context.scene, "deterministic")

            row = layout.row()
            row.prop(context.scene, "dominant")

            row = layout.row()
            row.prop(context.scene, "intrinsic")

            row = layout.row()
            row.prop(context.scene, "boundaries")

            row = layout.row()
            row.prop(context.scene, "smooth")

            row = layout.row()
            row.prop(context.scene, "crease")

            row = layout.row()
            row.prop(context.scene, "vertex_count")

        elif context.scene.remesher == "Blender Quadriflow":
 
            row = layout.row()
            row.prop(context.scene, "qf_use_mesh_sym")

            row = layout.row()
            row.prop(context.scene, "qf_preserve_sharp")

            row = layout.row()
            row.prop(context.scene, "qf_preserve_mesh_boundary")

            row = layout.row()
            row.prop(context.scene, "qf_preserve_paint_mask")

            row = layout.row()
            row.prop(context.scene, "qf_smooth_normals")

            row = layout.row()
            row.prop(context.scene, "qf_face_count")

        row = layout.row()
        row.prop(context.scene, "rm_triangulate")

        row = layout.row()
        row.prop(context.scene, "rm_fill_holes")

        # Start remesh
        row = layout.row()
        col = row.column()
        col.operator('object.jrt_remesh_op', icon='VIEW_PERSPECTIVE', text="Remesh")