bl_info = {
    "name": "ObjSeqToFBX",
    "description": "Convert OBJ Sequence to a single fbx file.",
    "author": "cliwo",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "3D View > Tools",
    "wiki_url": "https://github.com/Cliwo/MarvelousDesigner_Obj_seq_To_FBX",
    "category": "Development"
}

import bpy
from .obj_seq_to_fbx import *

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )

# ------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------

class MyProperties(PropertyGroup):
    input_path: StringProperty(
        name = "OBJ Sequence Path",
        description="Choose a directory:",
        default="",
        maxlen=1024,
        subtype='DIR_PATH'
        )
    
    output_path: StringProperty(
        name = "Path to Export FBX",
        description="Choose a directory:",
        default="",
        maxlen=1024,
        subtype='DIR_PATH'
        )
    
    output_file_name: StringProperty(
        name = "Name of FBX file",
        description="Input a name",
        default="",
        maxlen=128,
        )

# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------

class WM_OT_OBJSeqToFBX(Operator):
    bl_label = "Convert To FBX"
    bl_idname = "wm.obj_to_fbx"

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool
        
        convert_obj_seq_to_fbx(mytool.input_path, mytool.output_path, mytool.output_file_name)
        return {'FINISHED'}

# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------

class OBJECT_PT_CustomPanel(Panel):
    bl_label = "OBJSeqToFBX Panel"
    bl_idname = "custom_panel_objseq_to_fbx"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "OBJSeqToFBX"
    bl_context = "objectmode"   


    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        layout.prop(mytool, "input_path")
        layout.prop(mytool, "output_path")
        layout.prop(mytool, "output_file_name")
        layout.operator("wm.obj_to_fbx")
        layout.separator()


# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = (
    MyProperties,
    WM_OT_OBJSeqToFBX,
    OBJECT_PT_CustomPanel
)

def register():
    from bpy.utils import register_class
    for cls in classes:
       register_class(cls)

    bpy.types.Scene.my_tool = PointerProperty(type=MyProperties)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.my_tool

if __name__ == "__main__":
    register()
