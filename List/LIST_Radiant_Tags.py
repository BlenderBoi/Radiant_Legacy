import bpy
from Radiant import Utility_Functions

class RADIANT_UL_Tag_List(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):

        preferences = Utility_Functions.get_addon_preferences()

        row = layout.row(align=True)

        if preferences.ICON_TAGS_Select:
            Operator = row.operator("radiant.select_tagged_lights", text="", icon="RESTRICT_SELECT_OFF")
            Operator.index = index



        row.prop(item, "name", emboss=False, text="")

        if preferences.ICON_TAGS_Hide_Viewport:
            Operator = row.operator("radiant.set_hide_tagged_lights", text="", icon="RESTRICT_VIEW_OFF")
            Operator.index = index
            Operator.mode = "VIEWPORT"

        if preferences.ICON_TAGS_Hide_Render:
            Operator = row.operator("radiant.set_hide_tagged_lights", text="", icon="RESTRICT_RENDER_OFF")
            Operator.index = index
            Operator.mode = "RENDER"

        if preferences.ICON_TAGS_Hide_Select:
            Operator = row.operator("radiant.set_hide_tagged_lights", text="", icon="LOCKED")
            Operator.index = index
            Operator.mode = "LOCK"

        # if preferences.ICON_TAGS_Set_Property:
        #     Operator = row.operator("radiant.set_tagged_lights_property", text="", icon="PROPERTIES")
        #     Operator.index = index

        if preferences.ICON_TAGS_Adjust_Strength_And_Color:
            Operator = row.operator("radiant.adjust_strength_and_color_tagged_lights", text="", icon="PROPERTIES")
            Operator.index = index




        if preferences.ICON_TAGS_Remove:
            Operator = row.operator("radiant.tags_list_operator", text="", icon="X")
            Operator.operation = "REMOVE"
            Operator.index = index

classes = [RADIANT_UL_Tag_List]

def register():

    for cls in classes:

        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:

        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
