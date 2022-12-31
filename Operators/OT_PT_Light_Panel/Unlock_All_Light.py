import bpy

class Radiant_OT_Unlock_All_Light(bpy.types.Operator):
    """Unlock All"""
    bl_idname = "radiant.unlock_all_light"
    bl_label = "Unlock ALl Light"
    bl_options = {'REGISTER', 'UNDO'}

    state: bpy.props.BoolProperty()

    def execute(self, context):

        for obj in context.scene.objects:
            if obj.type == "LIGHT":
                obj.hide_select = self.state

        return {'FINISHED'}


classes = [Radiant_OT_Unlock_All_Light]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
