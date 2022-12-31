
import bpy

from Radiant import Utility_Functions
import rna_prop_ui
import math

ENUM_type = [("AREA","Area","Area"),("POINT","Point","Point"),("SPOT","Spot","Spot")]
ENUM_shape = [("RECTANGLE","Rectangle","Rectangle"),("ELLIPSE","Ellipse","Ellipse")]

default_color = [0.000000, 0.113775, 1.000000, 1.000000]

inf = 340282346638528859811704183484516925440

#Set Light Property

class Radiant_OT_Make_Raymesh_From_Light(bpy.types.Operator):
    """Add RayMesh To Light"""
    bl_idname = "radiant.make_raymesh_from_light"
    bl_label = "Make Raymesh From Light"
    bl_options = {'REGISTER', 'UNDO'}

    light_object: bpy.props.StringProperty()

    light_as_driver: bpy.props.BoolProperty(default=True)
    parent_to_light: bpy.props.BoolProperty(default=True)
    constraint_to_light: bpy.props.BoolProperty(default=True)
    disable_raymesh_selection: bpy.props.BoolProperty(default=False)


    def draw(self, context):
        layout = self.layout
        layout.prop(self, "light_as_driver", text="Use Light As Driver")

        layout.prop(self, "parent_to_light", text="Parent to Light")
        layout.prop(self, "constraint_to_light", text="Constraint to Light")
        layout.prop(self, "disable_raymesh_selection", text="Disable Raymesh Selection")


    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)


    @classmethod
    def poll(cls, context):

        if context.mode == "OBJECT":
            return True

    def execute(self, context):

        filename = "Raymesh_Light.blend"

        filepath = Utility_Functions.get_asset_file(filename)

        object_name = None

        object = context.view_layer.objects.get(self.light_object)

        if object.type == "LIGHT":
            if object.data.type in ["AREA"]:

                if self.light_as_driver:
                    object_name = "Light_Area"
                else:
                    object_name = "Mesh_Area"

            if object.data.type in ["SPOT"]:

                if self.light_as_driver:
                    object_name = "Light_Spot"
                else:
                    object_name = "Mesh_Spot"

            if object.data.type in ["POINT"]:

                if self.light_as_driver:
                    object_name = "Light_Point"
                else:
                    object_name = "Mesh_Point"

            if object.data.type in ["SUN"]:
                self.report({"INFO"}, "No Raymesh Available for Sun Light")

            if object:
                if object.type == "LIGHT":
                    if object.data.type in ["AREA", "POINT", "SPOT"]:

                        if object_name:

                            object.show_in_front = True
                            appended_objects = Utility_Functions.append_object_normal(filepath, object_name)


                            if self.light_as_driver:

                                object.data.Disable_Make_Raymesh_Button = True
                                Utility_Functions.Create_Raymesh_Properties(object)   

                            for obj in appended_objects:
                                if obj.type == "MESH":

                                    obj.name = "Mesh_" + object.name

                                    if self.parent_to_light:

                                        obj.parent = object
                                        obj.matrix_world = object.matrix_world

                                    if self.disable_raymesh_selection:
                                        obj.hide_select = True

                                    if self.constraint_to_light:
                                        constraint = obj.constraints.new("COPY_TRANSFORMS")
                                        constraint.target = object

                                    if self.light_as_driver:

                                        if not obj.animation_data:
                                            obj.animation_data_create()

                                        for driver in obj.animation_data.drivers:
                                            for var in driver.driver.variables:
                                                for target in var.targets:
                                                    if target.id_type == "LIGHT":
                                                        target.id = object.data

                                if obj.type == "LIGHT":
                                    bpy.data.objects.remove(obj)


                            object.select_set(True)
                            context.view_layer.objects.active = object





        return {'FINISHED'}


classes = [Radiant_OT_Make_Raymesh_From_Light]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
