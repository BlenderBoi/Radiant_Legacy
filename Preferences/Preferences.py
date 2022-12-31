import bpy
import os
import pathlib
import rna_keymap_ui

from . import Preferences
from Radiant import Utility_Functions
from Radiant import Panels

def get_menu(km, operator, menu):
    for idx, kmi in enumerate(km.keymap_items):
        if km.keymap_items.keys()[idx] == operator:
            if km.keymap_items[idx].properties.name == menu:
                return kmi
    return None

def update_panel(self, context):

    addon_preferences = Utility_Functions.get_addon_preferences()
    message = ": Updating Panel locations has failed"

    panels = []



    # item = [Panels.Render_Settings_Panel.Radiant_Render_Settings_Panel.RADIANT_PT_Render_Settings_Panel, addon_preferences.PANEL_Emission_Panel_Category, addon_preferences.PANEL_Emission_Panel_Label]
    pt = Panels.PANEL_Render_Settings.RADIANT_PT_Render_Settings_Panel
    catagory = addon_preferences.PANEL_Render_Settings_Panel_Category
    label = addon_preferences.PANEL_Render_Settings_Panel_Label
    item = [pt, catagory, label]
    panels.append(item)

    pt = Panels.PANEL_Active_Light_Panel.RADIANT_PT_Active_Light_Properties_Panel
    catagory = addon_preferences.PANEL_Active_Light_Properties_Panel_Category
    label = addon_preferences.PANEL_Active_Light_Properties_Panel_Label
    item = [pt, catagory, label]
    panels.append(item)


    pt = Panels.PANEL_Light_Panel.RADIANT_PT_Light_Panel
    catagory = addon_preferences.PANEL_Light_Panel_Category
    label = addon_preferences.PANEL_Light_Panel_Label
    item = [pt, catagory, label]
    panels.append(item)


    pt = Panels.PANEL_Radiant_Tool_Panel.RADIANT_PT_Radiant_Tool_Panel
    catagory = addon_preferences.PANEL_Radiant_Tools_Panel_Category
    label = addon_preferences.PANEL_Radiant_Tools_Panel_Label
    item = [pt, catagory, label]
    panels.append(item)

    try:
        pass
        for item in panels:

            panel = item[0]
            category = item[1]
            label = item[2]

            if "bl_rna" in panel.__dict__:
                bpy.utils.unregister_class(panel)

            panel.bl_category = category
            panel.bl_label = label

            bpy.utils.register_class(panel)

    except Exception as e:
        print("\n[{}]\n{}\n\nError:\n{}".format(__name__, message, e))
        pass



ENUM_Tabs = [("GENERAL", "General", "General"), ("KEYMAPS", "Keymaps", "Keymaps")]

