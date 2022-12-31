import bpy

from Radiant import Utility_Functions

class RADIANT_PT_Radiant_Tool_Panel(bpy.types.Panel):
    """Radiant Tools"""
    bl_label = "Radiant Tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Radiant"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        preferences = Utility_Functions.get_addon_preferences()
        return preferences.PANEL_Radiant_Tools_Panel

    def draw(self, context):
        layout = self.layout

        if context.mode in ["OBJECT", "EDIT_MESH", "EDIT_ARMATURE", "EDIT_CURVE", "POSE"]:
            layout.label(text="Radiant Tools", icon="TOOL_SETTINGS")
            layout.operator_context = "INVOKE_DEFAULT"

            if context.mode == "OBJECT":
                layout.operator("radiant.create_mesh_from_area_lights", text="Create Mesh From Area Lights", icon="LIGHT_AREA")
                layout.operator("radiant.create_tracked_empties_from_light", text="Create Light Tracker Empties", icon="EMPTY_DATA")
                layout.operator("radiant.aim_selected_lights", text="Aim Selected Lights", icon="CON_TRACKTO")


        if context.mode == "OBJECT":
            layout.separator()
            layout.label(text="Object", icon="OUTLINER_DATA_LIGHTPROBE")
            layout.operator("radiant.add_shadow_catcher_plane", text="Shadow Catcher Plane", icon="MATPLANE")
            layout.operator("radiant.add_volume_cube", text="Volume Cube", icon="FILE_VOLUME")

            layout.separator()

            layout.label(text="Raymesh", icon="LIGHT_HEMI")
            layout.menu("RADIANT_MT_add_raymesh_menu", text="Raymesh", icon="LIGHT_HEMI")
            layout.menu("RADIANT_MT_add_raymesh_mesh_menu", text="Raymesh (Mesh Only)", icon="LIGHT_HEMI")




classes = [RADIANT_PT_Radiant_Tool_Panel]


def register():
  for cls in classes:
    bpy.utils.register_class(cls)


def unregister():
  for cls in classes:
    bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
