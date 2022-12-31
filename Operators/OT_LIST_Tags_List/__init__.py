
import bpy


from . import Radiant_Tags_List_Operator
from . import Select_Tagged_Lights
from . import Set_Hide_Tagged_Lights
from . import Set_Property_Lights
from . import Adjust_Property_Lights
from . import Tag_Selected_Lights
modules = [Tag_Selected_Lights, Set_Property_Lights, Radiant_Tags_List_Operator, Select_Tagged_Lights, Set_Hide_Tagged_Lights, Adjust_Property_Lights]

def register():
    for module in modules:

        module.register()

def unregister():
    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
