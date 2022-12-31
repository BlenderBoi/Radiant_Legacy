import bpy



class Radiant_PT_Hide_Light_Children(bpy.types.Operator):
    """Toogle Light Children"""
    bl_idname = "radiant.hide_light_children"
    bl_label = "Toogle Hide Light Children"
    bl_options = {'REGISTER', 'UNDO'}

    object: bpy.props.StringProperty()

    def execute(self, context):

        object = context.view_layer.objects.get(self.object)

        check = any([not child.hide_viewport for child in object.children])

        for child in object.children:
            child.hide_viewport = check
            child.hide_render = check
            child.hide_set(check)

        return {'FINISHED'}

classes = [Radiant_PT_Hide_Light_Children]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