class Radiant_user_preferences(bpy.types.AddonPreferences):

    bl_idname = Utility_Functions.get_addon_name()


    TABS_Preferences: bpy.props.EnumProperty(items=ENUM_Tabs)

    PANEL_Light_Panel: bpy.props.BoolProperty(default=True)
    PANEL_Light_Panel_Category: bpy.props.StringProperty(default="Radiant", update=update_panel)
    PANEL_Light_Panel_Label: bpy.props.StringProperty(default="Light Panel", update=update_panel)

    PANEL_Render_Settings_Panel: bpy.props.BoolProperty(default=True)
    PANEL_Render_Settings_Panel_Category: bpy.props.StringProperty(default="Radiant", update=update_panel)
    PANEL_Render_Settings_Panel_Label: bpy.props.StringProperty(default="Render Settings", update=update_panel)

    PANEL_Render_Settings_Panel: bpy.props.BoolProperty(default=True)
    PANEL_Render_Settings_Panel_Category: bpy.props.StringProperty(default="Radiant", update=update_panel)
    PANEL_Render_Settings_Panel_Label: bpy.props.StringProperty(default="Render Settings", update=update_panel)


    PANEL_Active_Light_Properties_Panel: bpy.props.BoolProperty(default=True)
    PANEL_Active_Light_Properties_Panel_Category: bpy.props.StringProperty(default="Radiant", update=update_panel)
    PANEL_Active_Light_Properties_Panel_Label: bpy.props.StringProperty(default="Active Light", update=update_panel)


    PANEL_Radiant_Tools_Panel: bpy.props.BoolProperty(default=True)
    PANEL_Radiant_Tools_Panel_Category: bpy.props.StringProperty(default="Radiant", update=update_panel)
    PANEL_Radiant_Tools_Panel_Label: bpy.props.StringProperty(default="Radiant Tools", update=update_panel)



    Hide_Raymesh_Button_After_Make: bpy.props.BoolProperty(default=True)


    SHOW_LIGHT_PANEL_Icon_Expose: bpy.props.BoolProperty()

    ICON_LIGHT_PANEL_Light_Icon: bpy.props.BoolProperty(default=False)
    ICON_LIGHT_PANEL_Solo: bpy.props.BoolProperty(default=False)
    ICON_LIGHT_PANEL_Select: bpy.props.BoolProperty(default=True)
    ICON_LIGHT_PANEL_Find: bpy.props.BoolProperty(default=True)
    ICON_LIGHT_PANEL_Light_Type: bpy.props.BoolProperty(default=False)
    ICON_LIGHT_PANEL_Lock_Select: bpy.props.BoolProperty(default=False)
    ICON_LIGHT_PANEL_Hide_Viewport: bpy.props.BoolProperty(default=True)
    ICON_LIGHT_PANEL_Hide_Render: bpy.props.BoolProperty(default=True)

    ICON_LIGHT_PANEL_Link_Make_Single_Icon: bpy.props.BoolProperty(default=True)

    ICON_LIGHT_PANEL_Hide_Children: bpy.props.BoolProperty(default=True)

    ICON_LIGHT_PANEL_Duplicate: bpy.props.BoolProperty(default=False)
    ICON_LIGHT_PANEL_Remove: bpy.props.BoolProperty(default=True)
    ICON_LIGHT_PANEL_Move: bpy.props.BoolProperty(default=False)
    ICON_LIGHT_PANEL_Rotate: bpy.props.BoolProperty(default=False)
    ICON_LIGHT_PANEL_Aim: bpy.props.BoolProperty(default=False)
    ICON_LIGHT_PANEL_Color: bpy.props.BoolProperty(default=True)
    ICON_LIGHT_PANEL_Pin_Icon: bpy.props.BoolProperty(default=False)
    ICON_LIGHT_PANEL_Tags_Icon: bpy.props.BoolProperty(default=False)

    SHOW_TAGS_Icon_Expose: bpy.props.BoolProperty()

    ICON_TAGS_Select: bpy.props.BoolProperty(default=True)
    ICON_TAGS_Hide_Viewport: bpy.props.BoolProperty(default=True)
    ICON_TAGS_Hide_Render: bpy.props.BoolProperty(default=False)
    ICON_TAGS_Hide_Select: bpy.props.BoolProperty(default=False)
    ICON_TAGS_Remove: bpy.props.BoolProperty(default=True)
    ICON_TAGS_Set_Property: bpy.props.BoolProperty(default=True)
    ICON_TAGS_Adjust_Strength_And_Color: bpy.props.BoolProperty(default=True)

    BUTTONS_Display_All: bpy.props.BoolProperty(default=False)
    BUTTONS_Show_Transform_Button: bpy.props.BoolProperty(default=False)

    BUTTONS_Show_Add_Raymesh_Light_Button: bpy.props.BoolProperty(default=True)

    BUTTONS_Expose_Custom_Properties: bpy.props.BoolProperty(default=True)

    ENABLE_Tags: bpy.props.BoolProperty(default=True)
    ENABLE_Add_Menu: bpy.props.BoolProperty(default=True)


    def draw_general(self, context, layout):

        col = layout.column(align=True)

        col.label(text="Panels")
        col.prop(self, "PANEL_Light_Panel", text="Light Panel")
        if self.PANEL_Light_Panel:

            col.prop(self, "PANEL_Light_Panel_Category", text="Category")
            col.prop(self, "PANEL_Light_Panel_Label", text="Label")

        col.separator()

        col.prop(self, "PANEL_Render_Settings_Panel", text="Render Settings Panel")
        if self.PANEL_Render_Settings_Panel:

            col.prop(self, "PANEL_Render_Settings_Panel_Category", text="Category")
            col.prop(self, "PANEL_Render_Settings_Panel_Label", text="Label")


        col.separator()

        col.prop(self, "PANEL_Active_Light_Properties_Panel", text="Active Light Properties")
        if self.PANEL_Render_Settings_Panel:

            col.prop(self, "PANEL_Active_Light_Properties_Panel_Category", text="Category")
            col.prop(self, "PANEL_Active_Light_Properties_Panel_Label", text="Label")


        col.separator()

        col.prop(self, "PANEL_Radiant_Tools_Panel", text="Active Light Properties")
        if self.PANEL_Render_Settings_Panel:

            col.prop(self, "PANEL_Radiant_Tools_Panel_Category", text="Category")
            col.prop(self, "PANEL_Radiant_Tools_Panel_Label", text="Label")








        col.separator()
        col.prop(self, "BUTTONS_Display_All", text="Display / Lock All Light Buttons")
        col.prop(self, "BUTTONS_Show_Add_Raymesh_Light_Button", text="Show Add Raymesh Light Buttons at Light Manager")
        col.prop(self, "BUTTONS_Show_Transform_Button", text="Show Transform Buttons")
        col.prop(self, "BUTTONS_Expose_Custom_Properties", text="Show Custom Properties in Light Manager")
        col.prop(self, "Hide_Raymesh_Button_After_Make", text="Hide Make Raymesh Button after Creation")




        col.separator()

        col.prop(self, "ENABLE_Tags", text="Enable Tags")
        col.prop(self, "ENABLE_Add_Menu", text="Enable Radiant in Add Menu")



    def draw_hotkey(self, context, layout):

        layout.label(text="3D View")
        kc = context.window_manager.keyconfigs.user
        km = kc.keymaps['3D View']
        keymap_items = km.keymap_items

        kmi = get_menu(km, 'wm.call_menu', 'RADIANT_MT_radiant_menu')
        kmi.show_expanded = False

        rna_keymap_ui.draw_kmi([], kc, km, kmi, layout, 0)





    def draw(self, context):

        layout = self.layout

        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(self, "TABS_Preferences", expand=True)

        box = col.box()

        if self.TABS_Preferences == "GENERAL":
            self.draw_general(context, box)
        if self.TABS_Preferences == "KEYMAPS":
            self.draw_hotkey(context, box)

classes = [Radiant_user_preferences]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    update_panel(None, bpy.context)

def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
