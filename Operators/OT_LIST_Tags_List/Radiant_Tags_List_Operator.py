import bpy

from Radiant import Utility_Functions

ENUM_list_operation = [("ADD","Add","Add"),("REMOVE","Remove","Remove"),("UP","Up","Up"), ("DOWN","Down","Down"), ("ASSIGN","Assign","Assign"), ("UNASSIGN","Unassign","Unassign")]

class RADIANT_Tags_List_Operator(bpy.types.Operator):
    """List Operator"""
    bl_idname = "radiant.tags_list_operator"
    bl_label = "List Operator"
    bl_options = {'UNDO', 'REGISTER'}

    operation: bpy.props.EnumProperty(items=ENUM_list_operation)
    index: bpy.props.IntProperty()
    tag_name: bpy.props.StringProperty(default="Tag01")

    from_all: bpy.props.BoolProperty(default=True)

    def draw(self, context):

        layout = self.layout
        if self.operation == "UNASSIGN":
            layout.prop(self, "from_all", text="Unassign All Selected")

        if self.operation == "ADD":
            layout.prop(self, "tag_name", text="Tag:")

    def invoke(self, context, event):

        if event.shift:
            self.from_all = True
        else:
            self.from_all = False


        if self.operation in ["ADD"]:
            scn = context.scene
            Scene_Properties = scn.Radiant_Light_Properties
            Tag_List = Scene_Properties.Tags_List

            self.tag_name = "Tag0" + str(len(Tag_List))
            return context.window_manager.invoke_props_dialog(self)
        else:
            return self.execute(context)

    def execute(self, context):

        scn = context.scene

        Scene_Properties = scn.Radiant_Light_Properties

        item_list = Scene_Properties.Tags_List
        item_index = self.index

        if self.operation == "REMOVE":

            item_list.remove(self.index)

            if len(item_list) == Scene_Properties.Tags_List_Index:
                Scene_Properties.Tags_List_Index = len(item_list) - 1





            Utility_Functions.update_UI()
            return {'FINISHED'}

        if self.operation == "ADD":
            item = item_list.add()
            item.name = self.tag_name
            Scene_Properties.Tags_List_Index = len(item_list) - 1
            Utility_Functions.update_UI()
            return {'FINISHED'}



        if self.operation == "UP":
            if item_index >= 1:
                item_list.move(item_index, item_index-1)
                Scene_Properties.Tags_List_Index -= 1
                return {'FINISHED'}

        if self.operation == "DOWN":
            if len(item_list)-1 > item_index:
                item_list.move(item_index, item_index+1)
                Scene_Properties.Tags_List_Index += 1
                return {'FINISHED'}



        if self.operation == "ASSIGN":

            objects  = [object for object in context.selected_objects if object.type == "LIGHT"]

            for object in objects:

                if len(item_list) > scn.Radiant_Light_Properties.Tags_List_Index:


                    Active_Item = item_list[scn.Radiant_Light_Properties.Tags_List_Index]
                    object_radiant_settings = object.Radiant_Light_Properties

                    object_radiant_settings.Tags = Active_Item.name

            return {'FINISHED'}

        if self.operation == "UNASSIGN":
            objects  = [object for object in context.selected_objects if object.type == "LIGHT"]

            for object in objects:

                if self.from_all:

                    object_radiant_settings = object.Radiant_Light_Properties
                    object_radiant_settings.Tags = ""

                else:

                    if len(item_list) > scn.Radiant_Light_Properties.Tags_List_Index:

                        Active_Item = item_list[scn.Radiant_Light_Properties.Tags_List_Index]
                        object_radiant_settings = object.Radiant_Light_Properties

                        if Active_Item.name == object_radiant_settings.Tags:
                            object_radiant_settings.Tags = ""


            return {'FINISHED'}



        Utility_Functions.update_UI()
        return {'FINISHED'}


classes = [RADIANT_Tags_List_Operator]

def register():
  for cls in classes:
    bpy.utils.register_class(cls)


def unregister():
  for cls in classes:
    bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
