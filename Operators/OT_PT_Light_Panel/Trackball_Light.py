import bpy


class Radiant_PT_Trackball_Light(bpy.types.Operator):
    """Rotate"""
    bl_idname = "radiant.trackball_light"
    bl_label = "Rotate"
    bl_options = {'REGISTER', 'UNDO'}

    object: bpy.props.StringProperty()

    def execute(self, context):

        object = context.scene.objects.get(self.object)



        if object:
            bpy.ops.object.select_all(action='DESELECT')

            object.select_set(True)

            bpy.context.view_layer.objects.active = object

            bpy.ops.transform.trackball("INVOKE_DEFAULT")


        return {'FINISHED'}


classes = [Radiant_PT_Trackball_Light]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
