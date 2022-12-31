import bpy

from . import OT_LIST_Tags_List
from . import OT_PT_Light_Panel
from . import OT_GENERAL_Add
from . import OT_GENERAL_General

modules = [OT_GENERAL_General, OT_GENERAL_Add, OT_LIST_Tags_List, OT_PT_Light_Panel]

def register():

    for module in modules:
        module.register()

def unregister():

    for module in modules:
        module.unregister()
