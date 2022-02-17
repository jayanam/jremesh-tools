import bpy
from bpy.props import *

from bpy.types import AddonPreferences

def get_preferences():
    return bpy.context.preferences.addons[__package__].preferences

class JRemeshPrefs(AddonPreferences):
    bl_idname = __package__

    im_in_blender_folder : bpy.props.BoolProperty(
        name="Instant Meshes in Blender folder", 
        default = False
    )

    im_filepath: bpy.props.StringProperty(
        name="Instant Meshes Application (exe)",
        subtype='FILE_PATH'
    )

    def draw(self, context):
        layout = self.layout
        row = self.layout.row()
        row.label(text="Instant Meshes in Blender folder?")
        row.prop(self, 'im_in_blender_folder', text='')

        row = self.layout.row()
        row.label(text="Instant Meshes Application (exe)")
        row.prop(self, 'im_filepath', text='')
