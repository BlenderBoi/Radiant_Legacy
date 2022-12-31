import bpy


class Radiant_OT_Solo_Light(bpy.types.Operator):
    """Solo"""
    bl_idname = "radiant.solo_light"
    bl_label = "Solo Light"
    bl_options = {'REGISTER', 'UNDO'}

    object: bpy.props.StringProperty()

    def invoke(self, context, event):

        if event.shift:

            for obj in context.view_layer.objects:
                if obj.type == "LIGHT":
                    obj.hide_viewport = False
                    obj.hide_set(False)

            return {'FINISHED'}

        else:

            return self.execute(context)

    def execute(self, context):

        object = context.scene.objects.get(self.object)

        if object:
            for obj in context.view_layer.objects:
                if obj.type == "LIGHT":
                    obj.hide_viewport = True

            object.hide_viewport = False

        return {'FINISHED'}

classes = [Radiant_OT_Solo_Light]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
