
import bpy

from Radiant import Utility_Functions


ENUM_type = [("AREA","Area","Area"),("POINT","Point","Point"),("SPOT","Spot","Spot")]

default_color = [0.000000, 0.211262, 0.800000]

class Radiant_OT_Add_RayMesh_Light_As_Driver(bpy.types.Operator):
    """Add RayMesh"""
    bl_idname = "radiant.add_raymesh_light_as_driver"
    bl_label = "Add Raymesh Light As Driver"
    bl_options = {'REGISTER', 'UNDO'}


    type: bpy.props.EnumProperty(items=ENUM_type)
    disable_raymesh_selection: bpy.props.BoolProperty(default=False)
    invoke_prop: bpy.props.BoolProperty()

    color: bpy.props.FloatVectorProperty(default=default_color, subtype="COLOR", size=3, min=0.0, max=1.0)

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        # row.prop(self, "type", text="Type", expand=True)
        # layout.prop(self, "disable_raymesh_selection", text="Disable Raymesh Selection")

        row = layout.row()
        row.prop(self, "color", text="Color")

    def invoke(self, context, event):

        self.location = context.scene.cursor.location

        return context.window_manager.invoke_props_dialog(self)
        # if self.invoke_prop:
        #     return context.window_manager.invoke_props_dialog(self)
        # else:
        #     return self.execute(context)

    @classmethod
    def poll(cls, context):

        if context.mode == "OBJECT":
            return True

    def execute(self, context):
        filename = "Raymesh_Light.blend"

        filepath = Utility_Functions.get_asset_file(filename)

        object_name = None

        if self.type == "AREA":
            object_name = "Light_Area"
        if self.type == "POINT":
            object_name = "Light_Point"
        if self.type == "SPOT":
            object_name = "Light_Spot"

        if object_name:

            appended_object = Utility_Functions.append_object(filepath, object_name)

            for obj in appended_object:
                if obj.type == "MESH":
                    if self.disable_raymesh_selection:
                        obj.hide_select = True
                    obj.select_set(False)
                if obj.type == "LIGHT":
                    obj.data.Disable_Make_Raymesh_Button = True
                    obj.select_set(True)
                    context.view_layer.objects.active = obj
                    obj.data.color = self.color

                obj.rotation_euler[0] = 0
                obj.rotation_euler[1] = 0
                obj.rotation_euler[2] = 0

                obj.location = self.location


        return {'FINISHED'}


classes = [Radiant_OT_Add_RayMesh_Light_As_Driver]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
