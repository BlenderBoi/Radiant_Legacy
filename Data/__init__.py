import bpy

from . import Object_Properties
from . import Scene_Properties
from . import Material_Properties

modules = [Material_Properties, Object_Properties, Scene_Properties]

def register():

    for module in modules:
        module.register()

def unregister():

    for module in modules:
        module.unregister()
