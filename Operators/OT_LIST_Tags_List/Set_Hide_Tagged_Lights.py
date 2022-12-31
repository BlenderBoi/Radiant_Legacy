import bpy

ENUM_Property = [("VIEWPORT","Viewport","Viewport"), ("RENDER","Render","Render"), ("LOCK","Lock","Lock")]

class Radiant_OT_Set_Hide_Tagged_Lights(bpy.types.Operator):
    """Hide Tagged Lights"""
    bl_idname = "radiant.set_hide_tagged_lights"
    bl_label = "Hide Tagged Light"
    bl_options = {'REGISTER', 'UNDO'}

    index: bpy.props.IntProperty()
    mode: bpy.props.EnumProperty(items=ENUM_Property)
    state: bpy.props.BoolProperty()

    use_toogle: bpy.props.BoolProperty()

    def invoke(self, context, event):

        if event.shift:
            self.use_toogle = True
            return self.execute(context)

        else:
            self.use_toogle = False
            self.state = not self.state
            return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout

        if self.mode == "VIEWPORT":
            if self.state:
                text = "Viewport On"
                icon = "RESTRICT_VIEW_OFF"
            else:
                text = "Viewport Off"
                icon = "RESTRICT_VIEW_ON"

        if self.mode == "RENDER":
            if self.state:
                text = "Render On"
                icon = "RESTRICT_RENDER_OFF"
            else:
                text = "Render Off"
                icon = "RESTRICT_RENDER_ON"

        if self.mode == "LOCK":



            if self.state:
                text = "Lock Light Select"
                icon = "LOCKED"
            else:
                text = "Unlock Light Select"
                icon = "UNLOCKED"



        layout.prop(self, "state", text=text, icon=icon)

    def Toogle_Settings(self, context, Tagged_Objects):

        Check = [False]

        if Check:
            if self.mode == "VIEWPORT":
                Check = [object.hide_viewport for object in Tagged_Objects]
            if self.mode == "RENDER":
                Check = [object.hide_render for object in Tagged_Objects]
            if self.mode == "LOCK":
                Check = [object.hide_select for object in Tagged_Objects]

        for object in Tagged_Objects:
            if any(Check):
                if self.mode == "VIEWPORT":
                    object.hide_viewport = False
                    object.hide_set(False)
                if self.mode == "RENDER":
                    object.hide_render = False

                if self.mode == "LOCK":
                    object.hide_select = False

            else:
                if self.mode == "VIEWPORT":
                    object.hide_viewport = True
                    object.hide_set(True)

                if self.mode == "RENDER":
                    object.hide_render = True

                if self.mode == "LOCK":
                    object.hide_select = True

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

            objects = context.view_layer.objects
            Tagged_Objects = [object for object in objects if object.type == "LIGHT" and object.Radiant_Light_Properties.Tags == Active_Tag]
            if self.use_toogle:
                self.Toogle_Settings(context, Tagged_Objects)
            else:
                for object in Tagged_Objects:

                    if self.mode == "VIEWPORT":
                        object.hide_set(not self.state)
                        object.hide_viewport = not self.state

                    if self.mode == "RENDER":
                        object.hide_render = not self.state

                    if self.mode == "LOCK":
                        object.hide_select = self.state

        return {'FINISHED'}

classes = [Radiant_OT_Set_Hide_Tagged_Lights]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
