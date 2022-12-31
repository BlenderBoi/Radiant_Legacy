import bpy



class Radiant_OT_Find_Light(bpy.types.Operator):
    """Find Light"""
    bl_idname = "radiant.find_light"
    bl_label = "Find Object"
    bl_options = {'REGISTER', 'UNDO'}

    object: bpy.props.StringProperty()

    def execute(self, context):

        object = context.scene.objects.get(self.object)

        if object:

            selected = [obj for obj in context.selected_objects]
            active = context.object

            bpy.ops.object.select_all(action='DESELECT')

            object.select_set(True)
            bpy.context.view_layer.objects.active = object


            hide_state = object.hide_viewport
            select_state = object.hide_select


            object.hide_viewport = False
            object.hide_select = False


            if object.select_get():
                bpy.ops.view3d.view_selected(use_all_regions=False)

            object.hide_viewport = hide_state
            object.hide_select = select_state

            bpy.ops.object.select_all(action='DESELECT')

            for obj in selected:
                obj.select_set(True)

            bpy.context.view_layer.objects.active = active

        return {'FINISHED'}

classes = [Radiant_OT_Find_Light]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
