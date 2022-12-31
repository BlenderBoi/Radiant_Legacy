import bpy


class Radiant_PT_Apply_Light_Constraint(bpy.types.Operator):
    """Apply Constraint"""
    bl_idname = "radiant.apply_light_constraint"
    bl_label = "Apply Light Constraint"
    bl_options = {'REGISTER', 'UNDO'}

    object: bpy.props.StringProperty()

    def execute(self, context):

        object = context.scene.objects.get(self.object)



        context.view_layer.update()
        mat = object.matrix_world.copy()
        object.constraints.clear()
        context.view_layer.update()
        object.matrix_world = mat



        return {'FINISHED'}

classes = [Radiant_PT_Apply_Light_Constraint]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
