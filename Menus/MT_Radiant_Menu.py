import bpy


class RADIANT_MT_Radiant_Menu(bpy.types.Menu):
    bl_label = "Radiant Menu"
    bl_idname = "RADIANT_MT_radiant_menu"

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

            layout.menu("RADIANT_MT_add_raymesh_menu", text="Raymesh", icon="LIGHT_HEMI")
            layout.menu("RADIANT_MT_add_raymesh_mesh_menu", text="Raymesh (Mesh Only)", icon="LIGHT_HEMI")


classes = [RADIANT_MT_Radiant_Menu]

addon_keymaps = []

def register():

    for cls in classes:
        bpy.utils.register_class(cls)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if kc:
        km = kc.keymaps.new(name = "3D View", space_type="VIEW_3D")
        kmi = km.keymap_items.new("wm.call_menu", type="L", value="PRESS", shift=True, ctrl=True)
        kmi.properties.name = "RADIANT_MT_radiant_menu"
        addon_keymaps.append([km, kmi])

def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

    addon_keymaps.clear()

if __name__ == "__main__":
    register()
