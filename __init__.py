bl_info = {
    "name" : "JRemesh Tools",
    "author" : "jayanam",
    "description" : "Quad Remesh tools for Blender 2.8 - 3.x",
    "blender" : (2, 80, 0),
    "version" : (0, 1, 0, 0),
    "location" : "View3D",
    "warning" : "",
    "category" : "Object"
}

import bpy
from bpy.props import *


# Global properties
bpy.types.WindowManager.in_modal_mode = BoolProperty(name="Modal Mode",
                                        default = False)

# Scene properties
# bpy.types.Scene.extract_thickness = bpy.props.FloatProperty( name="Extract thickness", 
#                                       description="Thickness of the extracted mesh",
#                                       default = 0.1)


# Scene properties
bpy.types.WindowManager.in_draw_mode = BoolProperty(name="Draw Mode", default = False)


addon_keymaps = []

classes = ( )

def register():
    for c in classes:
        bpy.utils.register_class(c)

    # add keymap entry
    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')

    # kmi = km.keymap_items.new("object.fsc_add_object", 'A', 'PRESS', shift=True, ctrl=True)
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
