import bpy


class Radiant_OT_Remove_Light(bpy.types.Operator):
    """Remove"""
    bl_idname = "radiant.remove_light"
    bl_label = "Remove Light"
    bl_options = {'REGISTER', 'UNDO'}

    object: bpy.props.StringProperty()

    def execute(self, context):

        object = context.scene.objects.get(self.object)

        if object:

            bpy.data.objects.remove(object)

        return {'FINISHED'}

classes = [Radiant_OT_Remove_Light]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
