bl_info = {
    "name" : "JRemesh Tools",
    "author" : "jayanam",
    "description" : "Quad Remesh tools for Blender 2.8 - 3.x",
    "blender" : (2, 80, 0),
    "version" : (0, 3, 2, 2),
    "location" : "View3D",
    "warning" : "",
    "category" : "Object"
}

import bpy
from bpy.props import *

from . jrt_panel import JRT_PT_Panel
from . jrt_remesh_op import JRT_OT_Remesh
from . jrt_pref import JRemeshPrefs

remesher_items = [ ("Instant Meshes", "Instant Meshes", "", 0),
                   ("Blender Quadriflow", "Blender Quadriflow", "", 1)
                 ]

bpy.types.Scene.remesher = bpy.props.EnumProperty(items=remesher_items, 
                                                   name="Remesher",
                                                   default="Instant Meshes")

# Scene properties Instant Meshes
bpy.types.Scene.deterministic = bpy.props.BoolProperty(name="Deterministic", description="Prefer (slower) deterministic algorithms", default = False)

bpy.types.Scene.dominant =  bpy.props.BoolProperty(name="Dominant", description="Generate a tri/quad dominant mesh instead of a pure tri/quad mesh", default = False)

bpy.types.Scene.intrinsic = bpy.props.BoolProperty(name="Intrinsic", description="Intrinsic mode", default = False)

bpy.types.Scene.boundaries = bpy.props.BoolProperty(name="Boundaries", description="Align to boundaries (only applies when the mesh is not closed)", default =False)

bpy.types.Scene.vertex_count = bpy.props.IntProperty(name="Vertex Count", description="Desired vertex count of the output mesh", default=4000, min=10, max=500000)

bpy.types.Scene.crease = bpy.props.IntProperty(name="Crease Degree", description="Dihedral angle threshold for creases", default=0, min=0, max=100)

bpy.types.Scene.smooth = bpy.props.IntProperty(name="Smooth iterations", description="Number of smoothing & ray tracing reprojection steps", default=2, min=0, max=10)

# Scene properties Quadriflow
bpy.types.Scene.qf_use_mesh_sym = bpy.props.BoolProperty(name="Use Mesh Symmetry", description="Generates a symmetrical mesh using the Mesh Symmetry options.", default = False)

bpy.types.Scene.qf_preserve_sharp = bpy.props.BoolProperty(name="Preserve Sharp", description="Tells the algorithm to try to preserve sharp features of the mesh. Enabling this could make the operator slower depending on the complexity of the mesh.", default = True)

bpy.types.Scene.qf_preserve_mesh_boundary = bpy.props.BoolProperty(name="Preserve Mesh Boundary", description="Tells the algorithm to try to preserve the original volume of the mesh. Enabling this could make the operator slower depending on the complexity of the mesh.", default = False)

bpy.types.Scene.qf_preserve_paint_mask = bpy.props.BoolProperty(name="Preserve Paint Mask", description="Reprojects the Paint Mask onto the new mesh.", default = False)

bpy.types.Scene.qf_smooth_normals = bpy.props.BoolProperty(name="Smooth Normals", description="Applies the Smooth Normals operator to the resulting mesh.", default = False)

bpy.types.Scene.qf_face_count = bpy.props.IntProperty(name="Number of Faces", description="Input target number of faces in the new mesh.", default=2000, min=1, max=1000000)

# Common properties
bpy.types.Scene.rm_triangulate = bpy.props.BoolProperty(name="Triangulate", description="Add a triangulate modifier to the mesh before remeshing", default = False)

bpy.types.Scene.rm_fill_holes = bpy.props.BoolProperty(name="Fill holes", description="Try to fill the holes after remeshig (make manifold)", default = False)


addon_keymaps = []

classes = ( JRT_PT_Panel, JRT_OT_Remesh, JRemeshPrefs )

def register():
    for c in classes:
        bpy.utils.register_class(c)

    # add keymap entry
    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
 
    # remove keymap entry
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)

    addon_keymaps.clear()
    
if __name__ == "__main__":
    register()
