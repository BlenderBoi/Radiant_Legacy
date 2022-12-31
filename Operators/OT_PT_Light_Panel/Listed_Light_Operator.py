import bpy
import colorsys
import mathutils

ENUM_Operation = [("SELECT","Select","Select"),("HIDE","Hide","Hide"),("ADJUST","Adjust","Adjust")]

class Radiant_OT_Listed_Light_Operator(bpy.types.Operator):
    """Select"""
    bl_idname = "radiant.listed_light_operator"
    bl_label = "Select Listed Light"
    bl_options = {'REGISTER', 'UNDO'}

    object: bpy.props.StringProperty()
    operation: bpy.props.EnumProperty(items=ENUM_Operation)
    Deselect_All: bpy.props.BoolProperty()

    Strength: bpy.props.FloatProperty(default=1.0)
    Strength_Value: bpy.props.FloatProperty(default=100)

    set_strength: bpy.props.BoolProperty(default=False)

    Color: bpy.props.FloatVectorProperty(subtype="COLOR", default=(1, 1, 1))

    set_color: bpy.props.BoolProperty(default=False)

    Hue: bpy.props.FloatProperty(default=0)
    Saturation: bpy.props.FloatProperty(default=0)
    Value: bpy.props.FloatProperty(default=0)

    hide_children: bpy.props.BoolProperty(default=False)

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


    @classmethod
    def poll(cls, context):

        return context.mode == "OBJECT"



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


        return list(dict.fromkeys(Pinned_Objects+lights))

    def invoke(self, context, event):

        if self.operation == "ADJUST":
            self.Strength = 0
            self.Hue = 0
            self.Saturation = 0
            self.Value = 0
            return context.window_manager.invoke_props_dialog(self)


        if event.shift:
            self.Deselect_All = True

        else:
            self.Deselect_All = False

        if event.ctrl:
            self.hide_children = True

        else:
            self.hide_children = False



        return self.execute(context)

    def execute(self, context):

        objects  = self.get_filtered_lights(context)

        if self.operation == "SELECT":

            check = [object.select_get() for object in objects]

            if self.Deselect_All:

                bpy.ops.object.select_all(action='DESELECT')


            for object in objects:

                if self.Deselect_All:

                    object.select_set(True)

                else:
                    if any(check):
                        object.select_set(False)
                    else:
                        object.select_set(True)

                    if object.select_get():
                        context.view_layer.objects.active = object

        if self.operation == "HIDE":

            check = [object.hide_viewport for object in objects]



            for object in objects:

                object.hide_set(False)

                if self.Deselect_All:

                    object.hide_viewport = True
                    # object.hide_render = True

                else:

                    if any(check):
                        object.hide_viewport = False
                        # object.hide_render = False
                    else:
                        object.hide_viewport = True
                        # object.hide_render = True

        if self.operation == "ADJUST":

            for object in objects:

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

classes = [Radiant_OT_Listed_Light_Operator]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
