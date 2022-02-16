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
         
    def execute(self, context):
        try:
            mode = get_mode()

            to_object()
            
            tmp_dir = tempfile.gettempdir()
            im_app = get_preferences().im_filepath
            orig = os.path.join(tmp_dir, 'orig_object.obj')
            output = os.path.join(tmp_dir, 'remeshed_object.obj')

            self.report({'INFO'}, "JRemesh started")

            active_obj_name = context.active_object.name

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

            cmd = [im_app] + options + [orig]

            subprocess.run(cmd)

            bpy.ops.import_scene.obj(filepath=output,
                                     use_split_objects=False,
                                     use_smooth_groups=False,
                                     use_image_search=False,
                                     axis_forward='-Z', axis_up='Y')

            remeshed_object = bpy.context.selected_objects[0]

            remeshed_object.name = active_obj_name + '_rm'

            for mat in orig_object.data.materials:
                remeshed_object.data.materials.append(mat)

            for edge in remeshed_object.data.edges:
                edge.use_edge_sharp = False

            deselect_all()

            select(remeshed_object)

            bpy.ops.mesh.customdata_custom_splitnormals_clear()
            
            # bpy.ops.object.data_transfer(use_reverse_transfer=False,
            #                              use_freeze=False, data_type='UV', use_create=True, vert_mapping='NEAREST',
            #                              edge_mapping='NEAREST', loop_mapping='NEAREST_POLYNOR', poly_mapping='NEAREST',
            #                              use_auto_transform=False, use_object_transform=True, use_max_distance=False,
            #                              max_distance=1.0, ray_radius=0.0, islands_precision=0.1, layers_select_src='ACTIVE',
            #                              layers_select_dst='ACTIVE', mix_mode='REPLACE', mix_factor=1.0)

            orig_object.hide_set(True)
            select(remeshed_object)

            os.remove(output)

            to_mode(mode)

        except RuntimeError:
            pass
        finally:
            self.report({'INFO'}, "JRemesh completed")
        return {'FINISHED'}

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