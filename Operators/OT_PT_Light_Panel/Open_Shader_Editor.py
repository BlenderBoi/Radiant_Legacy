import bpy


class Radiant_OT_Open_Shader_Editor(bpy.types.Operator):
    """Open Shader Editor"""
    bl_idname = "radiant.open_shader_editor"
    bl_label = "Open in Shader Editor"
    bl_options = {'REGISTER', 'UNDO'}

    object: bpy.props.StringProperty()

    def execute(self, context):

        object = context.view_layer.objects.get(self.object)

        if object:


            bpy.context.view_layer.objects.active = object
            object.select_set(True)

            bpy.ops.wm.window_new()
            area = context.window_manager.windows[-1].screen.areas[0]
            area.type = "NODE_EDITOR"
            area.ui_type = "ShaderNodeTree"

        return {'FINISHED'}


classes = [Radiant_OT_Open_Shader_Editor]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
