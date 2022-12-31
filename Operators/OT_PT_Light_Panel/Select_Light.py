import bpy


class Radiant_OT_Select_Light(bpy.types.Operator):
    """Select"""
    bl_idname = "radiant.select_light"
    bl_label = "Select Light"
    bl_options = {'REGISTER', 'UNDO'}

    object: bpy.props.StringProperty()

    Deselect_All: bpy.props.BoolProperty()

    def invoke(self, context, event):
        if event.shift:
            self.Deselect_All = False


        else:
            self.Deselect_All = True


        return self.execute(context)

    def execute(self, context):

        object = context.scene.objects.get(self.object)

        if object:

            if self.Deselect_All:

                bpy.ops.object.select_all(action='DESELECT')

            object.select_set(not object.select_get())

            if object.select_get():
                context.view_layer.objects.active = object

        return {'FINISHED'}

classes = [Radiant_OT_Select_Light]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
