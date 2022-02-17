bl_info = {
    "name" : "JRemesh Tools",
    "author" : "jayanam",
    "description" : "Quad Remesh tools for Blender 2.8 - 3.x",
    "blender" : (2, 80, 0),
    "version" : (0, 2, 1, 0),
    "location" : "View3D",
    "warning" : "",
    "category" : "Object"
}

import bpy
from bpy.props import *

from . jrt_panel import JRT_PT_Panel
from . jrt_remesh_op import JRT_OT_Remesh
from . jrt_pref import JRemeshPrefs

# Global properties
# ...

# Scene properties
bpy.types.Scene.deterministic = bpy.props.BoolProperty(name="Deterministic", description="Prefer (slower) deterministic algorithms", default = False)

bpy.types.Scene.dominant =  bpy.props.BoolProperty(name="Dominant", description="Generate a tri/quad dominant mesh instead of a pure tri/quad mesh", default = False)

bpy.types.Scene.intrinsic = bpy.props.BoolProperty(name="Intrinsic", description="Intrinsic mode", default = False)

bpy.types.Scene.boundaries = bpy.props.BoolProperty(name="Boundaries", description="Align to boundaries (only applies when the mesh is not closed)", default =False)

bpy.types.Scene.vertex_count = bpy.props.IntProperty(name="Vertex Count", description="Desired vertex count of the output mesh", default=4000, min=10, max=100000)

bpy.types.Scene.crease = bpy.props.IntProperty(name="Crease Degree", description="Dihedral angle threshold for creases", default=0, min=0, max=100)

bpy.types.Scene.smooth = bpy.props.IntProperty(name="Smooth iterations", description="Number of smoothing & ray tracing reprojection steps", default=2, min=0, max=10)

addon_keymaps = []

classes = ( JRT_PT_Panel, JRT_OT_Remesh, JRemeshPrefs )

def register():
    for c in classes:
        bpy.utils.register_class(c)

    # add keymap entry
    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')

    # kmi = km.keymap_items.new("object.frt_remesh_op", 'A', 'PRESS', shift=True, ctrl=True)
    # addon_keymaps.append((km, kmi))


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
 
    # remove keymap entry
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)

    addon_keymaps.clear()
    
if __name__ == "__main__":
    register()
