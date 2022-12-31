import bpy
from Radiant import Utility_Functions

ENUM_Target_Type = [("OBJECT","Object","Object"),("SELECTED","Selected","Selected"),("CURSOR","Cursor","Cursor")]


class Radiant_PT_Aim_Light(bpy.types.Operator):
    """Duplicate"""
    bl_idname = "radiant.aim_light"
    bl_label = "Aim Light"
    bl_options = {'REGISTER', 'UNDO'}

    object: bpy.props.StringProperty()
    target: bpy.props.StringProperty()
    empty_name: bpy.props.StringProperty()

    use_constraint: bpy.props.BoolProperty(default=True)
    pre_clear_constraint: bpy.props.BoolProperty(default=True)

    move: bpy.props.BoolProperty(default=False)
    target_type: bpy.props.EnumProperty(items=ENUM_Target_Type)
    create_empty: bpy.props.BoolProperty(default=True)

    def invoke(self, context, event):

        if context.object:
            self.target = context.object.name

        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):

        object = context.scene.objects.get(self.object)

        layout = self.layout
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(self, "target_type", text="Target Type", expand=True)

        if self.target_type == "OBJECT":
            col.prop_search(self, "target", context.view_layer, "objects", text="")

        row = layout.row(align=True)
        row.prop(self, "use_constraint", text="Use Constraint")
        row.prop(self, "pre_clear_constraint", text="Pre Clear Constraints")

        # if self.use_constraint:
        #     layout.label(text="Extra")
        #     layout.prop(self, "move", text="Active Move Tool")

    def execute(self, context):

        object = context.scene.objects.get(self.object)
        target = context.view_layer.objects.get(self.target)
        empty = None

        # if target:


        if object:
            self.empty_name = "TGT_" + object.name

            back_active = context.object
            back_selected = context.selected_objects

            if self.pre_clear_constraint:
                object.constraints.clear()




            if self.target_type == "OBJECT":
                constraint = object.constraints.new(type="TRACK_TO")
                constraint.target = target

            if self.target_type in ["CURSOR", "SELECTED"]:
                constraint = object.constraints.new(type="TRACK_TO")

                context.view_layer.update()

                empty = bpy.data.objects.new(self.empty_name, object_data=None)
                bpy.context.collection.objects.link(empty)

                if self.target_type == "CURSOR":
                    empty.location = context.scene.cursor.location

                if self.target_type == "SELECTED":
                    selected_objects_coordinates = [object.matrix_world.to_translation() for object in context.selected_objects]
                    selected_midpoint = Utility_Functions.midpoint(selected_objects_coordinates, "BOUNDING_BOX")
                    empty.location = selected_midpoint

                constraint.target = empty


            if not self.use_constraint:

                context.view_layer.update()
                mat = object.matrix_world.copy()

                object.constraints.remove(constraint)
                context.view_layer.update()
                object.matrix_world = mat


                if self.target_type in ["CURSOR", "SELECTED"]:

                    if empty:
                        bpy.data.objects.remove(empty)







            if self.use_constraint:
                if self.move:


                    bpy.ops.object.select_all(action='DESELECT')

                    object.select_set(True)
                    bpy.context.view_layer.objects.active = object

                    bpy.ops.transform.translate("INVOKE_DEFAULT")


                    bpy.ops.object.select_all(action='DESELECT')

                    for obj in back_selected:
                        obj.select_set(True)

                    if back_active:
                        back_active.select_set(True)
                        bpy.context.view_layer.objects.active = back_active



        return {'FINISHED'}

classes = [Radiant_PT_Aim_Light]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
