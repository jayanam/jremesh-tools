from msilib.schema import Error
import bpy
from bpy.types import Operator

import os
import shutil
import tempfile
import subprocess

from . jrt_pref import get_preferences

from . utils.select_utils import *

class JRT_OT_Remesh(Operator):
    bl_idname = "object.jrt_remesh_op"
    bl_label = "Quad remesh"
    bl_description = "Execute quad remesher" 
    bl_options = {'REGISTER', 'UNDO'} 

    @classmethod
    def poll(cls, context):  
        return context.active_object is not None

    def execute(self, context):
        try:
            mode = get_mode()

            to_object()
            
            pref = get_preferences()

            app_path = pref.im_filepath

            if pref.im_in_blender_folder:
                app_path = "Instant Meshes.exe"
            
            if not os.path.isfile(app_path):
                raise IOError("Path to Instant Meshes Application is missing.")

            tmp_dir = tempfile.gettempdir()
            orig = os.path.join(tmp_dir, 'orig_object.obj')
            output = os.path.join(tmp_dir, 'remeshed_object.obj')

            self.report({'INFO'}, "JRemesh started")

            active_obj_name = context.active_object.name

            # Export original object
            bpy.ops.export_scene.obj(filepath=orig,
                                        check_existing=False,
                                        axis_forward='-Z', axis_up='Y',
                                        use_selection=True,
                                        use_mesh_modifiers=True,
                                        use_edges=True,
                                        use_smooth_groups=False,
                                        use_smooth_groups_bitflags=False,
                                        use_normals=True,
                                        use_uvs=True )

            orig_object = bpy.data.objects[active_obj_name]

            options = self.build_options(context, output)

            self.do_remesh(app_path, orig, options)

            # Import remeshed object
            bpy.ops.import_scene.obj(filepath=output,
                                     use_split_objects=False,
                                     use_smooth_groups=False,
                                     use_image_search=False,
                                     axis_forward='-Z', axis_up='Y')

            # Post import remeshed object                    
            remeshed_object = bpy.context.selected_objects[0]

            remeshed_object.name = active_obj_name + '_rm'

            remeshed_object.data.materials.clear()
            for mat in orig_object.data.materials:
                remeshed_object.data.materials.append(mat)

            for edge in remeshed_object.data.edges:
                edge.use_edge_sharp = False

            deselect_all()

            select(remeshed_object)

            bpy.ops.mesh.customdata_custom_splitnormals_clear()
            
            orig_object.hide_set(True)

            make_active(remeshed_object)

            to_mode(mode)

            os.remove(output)

        except IOError as ioerr:
            self.report({'ERROR'}, "JRemesh: {0}".format(ioerr))
        else:
            self.report({'INFO'}, "JRemesh completed")
        return {'FINISHED'}

    def do_remesh(self, im_app, orig, options):
        cmd = [im_app] + options + [orig]
        subprocess.run(cmd)

    def build_options(self, context, output):
        options = ['-c', str(context.scene.crease),
                   '-v', str(context.scene.vertex_count),
                   '-S', str(context.scene.smooth),
                   '-o', output]

        if context.scene.deterministic:
            options.append('-d')
        if context.scene.dominant:
            options.append('-D')
        if context.scene.intrinsic:
            options.append('-i')
        if context.scene.boundaries:
            options.append('-b')
        return options