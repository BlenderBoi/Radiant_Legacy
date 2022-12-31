import bpy
from Radiant import Utility_Functions

class Radiant_Tags_List(bpy.types.PropertyGroup):

    Tag: bpy.props.StringProperty()


def ENUM_Show_Light_Filter(self, context):

    preferences = Utility_Functions.get_addon_preferences()
    if preferences.ENABLE_Tags:
        items = [("ALL","All","All"),("SELECTED","Selected","Selected"),("ACTIVE","Active","Active"), None, ("COLLECTION","Collection","Collection"),("TAGS","Tags","Tags"),("PINNED","Pinned","Pinned"),("TYPE","Type","Type")]
    else:
        items = [("ALL","All","All"),("SELECTED","Selected","Selected"),("ACTIVE","Active","Active"), None, ("COLLECTION","Collection","Collection"),("PINNED","Pinned","Pinned"),("TYPE","Type","Type")]

    return items

ENUM_Light_Type = [("POINT","Point","Point"),("SUN","Sun","Sun"),("SPOT","Spot","Spot"),("AREA","Area","Area")]

ENUM_Emission_Object_Filter = [("ALL","All Objects","All Objects"),("SELECTED","Selected Objects","Selected Objects"),("ACTIVE","Active Object","Active Object"), None, ("MATERIALS", "All Emission Material", "All Emission Material")]

ENUM_Emission_Node_Finder = [("ALL_INPUT","Find All Inputs","Find All Inputs"), ("DIRECT","Emission Direct","Emission Nodes & Direct Input")]





class Radiant_SCENE_Light_Panel_Properties(bpy.types.PropertyGroup):

    Light_Filter: bpy.props.EnumProperty(items=ENUM_Show_Light_Filter)
    Light_Filter_Name: bpy.props.StringProperty(default="",options={'TEXTEDIT_UPDATE'})

    Light_Filter_Collection: bpy.props.StringProperty()
    Light_Filter_Tags: bpy.props.StringProperty()

    Light_Filter_Type: bpy.props.EnumProperty(items=ENUM_Light_Type)

    Show_Tag_List: bpy.props.BoolProperty()
    Tags_List: bpy.props.CollectionProperty(type=Radiant_Tags_List)
    Tags_List_Index: bpy.props.IntProperty()

    Emission_Object_Filter: bpy.props.EnumProperty(items=ENUM_Emission_Object_Filter, default=1)
    Emission_Node_Finder: bpy.props.EnumProperty(items=ENUM_Emission_Node_Finder)

    Emission_Include_Principled: bpy.props.BoolProperty(default=False)
    Emission_Include_Ramp_Nodes: bpy.props.BoolProperty(default=False)

    Move_Selected_to_Top: bpy.props.BoolProperty(default=False)
    Expand_Active_Light: bpy.props.BoolProperty(default=True)

    Hide_Linked_Duplicates: bpy.props.BoolProperty(default=False)


classes = [Radiant_Tags_List, Radiant_SCENE_Light_Panel_Properties]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)


    bpy.types.Scene.Radiant_Light_Properties = bpy.props.PointerProperty(type=Radiant_SCENE_Light_Panel_Properties)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.Radiant_Light_Properties
