import bpy
from . import OT_Add_Shadow_Catcher_Plane
from . import OT_Add_Volume_Cube
from . import OT_Add_RayMesh
from . import OT_Add_RayMesh_Light_As_Driver

modules = [OT_Add_RayMesh_Light_As_Driver, OT_Add_RayMesh, OT_Add_Shadow_Catcher_Plane, OT_Add_Volume_Cube]

def register():

    for module in modules:
        module.register()

def unregister():

    for module in modules:
        module.unregister()
