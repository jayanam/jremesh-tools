import bpy
from bpy.props import *

from bpy.types import AddonPreferences

def get_preferences():
    return bpy.context.preferences.addons[__package__].preferences

class JRemeshPrefs(AddonPreferences):
    bl_idname = __package__


    im_filepath: bpy.props.StringProperty(
        name="Instant Meshes Application (exe)",
        subtype='FILE_PATH'
    )

    # qf_filepath: bpy.props.StringProperty(
    #     name="Quadriflow Application (exe)",
    #     subtype='FILE_PATH'
    # )

    def draw(self, context):
        layout = self.layout

        row = self.layout.row()
        row.label(text="Instant Meshes Application")
        row.prop(self, 'im_filepath', text='')

        # row = self.layout.row()
        # row.label(text="Quadriflow Application (exe)")
        # row.prop(self, 'qf_filepath', text='')
