
import bpy


from . import Solo_Light
from . import Find_Light
from . import Select_Light
from . import Remove_Light
from . import Aim_Light
from . import Duplicate_Light
from . import Move_Light
from . import Trackball_Light

from . import Apply_Constraint_Light

from . import Unhide_All_Light
from . import Unlock_All_Light

from . import Add_Light

from . import Listed_Light_Operator

from . import Open_Shader_Editor

from . import Make_Raymesh_From_Light

from . import Hide_Children

from . import Make_Single_Light


modules = [Make_Single_Light, Hide_Children, Make_Raymesh_From_Light, Open_Shader_Editor, Listed_Light_Operator, Add_Light, Unhide_All_Light, Unlock_All_Light, Apply_Constraint_Light, Solo_Light, Find_Light, Select_Light, Remove_Light, Aim_Light, Duplicate_Light, Trackball_Light, Move_Light]

def register():
    for module in modules:

        module.register()

def unregister():
    for module in modules:
        module.unregister()

if __name__ == "__main__":
    register()
