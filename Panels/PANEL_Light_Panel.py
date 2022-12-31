import bpy
import bpy_extras
from Radiant import Utility_Functions
import rna_prop_ui
#Create Light From Selected

class RADIANT_PT_Light_Panel(bpy.types.Panel):
    """Panels for Manage Lights"""
    bl_label = "Light Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Radiant"

    @classmethod
    def poll(cls, context):
        preferences = Utility_Functions.get_addon_preferences()
        return preferences.PANEL_Light_Panel

    def get_filtered_lights(self, context):

        lights = []

        scn = context.scene
        scn_properties = scn.Radiant_Light_Properties
        object = context.object

        objects = context.view_layer.objects
        Pinned_Objects = [object for object in objects if object.type == "LIGHT" and object.Radiant_Light_Properties.Pin]

        if scn_properties.Light_Filter == "ALL":
            objects = context.view_layer.objects
            lights = [object for object in objects if object.type == "LIGHT"]

        if scn_properties.Light_Filter == "SELECTED":
            objects = context.selected_objects
            lights = [object for object in objects if object.type == "LIGHT"]

        if scn_properties.Light_Filter == "NAME":
            objects = context.selected_objects
            lights = [object for object in objects if object.type == "LIGHT" and scn_properties.Light_Filter_Name in object.name]

        if scn_properties.Light_Filter == "ACTIVE":
            if object:
                if object.type == "LIGHT":
                    lights = [object]

        if scn_properties.Light_Filter == "COLLECTION":

            collection = bpy.data.collections.get(scn_properties.Light_Filter_Collection)

            if collection:
                lights = [object for object in context.view_layer.objects if object.type == "LIGHT" and collection.objects.get(object.name)]
            else:
                lights = []

        if scn_properties.Light_Filter == "TAGS":

            lights = [object for object in context.view_layer.objects if object.type == "LIGHT" and object.Radiant_Light_Properties.Tags == scn_properties.Light_Filter_Tags]

        if scn_properties.Light_Filter == "PINNED":
            lights = []

        if scn_properties.Light_Filter == "TYPE":
            lights = []
            for object in context.view_layer.objects:
                if object.type == "LIGHT":
                    if object.data.type == scn_properties.Light_Filter_Type:
                        lights.append(object)


        sorted_list = list(dict.fromkeys(Pinned_Objects+lights))


        if scn_properties.Move_Selected_to_Top:
            for selected in context.selected_objects:
                if selected in sorted_list:
                    sorted_list.remove(selected)
                    sorted_list.insert(0, selected)

            if context.active_object:
                if context.active_object.select_get():
                    if context.active_object in sorted_list:
                        sorted_list.remove(context.active_object)
                        sorted_list.insert(0, context.active_object)


        if not scn_properties.Light_Filter_Name == "":
            sorted_list = [object for object in objects if scn_properties.Light_Filter_Name.lower() in object.name.lower() and object.type=="LIGHT"]


        return sorted_list

    def draw_icon_expose(self, context, layout):
        preferences = Utility_Functions.get_addon_preferences()
        row = layout.row(align=True)
        row.alignment = "LEFT"

        if Utility_Functions.draw_subpanel(preferences, preferences.SHOW_LIGHT_PANEL_Icon_Expose, "SHOW_LIGHT_PANEL_Icon_Expose", "Icon Expose", layout):

            layout.prop(preferences, "ICON_LIGHT_PANEL_Light_Icon", text="Light Icon")
            layout.prop(preferences, "ICON_LIGHT_PANEL_Pin_Icon", text="Pin")
            layout.prop(preferences, "ICON_LIGHT_PANEL_Link_Make_Single_Icon", text="Link Make Single")
            layout.prop(preferences, "ICON_LIGHT_PANEL_Solo", text="Solo")
            layout.prop(preferences, "ICON_LIGHT_PANEL_Select", text="Select")
            layout.prop(preferences, "ICON_LIGHT_PANEL_Find", text="Find")
            layout.prop(preferences, "ICON_LIGHT_PANEL_Light_Type", text="Light Type")
            if preferences.ENABLE_Tags:
                layout.prop(preferences, "ICON_LIGHT_PANEL_Tags_Icon", text="Tags")
            layout.prop(preferences, "ICON_LIGHT_PANEL_Lock_Select", text="Lock Select")
            layout.prop(preferences, "ICON_LIGHT_PANEL_Hide_Viewport", text="Hide Viewport")
            layout.prop(preferences, "ICON_LIGHT_PANEL_Hide_Render", text="Hide Render")
            layout.prop(preferences, "ICON_LIGHT_PANEL_Duplicate", text="Duplicate")
            layout.prop(preferences, "ICON_LIGHT_PANEL_Remove", text="Remove")
            layout.prop(preferences, "ICON_LIGHT_PANEL_Move", text="Move")
            layout.prop(preferences, "ICON_LIGHT_PANEL_Rotate", text="Rotate")
            layout.prop(preferences, "ICON_LIGHT_PANEL_Aim", text="Aim")
            layout.prop(preferences, "ICON_LIGHT_PANEL_Color", text="Color")
            layout.prop(preferences, "ICON_LIGHT_PANEL_Hide_Children", text="Hide Children")





    def draw_tag_icon_expose(self, context, layout):
        preferences = Utility_Functions.get_addon_preferences()
        row = layout.row(align=True)
        row.alignment = "LEFT"

        if Utility_Functions.draw_subpanel(preferences, preferences.SHOW_TAGS_Icon_Expose, "SHOW_TAGS_Icon_Expose", "Icon Expose", layout):

            layout.prop(preferences, "ICON_TAGS_Select", text="Select")
            layout.prop(preferences, "ICON_TAGS_Hide_Viewport", text="Hide Viewport")
            layout.prop(preferences, "ICON_TAGS_Hide_Render", text="Hide Render")
            layout.prop(preferences, "ICON_TAGS_Hide_Select", text="Select Lock")
            # layout.prop(preferences, "ICON_TAGS_Set_Property", text="Set Property")
            layout.prop(preferences, "ICON_TAGS_Remove", text="Remove Tag")
            layout.prop(preferences, "ICON_TAGS_Adjust_Strength_And_Color", text="Adjust Strength and Color")

    def draw_display_all_operator(self, context, layout):

        preferences = Utility_Functions.get_addon_preferences()

        if preferences.BUTTONS_Display_All:
            row = layout.row(align=True)
            row.operator("radiant.unhide_all_light", text="Hide All", icon="HIDE_ON").state = True
            row.operator("radiant.unhide_all_light", text="Unhide All", icon="HIDE_OFF").state = False

            row = layout.row(align=True)
            row.operator("radiant.unlock_all_light", text="Lock All", icon="LOCKED").state = True
            row.operator("radiant.unlock_all_light", text="Unlock All", icon="UNLOCKED").state = False

    def draw_light_filter_options(self, context, layout):

        scn = context.scene
        scn_properties = scn.Radiant_Light_Properties

        # layout.label(text="Light Panel")

        layout.prop(scn_properties, "Light_Filter", text="Filter")

        layout.prop(scn_properties, "Light_Filter_Name", text="", icon="VIEWZOOM")

        if scn_properties.Light_Filter == "NAME":
            layout.prop(scn_properties, "Light_Filter_Name", text="")

        if scn_properties.Light_Filter == "COLLECTION":
            layout.prop_search(scn_properties, "Light_Filter_Collection", bpy.data, "collections", text="")

        if scn_properties.Light_Filter == "TAGS":
            if len(scn_properties.Tags_List) == 0:
                col = layout.column(align=True)
                Operator = col.operator("radiant.tag_selected_lights", text="New Tag From Selected", icon="PLUS")
                Operator.mode = "ASSIGN_NEW"

            else:
                col = layout.column(align=True)
                row = col.row(align=True)

                row.prop_search(scn_properties, "Light_Filter_Tags", scn_properties, "Tags_List", text="")

                Operator = row.operator("radiant.tag_selected_lights", text="", icon="PLUS")
                Operator.mode = "ASSIGN_NEW"

                row = col.row(align=True)

                Operator = row.operator("radiant.tag_selected_lights", text="Assign", icon="ADD")
                Operator.mode = "ASSIGN"
                Operator.tag = scn_properties.Light_Filter_Tags

                Operator = row.operator("radiant.tag_selected_lights", text="Unassign", icon="REMOVE")
                Operator.mode = "UNASSIGN"


        if scn_properties.Light_Filter == "TYPE":
            layout.prop(scn_properties, "Light_Filter_Type", expand=True)

        layout.prop(scn_properties, "Hide_Linked_Duplicates", expand=True, text="Hide Linked Duplicates")

    def draw_tag_list(self, context, layout):

        scn = context.scene
        scn_properties = scn.Radiant_Light_Properties

        col = layout.column(align=True)

        if Utility_Functions.draw_subpanel(scn_properties, scn_properties.Show_Tag_List, "Show_Tag_List", "Tag List", col):

            row = col.row(align=True)
            row.template_list("RADIANT_UL_Tag_List", "", scn_properties, "Tags_List", scn_properties, "Tags_List_Index")

            row2 = col.row(align=True)
            operator = row2.operator("radiant.tags_list_operator", text="Assign", icon="ADD")
            operator.operation = "ASSIGN"

            operator = row2.operator("radiant.tags_list_operator", text="Unassign", icon="REMOVE")
            operator.operation = "UNASSIGN"

            index = scn_properties.Tags_List_Index

            col = row.column(align=True)
            operator = col.operator("radiant.tags_list_operator", text="", icon="ADD")
            operator.operation = "ADD"
            operator.index = index

            operator = col.operator("radiant.tags_list_operator", text="", icon="REMOVE")
            operator.operation = "REMOVE"
            operator.index = index

            operator = col.operator("radiant.tags_list_operator", text="", icon="TRIA_UP")
            operator.operation = "UP"
            operator.index = index

            operator = col.operator("radiant.tags_list_operator", text="", icon="TRIA_DOWN")
            operator.operation = "DOWN"
            operator.index = index


            self.draw_tag_icon_expose(context, layout)

    def draw_light_list(self, context, layout, lights):

        scn = context.scene
        scn_properties = scn.Radiant_Light_Properties
        preferences = Utility_Functions.get_addon_preferences()

        light_data_check = {}

        for light_object in lights:
            if light_object.data in light_data_check:
                light_data_check[light_object.data] += 1
            else:
                light_data_check[light_object.data] = 1


        light_data_track = []
        

        for light_object in lights:

            hide = False

            if scn_properties.Hide_Linked_Duplicates:
                if light_object.data in light_data_track:
                    continue

            light_data_track.append(light_object.data)

            light = light_object.data


            box = layout.box()
            col = box.column(align=True)

            is_linked = False

            if light_data_check.get(light) > 1:
                is_linked = True
            
            self.draw_light_list_header(context, light_object, col, is_linked)
            self.draw_light_list_settings(context, light_object, col)

        col = layout.column(align=True)

        if len(lights) == 0:
            col.label(text="No Lights Found", icon="INFO")
            col.separator()

        row = col.row(align=True)

        row = col.row(align=True)
        Operator = row.operator("radiant.listed_light_operator", text="Select", icon="RESTRICT_SELECT_OFF")
        Operator.operation = "SELECT"

        Operator = row.operator("radiant.listed_light_operator", text="Hide", icon="RESTRICT_VIEW_OFF")
        Operator.operation = "HIDE"

        Operator = row.operator("radiant.listed_light_operator", text="", icon="PROPERTIES")
        Operator.operation = "ADJUST"

        col = layout.column(align=True)
        row = col.row(align=True)

        row = layout.row(align=True)
        row.alignment = "LEFT"

        if context.mode == "OBJECT":
            add_operator = row.operator("radiant.add_light", icon="ADD")

            # if preferences.BUTTONS_Show_Add_Raymesh_Light_Button:
            #
            #     layout.separator()
            #     layout.label(text="Raymesh")
            #     layout = layout.row()
            #     add_operator = layout.operator("radiant.add_raymesh_light_as_driver", text="Add Raymesh Light", icon="LIGHT_HEMI")
            #     add_operator.invoke_prop = True

    def draw_light_list_header(self, context, object, layout, is_linked):

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

        if obj_properties.Show_Light_Settings:
            icon_arrow = "DISCLOSURE_TRI_DOWN"
        else:
            icon_arrow = "DISCLOSURE_TRI_RIGHT"

        row.prop(obj_properties, "Show_Light_Settings", icon=icon_arrow, text="", emboss=False)

        if preferences.ICON_LIGHT_PANEL_Light_Icon:
            row.label(text="", icon="LIGHT_" + light.type)




        if preferences.ICON_LIGHT_PANEL_Pin_Icon:
            row.prop(obj_properties, "Pin", text="", icon="PINNED")

        if preferences.ICON_LIGHT_PANEL_Link_Make_Single_Icon:
            if is_linked:
                operator = row.operator("radiant.make_unique",text="", icon="LINKED")
                operator.object = light_object.name


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

        if light_object == context.active_object:
            if light_object.select_get():
                row.prop(light_object, "name", text="", icon="KEYTYPE_JITTER_VEC")
            else:
                row.prop(light_object, "name", text="")

        else:
            if light_object in context.selected_objects:
                row.prop(light_object, "name", text="", icon="RESTRICT_SELECT_OFF")
            else:
                row.prop(light_object, "name", text="")

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

    def draw_light_list_settings(self, context, object, layout):

        scn = context.scene
        scn_properties = scn.Radiant_Light_Properties

        preferences = Utility_Functions.get_addon_preferences()

        light_object = object
        light = light_object.data
        col = layout

        object_radiant_settings = light_object.Radiant_Light_Properties

        active_light = scn_properties.Expand_Active_Light and light_object == context.active_object


        if object_radiant_settings.Show_Light_Settings or active_light:

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
        # if object_radiant_settings.Show_Light_Advanced_Option:



            if not light.type in ["SUN"]:

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
                    #     col.prop(light, "shape", text="Shape")
                    #     col.prop(light, "size", text="Size X")
                    #
                    #     if not light.shape in ["SQUARE", "DISK"]:
                    #         col.prop(light, "size_y", text="Size Y")
                    #

                        # if context.scene.render.engine == "CYCLES":
                        #     col.separator()
                        #     col.prop(light, "spread", text="Spread")



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
                    col.separator()

                    if light_object.data.use_shadow:

                        col.prop(light_object.data, "use_contact_shadow", text="Contact Shadow")

                        col.prop(light_object.data, "contact_shadow_distance", text="Distance")
                        col.prop(light_object.data, "contact_shadow_bias", text="Bias")
                        col.prop(light_object.data, "contact_shadow_thickness", text="Thickness")



            col.separator()

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

                Show_Button = True

                if preferences.Hide_Raymesh_Button_After_Make:
                    if light_object.data.Disable_Make_Raymesh_Button:
                        Show_Button = False

                if Show_Button:
                    if light_object.data.type in ["SPOT", "POINT", "AREA"]:
                        col.separator()
                        operator = col.operator("radiant.make_raymesh_from_light", text="Make Raymesh", icon="LIGHT_HEMI")
                        operator.light_object = light_object.name
                        col.separator()


            if preferences.ENABLE_Tags:
                row = col.row(align=True)
                row.prop_search(object_radiant_settings, "Tags", scn_properties, "Tags_List", text="Tags:")


            col.separator()


            if preferences.BUTTONS_Expose_Custom_Properties:



                data_custom_properties = Utility_Functions.get_user_defined_custom_properties(light_object.data)
                custom_properties = Utility_Functions.get_user_defined_custom_properties(light_object)

                if len(custom_properties) > 0:

                    if Utility_Functions.draw_subpanel(object_radiant_settings, object_radiant_settings.Show_Object_Custom_Properties, "Show_Object_Custom_Properties", "Object Custom Properties", col):
                        cpbox = col.box()
                        col.separator()
                        for p in custom_properties:
                            property = rna_prop_ui.rna_idprop_quote_path(p)
                            cpbox.prop(light_object, property)

                col.separator()

                if len(data_custom_properties) > 0:

                    if Utility_Functions.draw_subpanel(object_radiant_settings, object_radiant_settings.Show_Light_Custom_Properties, "Show_Light_Custom_Properties", "Light Custom Properties", col):
                        cpbox = col.box()
                        col.separator()
                        for p in data_custom_properties:
                            property = rna_prop_ui.rna_idprop_quote_path(p)
                            cpbox.prop(light_object.data, property)




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

        if bpy.context.scene.render.engine == "CYCLES":

            col.prop(light.cycles, "is_portal", text="Portal")
            col.separator()

        if bpy.context.scene.render.engine == "CYCLES":

            col.prop(light.cycles, "max_bounces", text="Max Bounces")
            col.prop(light.cycles, "use_multiple_importance_sampling", text="Multiple Importance")



    def draw_light_node_standard(self, object, light, layout):

        node = light.node_tree.get_output_node('CYCLES')

        if node:

            input = bpy_extras.node_utils.find_node_input(node, "Surface")

            if input:
                layout.template_node_view(light.node_tree, node, input)
            else:
                layout.label(text="Incompatible output node")
        else:
            layout.label(text="No output node")

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

    def draw(self, context):

        layout = self.layout

        scn = context.scene
        scn_properties = scn.Radiant_Light_Properties

        preferences = Utility_Functions.get_addon_preferences()

        object = context.object

        lights = self.get_filtered_lights(context)

        self.draw_display_all_operator(context, layout)

        self.draw_light_filter_options(context, layout)

        row= layout.row(align=True)
        row.prop(scn_properties, "Move_Selected_to_Top", text="Selected To Top")
        row.prop(scn_properties, "Expand_Active_Light", text="Expand Active")



        self.draw_light_list(context, layout, lights)

        self.draw_icon_expose(context, layout)

        if preferences.ENABLE_Tags:

            self.draw_tag_list(context, layout)










classes = [RADIANT_PT_Light_Panel]


def register():

    for cls in classes:

        bpy.utils.register_class(cls)



def unregister():
    for cls in classes:

        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
