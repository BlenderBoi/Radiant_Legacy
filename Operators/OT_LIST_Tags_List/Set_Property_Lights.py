import bpy
from Radiant import Utility_Functions

ENUM_Area_Shape = [("SQUARE","Square","Square"),("RECTANGLE","Rectangle","Rectangle"),("DISK","Disk","Disk"),("ELLIPSE","Ellipse","Ellipse")]

class Radiant_OT_Set_Property_Tagged_Lights(bpy.types.Operator):
    """Set Lights Property"""
    bl_idname = "radiant.set_tagged_lights_property"
    bl_label = "Set Tagged Light Property"
    bl_options = {'REGISTER', 'UNDO'}

    Strength: bpy.props.FloatProperty(default=1.0)
    Color: bpy.props.FloatVectorProperty(subtype="COLOR", default=(1, 1, 1))
    index: bpy.props.IntProperty()

    POINT_SPOT_Shadow_Soft_Size: bpy.props.FloatProperty()


    SHOW_Point_Spot_Light: bpy.props.BoolProperty()
    Use_Point_Spot_Light: bpy.props.BoolProperty()

    SHOW_Sun_Light: bpy.props.BoolProperty()
    Use_Sun_Light: bpy.props.BoolProperty()

    SUN_Angle: bpy.props.FloatProperty()

    SHOW_Spot_Light: bpy.props.BoolProperty()
    Use_Spot_Light: bpy.props.BoolProperty()

    SPOT_Size: bpy.props.FloatProperty(default=0.785398, subtype="ANGLE")
    SPOT_Blend: bpy.props.FloatProperty(default=0.150)

    SHOW_Area_Light: bpy.props.BoolProperty()
    Use_Area_Light: bpy.props.BoolProperty()

    AREA_X: bpy.props.FloatProperty(default=0.1)
    AREA_Y: bpy.props.FloatProperty(default=0.1)
    AREA_Shape: bpy.props.EnumProperty(items=ENUM_Area_Shape)
    AREA_CYCLES_Spread: bpy.props.FloatProperty()

    SHOW_Eevee_Factor: bpy.props.BoolProperty()
    Use_Eevee_Factor: bpy.props.BoolProperty()
    EEVEE_Diffuse_Factor: bpy.props.FloatProperty()
    EEVEE_Specular_Factor: bpy.props.FloatProperty()
    EEVEE_Volume_Factor: bpy.props.FloatProperty()

    Shadows: bpy.props.BoolProperty()

    SHOW_EEVEE_Shadow: bpy.props.BoolProperty()
    Use_EEVEE_Shadow: bpy.props.BoolProperty()

    EEVEE_Shadows_Clip_Start: bpy.props.FloatProperty(default=0.05)
    EEVEE_Shadows_Clip_Bias: bpy.props.FloatProperty(default=1.0)

    EEVEE_Contact_Shadows: bpy.props.BoolProperty()
    EEVEE_Contact_Shadows_Distance: bpy.props.FloatProperty(default=0.2)
    EEVEE_Contact_Shadows_Bias: bpy.props.FloatProperty(default=0.03)
    EEVEE_Contact_Shadows_Thickness: bpy.props.FloatProperty(default=0.2)

    EEVEE_SUN_Cascaded_Map_Count: bpy.props.IntProperty()
    EEVEE_SUN_Cascaded_Map_Fade: bpy.props.IntProperty()
    EEVEE_SUN_Cascaded_Map_Max_Distance: bpy.props.FloatProperty()
    EEVEE_SUN_Cascaded_Map_Distribution: bpy.props.FloatProperty()

    def draw(self, context):

        layout = self.layout
        col = layout.column(align=True)

        row = col.row(align=True)
        row.prop(self, "Strength", text="Strength")
        row.prop(self, "Color", text="")
        row = col.row(align=True)
        row.prop(self, "Shadows", text="Shadows")

        col.separator()

        engine = context.scene.render.engine

        if engine == "BLENDER_EEVEE":

            if Utility_Functions.draw_subpanel_checkbox(self, self.SHOW_Eevee_Factor, "SHOW_Eevee_Factor", self, "Use_Eevee_Factor", "Factor", col):


                col.prop(self, "EEVEE_Diffuse_Factor", text="Diffuse Factor")
                col.prop(self, "EEVEE_Specular_Factor", text="Specular Factor")
                col.prop(self, "EEVEE_Volume_Factor", text="Volume Factor")

        if Utility_Functions.draw_subpanel_checkbox(self, self.SHOW_Point_Spot_Light, "SHOW_Point_Spot_Light", self, "Use_Point_Spot_Light","Point & Spot", col):


            col.prop(self, "POINT_SPOT_Shadow_Soft_Size", text="Radius")

        if Utility_Functions.draw_subpanel_checkbox(self, self.SHOW_Sun_Light, "SHOW_Sun_Light", self, "Use_Sun_Light", "Sun", col):


            col.prop(self, "SUN_Angle", text="Angle")
            col.separator()


        if Utility_Functions.draw_subpanel_checkbox(self, self.SHOW_Spot_Light, "SHOW_Spot_Light", self, "Use_Spot_Light" , "Spot", col):


            col.prop(self, "SPOT_Size", text="Spot Size")
            col.prop(self, "SPOT_Blend", text="Spot Blend")

        if Utility_Functions.draw_subpanel_checkbox(self, self.SHOW_Area_Light, "SHOW_Area_Light", self, "Use_Area_Light","Area", col):


            col.prop(self, "AREA_Shape", text="")


            col.prop(self, "AREA_X", text="Area X")

            if self.AREA_Shape in ["RECTANGLE", "ELLIPSE"]:
                col.prop(self, "AREA_Y", text="Area Y")

            if engine == "CYCLES":
                col.prop(self, "AREA_CYCLES_Spread", text="Spread")


        if engine == "BLENDER_EEVEE":
            if self.Shadows:
                if Utility_Functions.draw_subpanel_checkbox(self, self.SHOW_EEVEE_Shadow, "SHOW_EEVEE_Shadow", self, "Use_EEVEE_Shadow", "Eevee Shadow", col):



                    col.prop(self, "EEVEE_Shadows_Clip_Start", text="Clip Start")
                    col.prop(self, "EEVEE_Shadows_Clip_Bias", text="Bias")

                    col.separator()

                    col.prop(self, "EEVEE_Contact_Shadows", text="Contact Shadows")

                    if self.EEVEE_Contact_Shadows:
                        col.prop(self, "EEVEE_Contact_Shadows_Distance", text="Distance")
                        col.prop(self, "EEVEE_Contact_Shadows_Bias", text="Bias")
                        col.prop(self, "EEVEE_Contact_Shadows_Thickness", text="Thickness")

                    if self.Use_Sun_Light:
                        col.separator()
                        col.label(text="Cascaded Shadow Map")
                        col.prop(self, "EEVEE_SUN_Cascaded_Map_Count", text="Count")
                        col.prop(self, "EEVEE_SUN_Cascaded_Map_Fade", text="Fade")
                        col.prop(self, "EEVEE_SUN_Cascaded_Map_Max_Distance", text="Max Distance")
                        col.prop(self, "EEVEE_SUN_Cascaded_Map_Distribution", text="Distribution")



    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):

        scn = context.scene
        scn_properties = scn.Radiant_Light_Properties
        Tag_List = scn_properties.Tags_List
        Tag_Index = self.index

        Active_Tag = None

        context.view_layer.update()

        if len(scn_properties.Tags_List) > 0:
            Active_Tag = scn_properties.Tags_List[Tag_Index].name

        if Active_Tag:


            objects = context.view_layer.objects
            Tagged_Objects = [object for object in objects if object.type == "LIGHT" and object.Radiant_Light_Properties.Tags == Active_Tag]
            Select_Check = [object.select_get() for object in Tagged_Objects]
            engine = context.scene.render.engine

            for object in Tagged_Objects:

                light_data = object.data
                light_type = object.data.type

                light_data.energy = self.Strength
                light_data.color = self.Color




                if self.Use_Point_Spot_Light:
                    if light_type in ["POINT", "SPOT"]:
                        light_data.shadow_soft_size = self.POINT_SPOT_Shadow_Soft_Size

                if self.Use_Sun_Light:
                    if light_type in ["SUN"]:
                        light_data.angle = self.SUN_Angle

                        if self.Shadows:
                            if self.Use_EEVEE_Shadow:
                                light_data.shadow_cascade_count = self.EEVEE_SUN_Cascaded_Map_Count
                                light_data.shadow_cascade_fade = self.EEVEE_SUN_Cascaded_Map_Fade
                                light_data.shadow_cascade_max_distance = self.EEVEE_SUN_Cascaded_Map_Max_Distance
                                light_data.shadow_cascade_exponent = self.EEVEE_SUN_Cascaded_Map_Distribution

                if self.Use_Spot_Light:
                    if light_type in ["SPOT"]:
                        light_data.spot_size = self.SPOT_Size
                        light_data.spot_blend = self.SPOT_Blend

                if self.Use_Area_Light:
                    if light_type in ["AREA"]:

                        light_data.size = self.AREA_X

                        if self.AREA_Shape in ["RECTANGLE", "ELLIPSE"]:
                            light_data.size_y = self.AREA_Y

                        light_data.shape = self.AREA_Shape

                        if engine == "CYCLES":
                            light_data.spread = self.AREA_CYCLES_Spread


                if engine == "BLENDER_EEVEE":
                    if self.Use_Eevee_Factor:
                        light_data.diffuse_factor = self.EEVEE_Diffuse_Factor
                        light_data.specular_factor = self.EEVEE_Specular_Factor
                        light_data.volume_factor = self.EEVEE_Volume_Factor

                    if self.Shadows:

                        if self.Use_EEVEE_Shadow:
                            light_data.shadow_buffer_clip_start = self.EEVEE_Shadows_Clip_Start
                            light_data.shadow_buffer_bias = self.EEVEE_Shadows_Clip_Bias
                            light_data.use_contact_shadow = self.EEVEE_Contact_Shadows

                            if self.EEVEE_Contact_Shadows:
                                light_data.contact_shadow_distance = self.EEVEE_Contact_Shadows_Distance
                                light_data.contact_shadow_bias = self.EEVEE_Contact_Shadows_Bias
                                light_data.contact_shadow_thickness = self.EEVEE_Contact_Shadows_Thickness

                if engine == "BLENDER_EEVEE":
                    light_data.use_shadow = self.Shadows

                if engine == "CYCLES":
                    light_data.cycles.cast_shadow = self.Shadows

        return {'FINISHED'}

classes = [Radiant_OT_Set_Property_Tagged_Lights]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
