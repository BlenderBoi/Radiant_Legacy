import bpy
from Radiant import Utility_Functions

class Radiant_PT_Light_Data_Properties_Panel(bpy.types.Panel):
    """Radiant Light Data"""
    bl_label = "Radiant"
    bl_idname = "OBJECT_PT_Radiant_Light_Data"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    @classmethod
    def poll(cls, context):
        object = context.object
        if object:
            if object.type == "LIGHT":
                return True

    def draw(self, context):
        layout = self.layout
        object = context.object
        layout.prop(object.data, "Disable_Make_Raymesh_Button", text="Disable Make Raymesh Button")


classes = [Radiant_PT_Light_Data_Properties_Panel]

def register():

    for cls in classes:

        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:

        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
