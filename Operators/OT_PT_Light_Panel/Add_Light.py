
import bpy
from Radiant import Utility_Functions

def ENUM_Activate(self, context):

    ENUM_items = [("NONE","None","None")]

     # or self.track_to

    if self.type == "POINT":

        ENUM_items = [("MOVE","Move","Move"),("NONE","None","None")]

    else:

        ENUM_items = [("MOVE","Move","Move"),("ROTATE","Trackball","ROTATE"),("NONE","None","None")]

    return ENUM_items

ENUM_Type = [("POINT","Point","Point"),("SUN","Sun","Sun"),("SPOT","Spot","Spot"),("AREA","Area","Area")]
ENUM_Position = [("CURSOR","Cursor","Cursor"),("CENTER","Center","Center"), ("SELECTED", "Selected", "Selected")]
ENUM_Target_Type = [("OBJECT","Object","Object"),("CURSOR","Cursor","Cursor")]

class Radiant_OT_Add_Light(bpy.types.Operator):
    """Add Aim Light"""
    bl_idname = "radiant.add_light"
    bl_label = "Add Light"
    bl_options = {'REGISTER', 'UNDO'}

    name: bpy.props.StringProperty(default="light")
    type: bpy.props.EnumProperty(default="SUN", items=ENUM_Type)
    position: bpy.props.EnumProperty(default="CURSOR", items=ENUM_Position)
    activate: bpy.props.EnumProperty(items=ENUM_Activate)

    select: bpy.props.BoolProperty(default=False)

    track_to: bpy.props.BoolProperty()
    target: bpy.props.StringProperty()
    target_type: bpy.props.EnumProperty(items=ENUM_Target_Type)


    new_tag: bpy.props.BoolProperty()
    tags: bpy.props.StringProperty()


    def invoke(self, context, event):

        if context.object:
            self.target = context.object.name

        return context.window_manager.invoke_props_dialog(self)

    @classmethod
    def poll(cls, context):

        if context.mode == "OBJECT":
            return True

    def draw(self, context):


        scn = context.scene
        scn_properties = scn.Radiant_Light_Properties

        layout = self.layout

        layout.prop(self, "name", text="Name")
        layout.prop(self, "position", expand=True)

        layout.prop(self, "type", expand=True)
        layout.prop(self, "activate", text="Activate")


        if not self.type == "POINT":
            layout.prop(self, "track_to", text="Track To")

            if self.track_to:
                layout.prop(self, "target_type", text="Target Type")
                if self.target_type == "OBJECT":
                    layout.prop_search(self, "target", context.view_layer, "objects", text="Target")


        layout.prop(self, "select", text="Select")

        row = layout.row(align=True)
        if self.new_tag:
            row.prop(self, "tags", text="Tags")

        else:
            row.prop_search(self, "tags", scn_properties, "Tags_List", text="Tags")


        row.prop(self, "new_tag", text="", icon="ADD")

    def execute(self, context):


        mode  = context.mode
        scn = context.scene

        preferences = Utility_Functions.get_addon_preferences()

        name = self.name
        type = self.type
        object = Utility_Functions.Create_Light(name, type=type, light_data=None, collection=None)

        scn_properties = scn.Radiant_Light_Properties

        back_active = context.object
        back_selected = [obj for obj in context.selected_objects]

        Utility_Functions.Set_Tags(self.tags, object)

        object.data.Disable_Make_Raymesh_Button = False

        if self.position == "CURSOR":
            object.location = context.scene.cursor.location

        if self.position == "CENTER":
            object.location = (0, 0, 0)

        if self.position == "SELECTED":
            location = Utility_Functions.get_selected_midpoint()
            object.location = location



##########################################################################

        target = context.view_layer.objects.get(self.target)

        if self.track_to:

            if not self.type == "POINT":
                if target:

                    if self.target_type == "OBJECT":

                        constraint = object.constraints.new(type="TRACK_TO")
                        constraint.target = target

                if self.target_type == "CURSOR":

                    constraint = object.constraints.new(type="TRACK_TO")

                    context.view_layer.update()

                    empty = bpy.data.objects.new(object.name + "_target", object_data=None)
                    bpy.context.collection.objects.link(empty)
                    empty.location = context.scene.cursor.location

                    constraint.target = empty

##########################################################################




        bpy.ops.object.select_all(action='DESELECT')

        object.select_set(True)
        bpy.context.view_layer.objects.active = object

        context.view_layer.update()

        if self.activate == "MOVE":
            bpy.ops.transform.translate("INVOKE_DEFAULT")

        if self.activate == "ROTATE":
            bpy.ops.transform.trackball("INVOKE_DEFAULT")

        if not self.select:

            bpy.ops.object.select_all(action='DESELECT')

            for obj in back_selected:
                obj.select_set(True)

            if back_active:
                back_active.select_set(True)
                bpy.context.view_layer.objects.active = back_active


        return {'FINISHED'}




classes = [Radiant_OT_Add_Light]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
