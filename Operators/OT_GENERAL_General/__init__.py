import bpy

from . import Create_Mesh_From_Area_Lights
from . import Create_Tracked_Empties
from . import Aim_Selected_Light
from . import Create_Raymesh_At_Selected_Light


modules = [Create_Raymesh_At_Selected_Light, Aim_Selected_Light, Create_Tracked_Empties, Create_Mesh_From_Area_Lights]

def register():

    for module in modules:
        module.register()

def unregister():

    for module in modules:
        module.unregister()
