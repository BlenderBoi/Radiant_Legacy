import bpy
from Radiant import Utility_Functions




class Radiant_MATERIAL_Light_Panel_Properties(bpy.types.PropertyGroup):

    SHOW_Emission: bpy.props.BoolProperty(default=True)

classes = [Radiant_MATERIAL_Light_Panel_Properties]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)


    bpy.types.Material.Radiant_Light_Properties = bpy.props.PointerProperty(type=Radiant_MATERIAL_Light_Panel_Properties)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Material.Radiant_Light_Properties
