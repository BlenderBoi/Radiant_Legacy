import bpy



class Radiant_PT_Make_Single(bpy.types.Operator):
    """Make Single"""
    bl_idname = "radiant.make_unique"
    bl_label = "Make Single"
    bl_options = {'REGISTER', 'UNDO'}

    object: bpy.props.StringProperty()

    def execute(self, context):

        object = context.scene.objects.get(self.object)

        if object:

            object.data = object.data.copy()




        return {'FINISHED'}

classes = [Radiant_PT_Make_Single]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
