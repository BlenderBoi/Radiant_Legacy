import bpy

from Radiant import Utility_Functions
import rna_prop_ui


class RADIANT_PT_Active_Light_Properties_Panel(bpy.types.Panel):
    """Active Light Properties"""
    bl_label = "Active Light Properties"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Radiant"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        preferences = Utility_Functions.get_addon_preferences()
        if preferences.PANEL_Active_Light_Properties_Panel:
            object = context.object
            if object:
                if object.type == "LIGHT":
                    return True

    def draw(self, context):

        layout = self.layout
        object = context.object
        if object:
            if object.type == "LIGHT":
                self.draw_light_list_header(context, object, layout)
                self.draw_light_settings(context, object, layout)

    def draw_basic_light_properties(self, object, layout):

        object_radiant_settings = object.Radiant_Light_Properties
        light = object.data

        row = layout.row(align=True)

        row.scale_y = 1.5


        col = row.column(align=True)


        col.prop(light, "energy")

        if light.type == "POINT":
            col.prop(light, "shadow_soft_size")

        if light.type == "SPOT":
            col.prop(light, "shadow_soft_size")

        if light.type == "SUN":
            col.prop(light, "angle")

        row2 = row.row(align=True)
        row2.alignment = "RIGHT"

        if not object_radiant_settings.Use_Blackbody:
            row2.prop(light, "color", text="")


        if object_radiant_settings.Use_Blackbody:

            row2.prop(light, "color", text="")
            row2.prop(object_radiant_settings, "Blackbody_Temperature", text="")

        row2.prop(object_radiant_settings, "Use_Blackbody", icon="TEMP", text="")

        if bpy.context.scene.render.engine == "CYCLES":
            if light.type == "AREA":
                col.prop(light, "spread", text="Spread")


        layout.separator()

        col = layout.column()
        col.scale_y = 1.2
        if light.type == "SPOT":
            row = col.row(align=True)
            row.prop(light, "spot_size", text="Spot Size")
            row.prop(light, "spot_blend", text="Spot Blend")
            col.prop(light, "show_cone", text="Show Cone")
            col.separator()

        if light.type == "AREA":

            col.prop(light, "shape", text="")
            row = col.row(align=True)
            row.prop(light, "size", text="Size X")

            if not light.shape in ["SQUARE", "DISK"]:
                row.prop(light, "size_y", text="Size Y")



    def draw_node_properties(self, context, object, layout):

        col = layout
        light = object.data
        light_object = object
        object_radiant_settings = object.Radiant_Light_Properties

        if context.scene.render.engine == "CYCLES":

            row = col.row(align=True)
            row.prop(light, "use_nodes", icon="NODETREE")

            if light.use_nodes:
                if Utility_Functions.draw_subpanel_style02(object_radiant_settings, object_radiant_settings.Show_Node_Properties, "Show_Node_Properties", "", row):

                    row = col.row(align=True)

                    box = col.box()

                    self.draw_light_node_standard(light_object, light, box)

                row_box = col.row(align=True)
                row_box.scale_y = 2
                operator = row_box.operator("radiant.open_shader_editor", icon="NODE_MATERIAL")
                operator.object = light_object.name
                #
                # operator = row_box.operator("radiant.node_tool_callers", text="", icon="DOWNARROW_HLT")
                # operator.object = light_object.name

    def draw_light_settings(self, context, object, layout):

        scn = context.scene
        scn_properties = scn.Radiant_Light_Properties

        preferences = Utility_Functions.get_addon_preferences()

        light_object = object
        light = light_object.data
        col = layout

        object_radiant_settings = light_object.Radiant_Light_Properties

        col.separator()

        row = col.row(align=True)
        row.prop(light, "type", expand=True)

        col.separator()
        row = col.row(align=True)

        if context.scene.render.engine == "CYCLES":

            row.prop(object_radiant_settings, "Tab_Properties_Display", expand=True)

            if object_radiant_settings.Tab_Properties_Display == "PROPERTIES":

                self.draw_basic_light_properties(light_object, col)

            if object_radiant_settings.Tab_Properties_Display == "NODE":

                self.draw_node_properties(context, light_object, col)

        else:

            self.draw_basic_light_properties(light_object, col)

        # col.separator()

    #     col.prop(object_radiant_settings, "Show_Light_Advanced_Option", text="Advanced")
    #
    #   if object_radiant_settings.Show_Light_Advanced_Option:


        if not light.type in ["POINT", "SUN"]:

            # if Utility_Functions.draw_subpanel(object_radiant_settings, object_radiant_settings.Show_Light_Shape, "Show_Light_Shape", "Shape", col):

            if context.scene.render.engine == "BLENDER_EEVEE":

                col.prop(light, "use_custom_distance", text="Custom Distance")

            if light.use_custom_distance:

                col.prop(light, "cutoff_distance", text="Distance")

                col.separator()

                # if light.type == "SPOT":
                #
                #     col.prop(light, "spot_size", text="Spot Size")
                #     col.prop(light, "spot_blend", text="Spot Blend")
                #     col.prop(light, "show_cone", text="Show Cone")
                #
                # if light.type == "AREA":
                #
                #     col.prop(light, "size", text="Size X")
                #
                #     if not light.shape in ["SQUARE", "DISK"]:
                #         col.prop(light, "size_y", text="Size Y")
                #         col.prop(light, "shape", text="Shape")
                #
                #     if context.scene.render.engine == "CYCLES":
                #         col.separator()
                #         col.prop(light, "spread", text="Spread")

        # col.separator()



        if context.scene.render.engine == "BLENDER_EEVEE":

            if Utility_Functions.draw_subpanel(object_radiant_settings, object_radiant_settings.Show_Light_Factor, "Show_Light_Factor", "Factor", col):

                if object_radiant_settings.Show_Light_Factor:

                    col.prop(light, "diffuse_factor")
                    col.prop(light, "specular_factor")
                    col.prop(light, "volume_factor")



        if Utility_Functions.draw_subpanel(object_radiant_settings, object_radiant_settings.Show_Light_Transform, "Show_Light_Transform", "Transform", col):

            col.prop(light_object, "location")
            col.operator("radiant.move_light", text="", icon="EMPTY_ARROWS").object = light_object.name

            col.separator()

            col.prop(light_object, "rotation_euler", text="Rotation")
            col.operator("radiant.trackball_light", text="", icon="ORIENTATION_GIMBAL").object = light_object.name

        if Utility_Functions.draw_subpanel(object_radiant_settings, object_radiant_settings.Show_Light_Shadow, "Show_Light_Shadow", "Shadow", col):

            if context.scene.render.engine == "CYCLES":
                col.prop(light.cycles, "cast_shadow", text="Cast Shadow")

            if context.scene.render.engine == "BLENDER_EEVEE":

                col.prop(light_object.data, "use_shadow", text="Shadow")

                if not light.type == "SUN":
                    col.prop(light, "shadow_buffer_clip_start", text="Clip Start")

                col.prop(light, "shadow_buffer_bias", text="Bias")

                col.separator()
                # col.separator()

                if light_object.data.use_shadow:

                    col.prop(light_object.data, "use_contact_shadow", text="Contact Shadow")

                    col.prop(light_object.data, "contact_shadow_distance", text="Distance")
                    col.prop(light_object.data, "contact_shadow_bias", text="Bias")
                    col.prop(light_object.data, "contact_shadow_thickness", text="Thickness")




        row = col.row(align=True)

        row.alignment = "EXPAND"

        row.scale_y = 1

        if context.mode == "OBJECT":

            if preferences.BUTTONS_Show_Transform_Button:
                row.scale_x = 2
                row.scale_y = 2
                row.operator("radiant.move_light", text="Move", icon="EMPTY_ARROWS").object = light_object.name
                row.operator("radiant.trackball_light", text="Rotate", icon="ORIENTATION_GIMBAL").object = light_object.name
                row.operator("radiant.aim_light", text="Aim", icon="CON_TRACKTO").object = light_object.name

            if len(light_object.constraints) > 0:

                col.separator()

                row = col.row(align=True)
                row.alignment = "LEFT"
                row.operator("radiant.apply_light_constraint", text="Apply Constraint", icon="CONSTRAINT").object = light_object.name

        if preferences.BUTTONS_Show_Add_Raymesh_Light_Button:

            if not light_object.data.Disable_Make_Raymesh_Button:
                if light_object.data.type in ["SPOT", "POINT", "AREA"]:

                    operator = col.operator("radiant.make_raymesh_from_light", text="Make Raymesh", icon="LIGHT_HEMI")
                    operator.light_object = light_object.name
                    col.separator()




        if preferences.ENABLE_Tags:
            row = col.row(align=True)
            row.prop_search(object_radiant_settings, "Tags", scn_properties, "Tags_List", text="Tags:")


        # col.separator()


        if preferences.BUTTONS_Expose_Custom_Properties:

            data_custom_properties = Utility_Functions.get_user_defined_custom_properties(light_object.data)

            custom_properties = Utility_Functions.get_user_defined_custom_properties(light_object)
            if len(custom_properties) > 0:

                if Utility_Functions.draw_subpanel(object_radiant_settings, object_radiant_settings.Show_Object_Custom_Properties, "Show_Object_Custom_Properties", "Object Custom Properties", col):
                    cpbox = col.box()
                    # col.separator()
                    for p in custom_properties:
                        property = rna_prop_ui.rna_idprop_quote_path(p)
                        cpbox.prop(light_object, property)

            if len(data_custom_properties) > 0:

                if Utility_Functions.draw_subpanel(object_radiant_settings, object_radiant_settings.Show_Light_Custom_Properties, "Show_Light_Custom_Properties", "Light Custom Properties", col):
                    cpbox = col.box()
                    # col.separator()
                    for p in data_custom_properties:
                        property = rna_prop_ui.rna_idprop_quote_path(p)
                        cpbox.prop(light_object.data, property)

    def draw_light_list_header(self, context, object, layout):

        scn = context.scene
        scn_properties = scn.Radiant_Light_Properties

        preferences = Utility_Functions.get_addon_preferences()

        light_object = object
        light = light_object.data

        col = layout
        # col.scale_x = 1.5
        # col.scale_y = 1.5
        row = col.row(align=True)

        obj_properties = light_object.Radiant_Light_Properties



        # if obj_properties.Show_Light_Settings:
        #     icon_arrow = "DISCLOSURE_TRI_DOWN"
        # else:
        #     icon_arrow = "DISCLOSURE_TRI_RIGHT"
        #
        # row.prop(obj_properties, "Show_Light_Settings", icon=icon_arrow, text="", emboss=False)

        if preferences.ICON_LIGHT_PANEL_Light_Icon:
            row.label(text="", icon="LIGHT_" + light.type)

        if preferences.ICON_LIGHT_PANEL_Pin_Icon:
            row.prop(obj_properties, "Pin", text="", icon="PINNED")





        if preferences.ICON_LIGHT_PANEL_Solo:
            row.operator("radiant.solo_light", icon="SOLO_ON", text="").object = light_object.name

        if preferences.ICON_LIGHT_PANEL_Select:
            if context.mode == "OBJECT":
                row.operator("radiant.select_light", icon="RESTRICT_SELECT_OFF", text="").object = light_object.name

        if preferences.ICON_LIGHT_PANEL_Find:
            if context.mode == "OBJECT":
                row.operator("radiant.find_light", icon="VIEWZOOM", text="").object = light_object.name

        if preferences.ICON_LIGHT_PANEL_Move:
            if context.mode == "OBJECT":
                row.operator("radiant.move_light", text="", icon="EMPTY_ARROWS").object = light_object.name

        if preferences.ICON_LIGHT_PANEL_Rotate:

            if context.mode == "OBJECT":
                row.operator("radiant.trackball_light", text="", icon="ORIENTATION_GIMBAL").object = light_object.name

        if preferences.ICON_LIGHT_PANEL_Aim:

            if context.mode == "OBJECT":
                row.operator("radiant.aim_light", text="", icon="CON_TRACKTO").object = light_object.name

        # if light_object == context.active_object:
        #     if light_object.select_get():
        #         row.prop(light_object, "name", text="", icon="KEYTYPE_JITTER_VEC")
        #     else:
        row.prop(light_object, "name", text="")

        # else:
        #     if light_object in context.selected_objects:
        #         row.prop(light_object, "name", text="", icon="RESTRICT_SELECT_OFF")
        #     else:
        #         row.prop(light_object, "name", text="")

        row = row.row(align=True)
        row.alignment = "RIGHT"

        if preferences.ENABLE_Tags:
            if preferences.ICON_LIGHT_PANEL_Tags_Icon:
                row.prop_search(obj_properties, "Tags", scn_properties, "Tags_List", text="", icon="PMARKER_ACT")

        if preferences.ICON_LIGHT_PANEL_Light_Type:
            row.prop(light, "type", text="")

        if preferences.ICON_LIGHT_PANEL_Color:
            row.prop(light, "color", text="")



        if preferences.ICON_LIGHT_PANEL_Lock_Select:
            if light_object.hide_select:
                row.prop(light_object, "hide_select", text="", icon="UNPINNED")

            else:
                row.prop(light_object, "hide_select", text="", icon="UNLOCKED")



        if preferences.ICON_LIGHT_PANEL_Hide_Children:

            check_child = [child for child in light_object.children]

            if len(check_child) > 0:

                check_viewport = all([not child.hide_viewport for child in light_object.children])
                check_render = all([not child.hide_render for child in light_object.children])
                check_hide = all([not child.hide_get() for child in light_object.children])

                icon = None

                if check_viewport and check_render and check_hide:
                    icon = "OUTLINER_OB_POINTCLOUD"
                else:
                    icon = "OUTLINER_DATA_POINTCLOUD"

                if icon:
                    operator = row.operator("radiant.hide_light_children", text="", icon=icon)
                    operator.object = light_object.name

        if preferences.ICON_LIGHT_PANEL_Hide_Viewport:
            row.prop(light_object, "hide_viewport", text="")

        if preferences.ICON_LIGHT_PANEL_Hide_Render:
            row.prop(light_object, "hide_render", text="")

        if preferences.ICON_LIGHT_PANEL_Duplicate:
            if context.mode == "OBJECT":
                row.operator("radiant.duplicate_light", text="", icon="DUPLICATE").object = light_object.name

        if preferences.ICON_LIGHT_PANEL_Remove:
            row.operator("radiant.remove_light", icon="X", text="", emboss=False).object = light_object.name








classes = [RADIANT_PT_Active_Light_Properties_Panel]


def register():
  for cls in classes:
    bpy.utils.register_class(cls)


def unregister():
  for cls in classes:
    bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
