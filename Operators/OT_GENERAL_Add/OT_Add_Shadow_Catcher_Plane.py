
import bpy

from Radiant import Utility_Functions



class Radiant_OT_Add_Shadow_Catcher_Plane(bpy.types.Operator):
    """Add Shadow Catcher Plane"""
    bl_idname = "radiant.add_shadow_catcher_plane"
    bl_label = "Add Shadow Catcher Plane"
    bl_options = {'REGISTER', 'UNDO'}

    name: bpy.props.StringProperty(default="Shadow_Catcher_Plane")

    size_x: bpy.props.FloatProperty(default=5.0, name="Size X")
    size_y: bpy.props.FloatProperty(default=5.0, name="Size Y")

    def invoke(self, context, event):
        self.location = context.scene.cursor.location
        return self.execute(context)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "name", text="Name")
        col = layout.column(align=True)
        col.prop(self, "size_x")
        col.prop(self, "size_y")

    @classmethod
    def poll(cls, context):

        if context.mode == "OBJECT":
            return True

    def execute(self, context):
        filename = "ShadowCatcher.blend"

        filepath = Utility_Functions.get_asset_file(filename)
        object_name = "Shadow_Catcher"

        appended_object = Utility_Functions.append_object(filepath, object_name)
        appended_object.name = self.name
        appended_object.location = self.location
        appended_object.scale.x = self.size_x
        appended_object.scale.y = self.size_y
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

        return {'FINISHED'}


classes = [Radiant_OT_Add_Shadow_Catcher_Plane]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
