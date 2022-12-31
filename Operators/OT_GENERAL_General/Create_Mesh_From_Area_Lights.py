import bpy
import bmesh
import mathutils
from Radiant import Utility_Functions




ENUM_Energy_Mode=[("LIGHT","From Lights","From Lights"), ("SET","Set","Set")]
ENUM_Bind_Target=[("NONE","None","None"),("TO_LIGHT","To Light","Mesh to Light"),("TO_MESH","To Mesh","Light to Mesh")]
ENUM_Bind_Mode = [("PARENT_AND_COPY_TRANSFORM","Parent And Copy Transform","Parent And Copy Transform"), ("COPY_TRANSFORM","Copy Transform (Constraints)","Copy Transform (Constraints)"),("PARENT","Parent","Parent")]

ENUM_Driver = [("LIGHT","Light","Light"),("MATERIAL","Object Material","Object Material")]

class Radiant_OT_Create_Mesh_From_Area_Lights(bpy.types.Operator):
    """Create Mesh from Area Lights"""
    bl_idname = "radiant.create_mesh_from_area_lights"
    bl_label = "Create Mesh From Area Lights"
    bl_options = {'REGISTER', 'UNDO'}

    ELLIPSE_Segments: bpy.props.IntProperty(default=32, min=3)
    QUAD_Segments: bpy.props.IntProperty(default=0, soft_max = 10, min=0)
    Mesh_Prefix: bpy.props.StringProperty(default="Mesh_")

    Energy_Mode: bpy.props.EnumProperty(items=ENUM_Energy_Mode)
    Set_Energy: bpy.props.FloatProperty(default=1)

    Bind_Target: bpy.props.EnumProperty(items=ENUM_Bind_Target, default="TO_LIGHT")
    Bind_Type: bpy.props.EnumProperty(items=ENUM_Bind_Mode)

    Lock_Child_Selection: bpy.props.BoolProperty(default=False)




    Use_Driver: bpy.props.BoolProperty(default=False)
    Driver: bpy.props.EnumProperty(items=ENUM_Driver)
    Set_Up_Driver_Color: bpy.props.BoolProperty(default=False)
    Set_Up_Driver_Strength: bpy.props.BoolProperty(default=False)


    def draw(self, context):
        layout = self.layout
        layout.prop(self, "Mesh_Prefix", text="Prefix")

        col = layout.column(align=True)
        col.label(text="Energy")
        row = col.row(align=True)
        row.prop(self, "Energy_Mode", text="")

        if self.Energy_Mode == "SET":
            row.prop(self, "Set_Energy", text="Energy")

        col.separator()
        col.label(text="Segments")

        row = col.row()
        row.prop(self, "ELLIPSE_Segments", text="Ellipse Segments")
        row.prop(self, "QUAD_Segments", text="Quad Segments")

        col.separator()
        col.label(text="Bind")
        row = col.row(align=True)
        row.prop(self, "Bind_Target", text="Parent", expand=True)

        if self.Bind_Target in ["TO_MESH", "TO_LIGHT"]:
            col.prop(self, "Lock_Child_Selection", text="Lock Binded Selection")

        col.separator()


        col.prop(self, "Use_Driver", text="Use Driver")

        if self.Use_Driver:
            row = col.row(align=True)
            row.prop(self,"Set_Up_Driver_Color",text="Drive Color")
            row.prop(self,"Set_Up_Driver_Strength",text="Drive Strength")

            if self.Set_Up_Driver_Color or self.Set_Up_Driver_Strength:
                col.prop(self,"Driver",text="Driver")

    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)

    @classmethod
    def poll(cls, context):

        if context.mode == "OBJECT":
            return True

    def execute(self, context):
        selected_lights = [object for object in context.selected_objects if object.type == "LIGHT"]

        for object in selected_lights:
            if object.data.type == "AREA":

                bm = bmesh.new()

                if object.data.shape in ["DISK", "ELLIPSE"]:

                    segments = self.ELLIPSE_Segments
                    bmesh.ops.create_circle(bm, cap_ends=True, radius=1, segments=segments)

                if object.data.shape in ["SQUARE", "RECTANGLE"]:

                    segments = self.QUAD_Segments
                    bmesh.ops.create_grid(bm, x_segments=segments, y_segments=segments, size=1)

                x = object.data.size / 2
                y = object.data.size / 2

                if object.data.shape in ["ELLIPSE", "RECTANGLE"]:
                    y = object.data.size_y / 2

                Vector = mathutils.Vector([x, y, 1])
                Verts = bm.verts
                bmesh.ops.scale(bm, vec=Vector, verts=Verts, use_shapekey=False)

                name = self.Mesh_Prefix + object.name
                mesh = bpy.data.meshes.new(name)

                bm.to_mesh(mesh)
                bm.free()

                Mesh_Object = bpy.data.objects.new(name, mesh)
                Mesh_Object.matrix_world = object.matrix_world
                bpy.context.collection.objects.link(Mesh_Object)

                bpy.context.view_layer.objects.active = Mesh_Object
                Mesh_Object.select_set(True)

                color = [object.data.color[0], object.data.color[1], object.data.color[2], 1]

                if self.Energy_Mode == "SET":
                    strength = self.Set_Energy
                if self.Energy_Mode == "LIGHT":
                    strength = object.data.energy

                material = Utility_Functions.Append_New_Emission_Material(Mesh_Object, color=color, strength=strength)

                context.view_layer.update()

                if self.Bind_Target == "TO_MESH":
                    mw = object.matrix_world

                    object.parent = Mesh_Object
                    object.matrix_world = mw
                    if self.Lock_Child_Selection:
                        object.hide_select = True

                if self.Bind_Target == "TO_LIGHT":
                    mw = Mesh_Object.matrix_world

                    Mesh_Object.parent = object
                    Mesh_Object.matrix_world = mw
                    if self.Lock_Child_Selection:
                        Mesh_Object.hide_select = True

                if self.Use_Driver:
                    if self.Set_Up_Driver_Color or self.Set_Up_Driver_Strength:
                        if self.Driver == "LIGHT":
                            light = object.data
                            mat = material

                            for node in mat.node_tree.nodes:

                                if node.type == "EMISSION":

                                    if self.Set_Up_Driver_Color:

                                        d = node.inputs["Color"].driver_add( "default_value", 0 ).driver

                                        v = d.variables.new()
                                        v.name = "light_color"
                                        v.targets[0].id_type = "LIGHT"
                                        v.targets[0].id = light
                                        v.targets[0].data_path = "color[0]"
                                        d.expression = v.name

                                        d = node.inputs["Color"].driver_add( "default_value", 1 ).driver

                                        v = d.variables.new()
                                        v.name = "light_color"
                                        v.targets[0].id_type = "LIGHT"
                                        v.targets[0].id = light
                                        v.targets[0].data_path = "color[1]"
                                        d.expression = v.name

                                        d = node.inputs["Color"].driver_add( "default_value", 2 ).driver

                                        v = d.variables.new()
                                        v.name = "light_color"
                                        v.targets[0].id_type = "LIGHT"
                                        v.targets[0].id = light
                                        v.targets[0].data_path = "color[2]"
                                        d.expression = v.name


                                    if self.Set_Up_Driver_Strength:

                                        d = node.inputs["Strength"].driver_add( "default_value").driver

                                        v = d.variables.new()
                                        v.name = "light_strength"
                                        v.targets[0].id_type = "LIGHT"
                                        v.targets[0].id = light
                                        v.targets[0].data_path = "energy"
                                        d.expression = v.name

                                    break

                        if self.Driver == "MATERIAL":
                            light = object.data
                            mat = material

                            if self.Set_Up_Driver_Color:

                                d = light.driver_add( "color", 0 ).driver

                                v = d.variables.new()
                                v.name = "emission_color"
                                v.targets[0].id_type = "MATERIAL"
                                v.targets[0].id = mat
                                v.targets[0].data_path = 'node_tree.nodes["Emission"].inputs[0].default_value[0]'
                                d.expression = v.name

                                d = light.driver_add( "color", 1 ).driver

                                v = d.variables.new()
                                v.name = "emission_color"
                                v.targets[0].id_type = "MATERIAL"
                                v.targets[0].id = mat
                                v.targets[0].data_path = 'node_tree.nodes["Emission"].inputs[0].default_value[1]'
                                d.expression = v.name

                                d = light.driver_add( "color", 2 ).driver

                                v = d.variables.new()
                                v.name = "emission_color"
                                v.targets[0].id_type = "MATERIAL"
                                v.targets[0].id = mat
                                v.targets[0].data_path = 'node_tree.nodes["Emission"].inputs[0].default_value[2]'
                                d.expression = v.name

                            if self.Set_Up_Driver_Strength:

                                d = light.driver_add( "energy").driver

                                v = d.variables.new()
                                v.name = "emission_strength"
                                v.targets[0].id_type = "MATERIAL"
                                v.targets[0].id = mat
                                v.targets[0].data_path = 'node_tree.nodes["Emission"].inputs[1].default_value'
                                d.expression = v.name








#LIGHT, MATERIAL
    # SHOW_Driver: bpy.props.BoolProperty(default=False)
    # Driver: bpy.props.EnumProperty(items=ENUM_Driver)
    # Set_Up_Driver_Color: bpy.props.BoolProperty(default=False)
    # Set_Up_Driver_Strength: bpy.props.BoolProperty(default=False)




        return {'FINISHED'}


classes = [Radiant_OT_Create_Mesh_From_Area_Lights]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
