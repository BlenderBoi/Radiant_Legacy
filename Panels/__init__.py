import bpy


from . import PANEL_Light_Panel
from . import PANEL_Object_Data_Properties
from . import PANEL_Render_Settings
from . import PANEL_Active_Light_Panel
from . import PANEL_Radiant_Tool_Panel
from . import PANEL_Light_Data_Properties

modules = [PANEL_Light_Data_Properties, PANEL_Radiant_Tool_Panel, PANEL_Active_Light_Panel, PANEL_Light_Panel, PANEL_Object_Data_Properties, PANEL_Render_Settings]

def register():

    for module in modules:
        module.register()

def unregister():

    for module in modules:
        module.unregister()
