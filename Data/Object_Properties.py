import bpy
from Radiant import Utility_Functions

def Temperature_Update(self, context):
    if self.Use_Blackbody:
        self.id_data.data.color = Utility_Functions.Blackbody_Color(self.Blackbody_Temperature)


ENUM_Tab_Properties_Display = [("PROPERTIES","Properties","Properties"), ("NODE","Nodes","Nodes")]

class Radiant_OBJECT_Light_Panel_Properties(bpy.types.PropertyGroup):

    Use_Blackbody: bpy.props.BoolProperty()
    Blackbody_Temperature: bpy.props.FloatProperty(soft_min = 0, step=100, update=Temperature_Update)

    Show_Light_Settings: bpy.props.BoolProperty()
    Show_Light_Advanced_Option: bpy.props.BoolProperty()
    Show_Light_Factor: bpy.props.BoolProperty()
    Show_Light_Shape: bpy.props.BoolProperty()
    Show_Light_Transform: bpy.props.BoolProperty()
    Show_Light_Shadow: bpy.props.BoolProperty()

    Show_Light_Custom_Properties: bpy.props.BoolProperty()
    Show_Object_Custom_Properties: bpy.props.BoolProperty()

    Show_Raymesh_Properties: bpy.props.BoolProperty()


    Contextual_Raymesh_Properties: bpy.props.BoolProperty()


    Tab_Properties_Display: bpy.props.EnumProperty(items=ENUM_Tab_Properties_Display)

    Show_Node_Properties: bpy.props.BoolProperty(default=True)

    Pin: bpy.props.BoolProperty()
    Tags: bpy.props.StringProperty()
    Notes: bpy.props.StringProperty()

classes = [Radiant_OBJECT_Light_Panel_Properties]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Object.Radiant_Light_Properties = bpy.props.PointerProperty(type=Radiant_OBJECT_Light_Panel_Properties)
    bpy.types.Light.Disable_Make_Raymesh_Button = bpy.props.BoolProperty(default=False)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Object.Radiant_Light_Properties
    del bpy.types.Light.Disable_Make_Raymesh_Button
