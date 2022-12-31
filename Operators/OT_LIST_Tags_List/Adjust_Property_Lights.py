import bpy
from Radiant import Utility_Functions
import colorsys
import mathutils

class Radiant_OT_Adjust_Strength_And_Color_Tagged_Lights(bpy.types.Operator):
    """Adjust Strength and Color for Tagged Lights"""
    bl_idname = "radiant.adjust_strength_and_color_tagged_lights"
    bl_label = "Adjust Tagged Light Strength and Color"
    bl_options = {'REGISTER', 'UNDO'}


    Strength: bpy.props.FloatProperty(default=1.0)
    Strength_Value: bpy.props.FloatProperty(default=100)

    set_strength: bpy.props.BoolProperty(default=False)

    Color: bpy.props.FloatVectorProperty(subtype="COLOR", default=(1, 1, 1))

    set_color: bpy.props.BoolProperty(default=False)

    Hue: bpy.props.FloatProperty(default=0)
    Saturation: bpy.props.FloatProperty(default=0)
    Value: bpy.props.FloatProperty(default=0)




    index: bpy.props.IntProperty()


    def draw(self, context):

        layout = self.layout
        col = layout.column(align=True)

        col.prop(self, "set_strength", text="Set Strength")

        if self.set_strength:
            col.prop(self, "Strength_Value", text="Set Strength")
        else:
            col.prop(self, "Strength", text="Add Strength")



        col.separator()
        col.prop(self, "set_color", text="Set Color")

        if self.set_color:
            col.prop(self, "Color")
        else:
            row = col.row(align=True)
            row.prop(self, "Hue", text="Hue")
            row.prop(self, "Saturation", text="Saturation")
            row.prop(self, "Value", text="Value")

    def invoke(self, context, event):
        self.Strength = 0
        self.Hue = 0
        self.Saturation = 0
        self.Value = 0

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

            for object in Tagged_Objects:
                if self.set_strength:
                    object.data.energy = self.Strength_Value
                else:
                    object.data.energy = object.data.energy + self.Strength

                if self.set_color:
                    object.data.color = self.Color
                else:

                    add_hsv = (self.Hue, self.Saturation, self.Value)

                    color_rgb = object.data.color
                    color_hsv = colorsys.rgb_to_hsv(color_rgb[0], color_rgb[1], color_rgb[2])
                    final_color_hsv = mathutils.Vector(color_hsv) + mathutils.Vector(add_hsv)
                    final_color_rgb = colorsys.hsv_to_rgb(final_color_hsv[0], final_color_hsv[1], final_color_hsv[2])

                    object.data.color = final_color_rgb

        return {'FINISHED'}

classes = [Radiant_OT_Adjust_Strength_And_Color_Tagged_Lights]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
