import bpy

ENUM_Mode = [("ASSIGN","Assign","Assign"),("UNASSIGN","Unassign","Unassign"), ("ASSIGN_NEW", "New", "New")]
class Radiant_OT_Tag_Selected_Lights(bpy.types.Operator):
    """Tag Selected Lights"""
    bl_idname = "radiant.tag_selected_lights"
    bl_label = "Tag Selected Lights"
    bl_options = {'REGISTER', 'UNDO'}

    mode: bpy.props.EnumProperty(items=ENUM_Mode)
    tag: bpy.props.StringProperty()

    new_tag_name: bpy.props.StringProperty(default="Tag")

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "new_tag_name", text="Tag Name")

    def invoke(self, context, event):
        scn = context.scene
        scn_properties = scn.Radiant_Light_Properties
        Tag_List = scn_properties.Tags_List

        if self.mode == "ASSIGN_NEW":
            self.new_tag_name = "Tag" + str(len(Tag_List))
            return context.window_manager.invoke_props_dialog(self)
        else:
            return self.execute(context)

    def execute(self, context):

        scn = context.scene
        scn_properties = scn.Radiant_Light_Properties

        selected_objects = [object for object in context.selected_objects if object.type == "LIGHT"]

        if self.mode == "ASSIGN_NEW":
            Tag_List = scn_properties.Tags_List
            new_tag = Tag_List.add()
            new_tag.name = self.new_tag_name

            scn_properties.Tags_List_Index = len(Tag_List)-1

            scn_properties.Light_Filter_Tags = self.new_tag_name

        for object in selected_objects:

            object_radiant_settings = object.Radiant_Light_Properties
            if self.mode == "UNASSIGN":
                object_radiant_settings.Tags = ""

            if self.mode == "ASSIGN":
                object_radiant_settings.Tags = self.tag

            if self.mode == "ASSIGN_NEW":
                object_radiant_settings.Tags = self.new_tag_name

        return {'FINISHED'}

classes = [Radiant_OT_Tag_Selected_Lights]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
