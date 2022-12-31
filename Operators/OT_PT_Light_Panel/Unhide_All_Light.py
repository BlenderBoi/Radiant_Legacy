import bpy

class Radiant_OT_Unhide_All_Light(bpy.types.Operator):
    """Unhide All"""
    bl_idname = "radiant.unhide_all_light"
    bl_label = "Unhide ALl Light"
    bl_options = {'REGISTER', 'UNDO'}

    state: bpy.props.BoolProperty()

    def execute(self, context):


        for obj in context.view_layer.objects:
            if obj.type == "LIGHT":
                obj.hide_viewport = self.state
                obj.hide_set(self.state)

        return {'FINISHED'}


classes = [Radiant_OT_Unhide_All_Light]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
