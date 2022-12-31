import bpy

from . import MT_Radiant_Menu
from . import MT_Add_Menu

modules = [MT_Radiant_Menu, MT_Add_Menu]

def register():

    for module in modules:
        module.register()

def unregister():

    for module in modules:
        module.unregister()
