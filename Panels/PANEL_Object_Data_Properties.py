import bpy
from Radiant import Utility_Functions

class Radiant_PT_Object_Data_Properties_Panel(bpy.types.Panel):
    """Radiant Object Data"""
    bl_label = "Radiant"
    bl_idname = "OBJECT_PT_Radiant_Object_Data"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    @classmethod
    def poll(cls, context):
        object = context.object
        if object:
            if object.type == "LIGHT":
                return True

    def draw(self, context):
        layout = self.layout
        object = context.object
        scn = context.scene
        scn_properties = scn.Radiant_Light_Properties
        preferences = Utility_Functions.get_addon_preferences()

        if object:
            object_properties = object.Radiant_Light_Properties

            if preferences.ENABLE_Tags:
                layout.prop_search(object_properties, "Tags", scn_properties, "Tags_List", text="Tags")

            layout.prop(object_properties, "Notes", text="Notes", icon="TEXT")

classes = [Radiant_PT_Object_Data_Properties_Panel]

def register():

    for cls in classes:

        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:

        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
