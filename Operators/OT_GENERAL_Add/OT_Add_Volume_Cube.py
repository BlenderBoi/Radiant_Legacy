
import bpy

from Radiant import Utility_Functions



class Radiant_OT_Add_Volume_Cube(bpy.types.Operator):
    """Add Volume Cube"""
    bl_idname = "radiant.add_volume_cube"
    bl_label = "Add Volume Cube"
    bl_options = {'REGISTER', 'UNDO'}

    name: bpy.props.StringProperty(default="Volume_Cube")

    density: bpy.props.FloatProperty(default=0.03)
    anisotropy: bpy.props.FloatProperty(default=0)

    size: bpy.props.FloatVectorProperty(default=(20.0, 20.0, 20.0))

    def invoke(self, context, event):
        self.location = context.scene.cursor.location
        return self.execute(context)


    def draw(self, context):
        layout = self.layout
        layout.prop(self, "size", text="Size")
        layout.separator()
        layout.prop(self, "density", text="Density")
        layout.prop(self, "anisotropy", text="Anisotropy")

    @classmethod
    def poll(cls, context):

        if context.mode == "OBJECT":
            return True

    def execute(self, context):

        filename = "VolumeCube.blend"

        filepath = Utility_Functions.get_asset_file(filename)
        object_name = "Volume_Cube"

        appended_object = Utility_Functions.append_object(filepath, object_name)
        appended_object.name = self.name
        appended_object.location = self.location

        appended_object.scale = self.size
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

        material = appended_object.material_slots[0].material
        nodes = material.node_tree.nodes

        volume_node = nodes.get("PrincipledVolumeNode")
        volume_node.inputs["Density"].default_value = self.density
        volume_node.inputs["Anisotropy"].default_value = self.anisotropy



        return {'FINISHED'}


classes = [Radiant_OT_Add_Volume_Cube]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
