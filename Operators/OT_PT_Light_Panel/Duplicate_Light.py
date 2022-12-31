import bpy



class Radiant_PT_Duplicate_Light(bpy.types.Operator):
    """Duplicate"""
    bl_idname = "radiant.duplicate_light"
    bl_label = "Duplicate Light"
    bl_options = {'REGISTER', 'UNDO'}

    object: bpy.props.StringProperty()

    def execute(self, context):

        object = context.scene.objects.get(self.object)

        if object:
            duplicates = object.copy()
            duplicates.data = object.data.copy()
            duplicates.data.Disable_Make_Raymesh_Button = False

            for collection in object.users_collection:
                collection.objects.link(duplicates)



            bpy.ops.object.select_all(action='DESELECT')

            duplicates.select_set(True)

            bpy.context.view_layer.objects.active = duplicates

            bpy.ops.transform.translate("INVOKE_DEFAULT")


        return {'FINISHED'}

classes = [Radiant_PT_Duplicate_Light]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
