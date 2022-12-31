import bpy


class Radiant_OT_Select_Tagged_Lights(bpy.types.Operator):
    """Select Tagged Lights"""
    bl_idname = "radiant.select_tagged_lights"
    bl_label = "Select Tagged Light"
    bl_options = {'REGISTER', 'UNDO'}

    Deselect_All: bpy.props.BoolProperty()
    index: bpy.props.IntProperty()

    def invoke(self, context, event):
        if event.shift:
            self.Deselect_All = True

        else:
            self.Deselect_All = False

        return self.execute(context)

    def execute(self, context):

        scn = context.scene
        scn_properties = scn.Radiant_Light_Properties
        Tag_List = scn_properties.Tags_List
        Tag_Index = self.index

        Active_Tag = None

        context.view_layer.update()

        if len(scn_properties.Tags_List) > 0:
            Active_Tag = scn_properties.Tags_List[Tag_Index].name

        if Active_Tag:

            if self.Deselect_All:
                bpy.ops.object.select_all(action='DESELECT')

            objects = context.view_layer.objects
            Tagged_Objects = [object for object in objects if object.type == "LIGHT" and object.Radiant_Light_Properties.Tags == Active_Tag]
            Select_Check = [object.select_get() for object in Tagged_Objects]

            for object in Tagged_Objects:
                if any(Select_Check):
                    object.select_set(False)
                else:
                    object.select_set(True)


                if object.select_get():
                    context.view_layer.objects.active = object

        return {'FINISHED'}

classes = [Radiant_OT_Select_Tagged_Lights]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
