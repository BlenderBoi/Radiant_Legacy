
import bpy

from Radiant import Utility_Functions


ENUM_type = [("AREA","Area","Area"),("POINT","Point","Point"),("SPOT","Spot","Spot"), ("TEXT", "Text", "Text"), ("SHAPE", "Shape", "Shape")]
ENUM_shape = [("RECTANGLE","Rectangle","Rectangle"),("ELLIPSE","Ellipse","Ellipse")]
default_color = [0.000000, 0.211262, 0.800000, 1.000000]



def set_geometry_node_prop(context, object, property, value):

    if object:
        for modifier in object.modifiers:
            modifier[property] = value


class Radiant_OT_Add_RayMesh(bpy.types.Operator):
    """Add RayMesh"""
    bl_idname = "radiant.add_raymesh"
    bl_label = "Add Raymesh"
    bl_options = {'REGISTER', 'UNDO'}

    name: bpy.props.StringProperty(default="Raymesh")
    type: bpy.props.EnumProperty(items=ENUM_type)

    text: bpy.props.StringProperty(default="Text")
    color: bpy.props.FloatVectorProperty(default=default_color, subtype="COLOR", size=4, min=0.0, max=1.0)


    def draw(self, context):
        layout = self.layout
        # layout.prop(self, "name", text="Name")
        row = layout.row()
        # row.prop(self, "type", text="Type", expand=True)
        if self.type == "TEXT":
            row.prop(self, "text", text="Text")
        row = layout.row()
        row.prop(self, "color", text="Color")


    def invoke(self, context, event):

        if self.type == "AREA":
            self.name = "Mesh_Area"
        if self.type == "POINT":
            self.name = "Mesh_Point"
        if self.type == "SPOT":
            self.name = "Mesh_Spot"
        if self.type == "TEXT":
            self.name = "Mesh_Text"
        if self.type == "SHAPE":
            self.name = "Mesh_Shape"

        self.location = context.scene.cursor.location

        # if self.type in ["AREA", "POINT", "SPOT", "SHAPE"]:

        #     return self.execute(context)

        # if self.type in ["TEXT"]:

        return context.window_manager.invoke_props_dialog(self)

    @classmethod
    def poll(cls, context):

        if context.mode == "OBJECT":
            return True

    def execute(self, context):
        filename = "Raymesh_Light.blend"

        filepath = Utility_Functions.get_asset_file(filename)

        object_name = None

        inputs = []

        if self.type == "AREA":
            object_name = "Mesh_Area"

            inputs = ["Input_32", "Input_35"] 

        if self.type == "POINT":
            object_name = "Mesh_Point"
            inputs = ["Input_11", "Input_12"] 

        if self.type == "SPOT":
            object_name = "Mesh_Spot"
            inputs = ["Input_30"] 

        if self.type == "TEXT":
            object_name = "Mesh_Text"
            inputs = ["Input_35", "Input_32"] 

        if self.type == "SHAPE":
            object_name = "Mesh_Shape"
            inputs = ["Input_35", "Input_32"] 

        if object_name:

            appended_object = Utility_Functions.append_object(filepath, object_name)
            appended_object.name = self.name
            appended_object.location = self.location
            
            for input in inputs:
                appended_object.modifiers[0][input][0] = self.color[0]
                appended_object.modifiers[0][input][1] = self.color[1]
                appended_object.modifiers[0][input][2] = self.color[2]
                appended_object.modifiers[0][input][3] = self.color[3]

            appended_object.rotation_euler[0] = 0
            appended_object.rotation_euler[1] = 0
            appended_object.rotation_euler[2] = 0

            



            if self.type == "TEXT":
                appended_object.data.body = self.text

            context.view_layer.objects.active = appended_object


        return {'FINISHED'}


classes = [Radiant_OT_Add_RayMesh]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
