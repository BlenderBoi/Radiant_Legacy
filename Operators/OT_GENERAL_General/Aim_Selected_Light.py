import bpy
from Radiant import Utility_Functions
import mathutils

ENUM_Target = [('ACTIVE', 'Active Object', 'Active Object'), ('OBJECT', 'Pick Object', 'Pick Object'), ('CURSOR', 'Cursor', 'Cursor')]

class RADIANT_Aim_Selected_Lights(bpy.types.Operator):
    """Aim Selected Lights"""
    bl_idname = "radiant.aim_selected_lights"
    bl_label = "Aim Selected Lights"
    bl_options = {'UNDO', 'REGISTER'}

    target: bpy.props.EnumProperty(items=ENUM_Target)
    object: bpy.props.StringProperty()

    pre_clear_constraint: bpy.props.BoolProperty(default=True)

    use_constraint: bpy.props.BoolProperty(default=True)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "target", text="Target")

        if self.target == "OBJECT":
            layout.prop_search(self, "object", context.view_layer, "objects", text="Target")

        layout.prop(self, "pre_clear_constraint", text="Pre Clear Constraint")
        layout.prop(self, "use_constraint", text="Use Constraint")


    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)


    def execute(self, context):

        selected_objects = [object for object in context.selected_objects if object.type == "LIGHT"]

        target = None
        empty = None

        if self.target == "ACTIVE":
            target = context.active_object

            if target in selected_objects:
                selected_objects.remove(target)

        if self.target == "OBJECT":
            target = context.view_layer.objects.get(self.object)

            if target in selected_objects:
                selected_objects.remove(target)

        if self.target == "CURSOR":

            empty = Utility_Functions.Create_Empty("Empty_Cursor_Target")
            empty.location = context.scene.cursor.location
            # empty.empty_display_type = self.Empty_Shape
            # empty.empty_display_size = self.Empty_Display_Size

            target = empty

            if target in selected_objects:
                selected_objects.remove(target)



        if target:
            for object in selected_objects:
                if not object.data.type == "POINT":

                    if self.pre_clear_constraint:
                        object.constraints.clear()


                    constraint = object.constraints.new("DAMPED_TRACK")
                    constraint.target = target
                    constraint.track_axis = "TRACK_NEGATIVE_Z"

                    context.view_layer.update()
                    mw = object.matrix_world.copy()
                    object.matrix_world = mw

                    if not self.use_constraint:
                        object.constraints.remove(constraint)

        if not self.use_constraint:

            if empty:
                bpy.data.objects.remove(empty)




        return {'FINISHED'}


classes = [RADIANT_Aim_Selected_Lights]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
