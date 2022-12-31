import bpy
from Radiant import Utility_Functions



class RADIANT_MT_Add_Raymesh_Menu(bpy.types.Menu):
    bl_label = "Raymesh"
    bl_idname = "RADIANT_MT_add_raymesh_menu"

    def draw(self, context):

        layout = self.layout



        layout.label(text="Raymesh (Light Driver)")

        layout.operator("radiant.create_raymesh_at_selected_lights", text="Raymesh At Selected Light", icon="LIGHT_HEMI")

        layout.separator()

        operator = layout.operator("radiant.add_raymesh_light_as_driver", text="Raymesh Point", icon="LIGHT_POINT")
        operator.type = "POINT"
        operator.invoke_prop = False

        operator = layout.operator("radiant.add_raymesh_light_as_driver", text="Raymesh Spot", icon="LIGHT_SPOT")
        operator.type = "SPOT"
        operator.invoke_prop = False

        operator = layout.operator("radiant.add_raymesh_light_as_driver", text="Raymesh Area", icon="LIGHT_AREA")
        operator.type = "AREA"
        operator.invoke_prop = False







class RADIANT_MT_Add_Raymesh_Mesh_Menu(bpy.types.Menu):
    bl_label = "Raymesh (Mesh Only)"
    bl_idname = "RADIANT_MT_add_raymesh_mesh_menu"

    def draw(self, context):

        layout = self.layout


        layout.label(text="Raymesh (Mesh Only)")
        operator = layout.operator("radiant.add_raymesh", text="Raymesh Point", icon="LIGHT_POINT")
        operator.type = "POINT"

        operator = layout.operator("radiant.add_raymesh", text="Raymesh Spot", icon="LIGHT_SPOT")
        operator.type = "SPOT"

        operator = layout.operator("radiant.add_raymesh", text="Raymesh Area", icon="LIGHT_AREA")
        operator.type = "AREA"

        layout.separator()

        operator = layout.operator("radiant.add_raymesh", text="Raymesh Text", icon="LIGHT_AREA")
        operator.type = "TEXT"


        operator = layout.operator("radiant.add_raymesh", text="Raymesh Shape", icon="LIGHT_AREA")
        operator.type = "SHAPE"



class RADIANT_MT_Add_Object_Menu(bpy.types.Menu):
    bl_label = "Object"
    bl_idname = "RADIANT_MT_add_object_menu"

    def draw(self, context):

        layout = self.layout
        # layout.menu("RADIANT_MT_add_raymesh_menu", text="Raymesh", icon="LIGHT_HEMI")
        layout.operator("radiant.add_shadow_catcher_plane", text="Shadow Catcher Plane", icon="MATPLANE")
        layout.operator("radiant.add_volume_cube", text="Volume Cube", icon="FILE_VOLUME")

class RADIANT_MT_Radiant_Tool_Menu(bpy.types.Menu):
    bl_label = "Radiant Tool"
    bl_idname = "RADIANT_MT_radiant_tool_menu"

    def draw(self, context):

        layout = self.layout


        if context.mode in ["OBJECT", "EDIT_MESH", "EDIT_ARMATURE", "EDIT_CURVE", "POSE"]:
            layout.operator_context = "INVOKE_DEFAULT"
            # layout.operator("radiant.create_raymesh_at_selected_lights", text="Create Raymesh At Selected Light", icon="LIGHT_HEMI")
            # layout.separator()
            layout.operator("radiant.create_mesh_from_area_lights", text="Create Mesh From Area Lights", icon="LIGHT_AREA")
            layout.operator("radiant.create_tracked_empties_from_light", text="Create Light Tracker Empties", icon="EMPTY_DATA")
            layout.separator()
            layout.operator("radiant.aim_selected_lights", text="Aim Selected Lights", icon="CON_TRACKTO")

def draw_radiant_add_mesh_menu(self, context):

    layout = self.layout
    preferences = Utility_Functions.get_addon_preferences()

    if preferences.ENABLE_Add_Menu:
        if context.mode == "OBJECT":
            layout.separator()
            layout.menu("RADIANT_MT_add_raymesh_mesh_menu", text="Raymesh (Mesh)", icon="LIGHT_HEMI")

def draw_radiant_add_menu(self, context):

    layout = self.layout


    preferences = Utility_Functions.get_addon_preferences()

    if preferences.ENABLE_Add_Menu:
        if context.mode == "OBJECT":
            layout.separator()
            layout.menu("RADIANT_MT_add_object_menu", text="Object", icon="OUTLINER_DATA_LIGHTPROBE")

            layout.menu("RADIANT_MT_add_raymesh_menu", text="Raymesh", icon="LIGHT_HEMI")

            layout.separator()

        if context.mode in ["OBJECT", "EDIT_MESH", "EDIT_ARMATURE", "EDIT_CURVE", "POSE"]:

            layout.menu("RADIANT_MT_radiant_tool_menu", text="Radiant Tool", icon="TOOL_SETTINGS")



classes = [RADIANT_MT_Add_Object_Menu, RADIANT_MT_Radiant_Tool_Menu, RADIANT_MT_Add_Raymesh_Menu, RADIANT_MT_Add_Raymesh_Mesh_Menu]

addon_keymaps = []

def register():

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.VIEW3D_MT_light_add.append(draw_radiant_add_menu)
    bpy.types.VIEW3D_MT_mesh_add.append(draw_radiant_add_mesh_menu)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

    bpy.types.VIEW3D_MT_light_add.remove(draw_radiant_add_menu)
    bpy.types.VIEW3D_MT_mesh_add.remove(draw_radiant_add_mesh_menu)


    addon_keymaps.clear()

if __name__ == "__main__":
    register()
