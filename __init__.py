bl_info = {
    "name": "Radiant",
    "author": "BlenderBoi",
    "version": (1, 3, 0),
    "blender": (3, 1, 0),
    "description": "",
    "wiki_url": "",
    "category": "Light",
}

import bpy
from . import Preferences
from . import Data
from . import Panels
from . import Operators
from . import List
from . import Menus


modules = [List, Data, Panels, Operators, Menus, Preferences]

def register():

    for module in modules:
        module.register()

def unregister():

    for module in modules:
        module.unregister()
















if __name__ == "__main__":
    register()
