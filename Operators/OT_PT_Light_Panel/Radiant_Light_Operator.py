import bpy
import math
import mathutils
import numpy
from Radiant import Utility_Functions
import bpy_extras.io_utils
from Radiant import Preferences
import bmesh
from Radiant import Radiant_Properties




ENUM_Position = [("CURSOR","Cursor","Cursor"),("CENTER","Center","Center"), ("SELECTED", "Selected", "Selected")]
ENUM_Type = [("POINT","Point","Point"),("SUN","Sun","Sun"),("SPOT","Spot","Spot"),("AREA","Area","Area")]
ENUM_Target_Type = [("OBJECT","Object","Object"),("CURSOR","Cursor","Cursor")]

def ENUM_Activate(self, context):

    ENUM_items = [("NONE","None","None")]

    if self.type == "POINT" or self.track_to:

        ENUM_items = [("MOVE","Move","Move"),("NONE","None","None")]

    else:

        ENUM_items = [("MOVE","Move","Move"),("ROTATE","Rotate","ROTATE"),("NONE","None","None")]

    return ENUM_items

def ENUM_Light_Groups(self, context):

    scn = context.scene
    radiant_properties = scn.Radiant_Light_Properties
    light_groups = radiant_properties.Light_Groups

    if len(light_groups) == 0:
        Items = [("None", "None", "None")]
    else:
        Items = []

    for index, light_group in enumerate(light_groups):
        Items.append((str(index), light_group.name, light_group.name))

    return Items

def ENUM_Light_Group_Mode(self, context):

    Items = [("NEW","New","New")]

    scn = context.scene
    radiant_properties = scn.Radiant_Light_Properties
    light_groups = radiant_properties.Light_Groups
    preferences = Preferences.get_addon_preferences()

    if len(light_groups) > 0:
        Items.append(("EXIST", "Exist", "Exist"))

    if preferences.Show_Light == "LIGHT_GROUP":
        if len(light_groups) > 0:
            Items.append(("ACTIVE", "Active", "Active"))

    return Items

class Radiant_OT_Add_Light(bpy.types.Operator):
    """Add Light"""
    bl_idname = "radiant.add_light"
    bl_label = "Add Light"
    bl_options = {'REGISTER', 'UNDO'}

    name: bpy.props.StringProperty(default="light")

    position: bpy.props.EnumProperty(default="CURSOR", items=ENUM_Position)

    offset: bpy.props.FloatVectorProperty(default=(0, 0, 0))

    track_to: bpy.props.BoolProperty()
    target: bpy.props.StringProperty()
    target_type: bpy.props.EnumProperty(items=ENUM_Target_Type)
    # generate_target_empty: bpy.props.BoolProperty(default=True)

    type: bpy.props.EnumProperty(default="SUN", items=ENUM_Type)

    activate: bpy.props.EnumProperty(items=ENUM_Activate)

    keep_constraint: bpy.props.BoolProperty(default=True)

    select: bpy.props.BoolProperty(default=True)

    SHOW_Light_Group: bpy.props.BoolProperty()

    Use_Light_Group: bpy.props.BoolProperty(default=False)

    Light_Groups: bpy.props.EnumProperty(items=ENUM_Light_Groups)

    Light_Group_Mode: bpy.props.EnumProperty(items=ENUM_Light_Group_Mode)

    New_Light_Group_Name: bpy.props.StringProperty(default="Light Group")

    @classmethod
    def poll(cls, context):

        if context.mode == "OBJECT":
            return True

    def draw(self, context):

        layout = self.layout
        layout.prop(self, "name", text="Name")
        layout.prop(self, "position", text="Position")

        if self.activate == "NONE":
            layout.prop(self, "offset", text="Offset")

        layout.prop(self, "type", expand=True)

        if not self.type == "POINT":
            layout.prop(self, "track_to", text="Track To")

            if self.track_to:
                layout.prop(self, "target_type", text="Target Type")
                if self.target_type == "OBJECT":
                    layout.prop_search(self, "target", context.view_layer, "objects", text="Target")
                # if self.target_type == "CURSOR":
                    # layout.prop(self, "generate_target_empty", text="Generate Target Empty")


                # layout.prop(self, "keep_constraint", text="Keep Constraint")

        layout.prop(self, "activate", text="Activate")

        layout.prop(self, "select", text="Select")


        if Utility_Functions.draw_subpanel(self, self.SHOW_Light_Group, "SHOW_Light_Group", "Light Group", layout):

            layout.prop(self, "Use_Light_Group", text="Use Light Group")

            if self.Use_Light_Group:

                col = layout.column(align=True)

                scn = context.scene
                radiant_properties = scn.Radiant_Light_Properties
                light_groups = radiant_properties.Light_Groups
                preferences = Preferences.get_addon_preferences()

                row = col.row(align=True)

                row.prop(self, "Light_Group_Mode", expand=True)

                if self.Light_Group_Mode == "EXIST":
                    col.prop(self, "Light_Groups", text="")

                if self.Light_Group_Mode == "NEW":
                    col.prop(self, "New_Light_Group_Name", text="")

                # if self.Light_Group_Mode == "ACTIVE":
                #     col.label(text=radiant_properties.Light_Groups_Enum)

    def invoke(self, context, event):

        if context.object:
            self.target = context.object.name

        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):

        light = bpy.data.lights.new(self.name, type=self.type)
        object = bpy.data.objects.new(self.name, light)
        context.collection.objects.link(object)

        mode  = context.mode
        scn = context.scene

        radiant_properties = scn.Radiant_Light_Properties
        light_groups = radiant_properties.Light_Groups

        preferences = Preferences.get_addon_preferences()
        light_group_enum = radiant_properties.Light_Groups_Enum

        if self.Use_Light_Group:

            if self.Light_Group_Mode == "NEW":
                light_group = light_groups.add()
                light_group.name = self.New_Light_Group_Name

                light_group_check = [l.Light for l in light_group.Lights]
                if not object in light_group_check:
                    lg_light = light_group.Lights.add()
                    lg_light.Light = object

            if self.Light_Group_Mode == "EXIST":

                if not self.Light_Groups == "None":
                    if len(light_groups) > int(self.Light_Groups):

                        light_group = light_groups[int(self.Light_Groups)]

                        lg_light = light_group.Lights.add()
                        lg_light.Light = object

            if self.Light_Group_Mode == "ACTIVE":

                if not light_groups == "None":
                    if len(light_groups) > int(light_group_enum):

                        light_group = light_groups[int(light_group_enum)]

                        lg_light = light_group.Lights.add()
                        lg_light.Light = object

        back_active = context.object
        back_selected = [obj for obj in context.selected_objects]
        target = context.view_layer.objects.get(self.target)


        if self.position == "CURSOR":
            object.location = context.scene.cursor.location
        if self.position == "CENTER":
            object.location = (0, 0, 0)
        if self.position == "SELECTED":
            points = [obj.matrix_world.to_translation() for obj in context.selected_objects]

            if len(points) > 0:
                object.location = Utility_Functions.midpoint(points, "BOUNDING_BOX")
            else:
                object.location = (0, 0, 0)

        if self.activate == "NONE":
            object.location += mathutils.Vector(self.offset)

        if self.track_to:

            if not self.type == "POINT":
                if target:

                    if self.target_type == "OBJECT":

                        constraint = object.constraints.new(type="TRACK_TO")

                        constraint.target = target

                    context.view_layer.update()
                    mat = object.matrix_world.copy()

                    if not self.keep_constraint:
                        object.constraints.remove(constraint)
                        context.view_layer.update()
                        object.matrix_world = mat

                if self.target_type == "CURSOR":


                    constraint = object.constraints.new(type="TRACK_TO")

                    context.view_layer.update()

                    empty = bpy.data.objects.new(object.name + "_target", object_data=None)
                    bpy.context.collection.objects.link(empty)
                    empty.location = context.scene.cursor.location

                    constraint.target = empty



        bpy.ops.object.select_all(action='DESELECT')

        object.select_set(True)
        bpy.context.view_layer.objects.active = object


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






    # target_object: bpy.props.PointerProperty(type=bpy.types.Object)


class Radiant_PT_Apply_Light_Constraint(bpy.types.Operator):
    """Apply Constraint"""
    bl_idname = "radiant.apply_light_constraint"
    bl_label = "Apply Light Constraint"
    bl_options = {'REGISTER', 'UNDO'}

    object: bpy.props.StringProperty()

    def execute(self, context):

        object = context.scene.objects.get(self.object)



        context.view_layer.update()
        mat = object.matrix_world.copy()
        object.constraints.clear()
        context.view_layer.update()
        object.matrix_world = mat



        return {'FINISHED'}

class Radiant_PT_Trackball_Light(bpy.types.Operator):
    """Rotate"""
    bl_idname = "radiant.trackball_light"
    bl_label = "Rotate"
    bl_options = {'REGISTER', 'UNDO'}

    object: bpy.props.StringProperty()

    def execute(self, context):

        object = context.scene.objects.get(self.object)



        if object:
            bpy.ops.object.select_all(action='DESELECT')

            object.select_set(True)

            bpy.context.view_layer.objects.active = object

            bpy.ops.transform.trackball("INVOKE_DEFAULT")


        return {'FINISHED'}

class Radiant_PT_Move_Light(bpy.types.Operator):
    """Move"""
    bl_idname = "radiant.move_light"
    bl_label = "Move"
    bl_options = {'REGISTER', 'UNDO'}

    object: bpy.props.StringProperty()

    def execute(self, context):

        object = context.scene.objects.get(self.object)



        if object:
            bpy.ops.object.select_all(action='DESELECT')

            object.select_set(True)

            bpy.context.view_layer.objects.active = object

            bpy.ops.transform.translate("INVOKE_DEFAULT")


        return {'FINISHED'}

ENUM_Assign_Emission_Mode = [("REPLACE","Replace Slot","Replace Slot"),("CLEAR","Clear Slot","Clear Slot")]
ENUM_Replace_Slot_Scope = [("ACTIVE","Active Object","Active Object"),("SELECTED","Selected Objects","Selected Objects")]
ENUM_Replace_By = [("MATERIAL","Material","Material"), ("INDEX","Index","INDEX")]

class Radiant_OT_Select_Object_By_Emission_Material(bpy.types.Operator):
    """Select By Material"""
    bl_idname = "radiant.select_by_emission_material"
    bl_label = "Select by Material"
    bl_options = {'REGISTER', 'UNDO'}

    material: bpy.props.StringProperty()

    def execute(self, context):

        material = bpy.data.materials.get(self.material)

        if context.mode == "OBJECT":

            if material:

                objects = context.view_layer.objects

                for object in objects:
                    for slot in object.material_slots:
                        if slot.material == material:

                            object.select_set(True)
                            bpy.context.view_layer.objects.active = object
                            break

        if context.mode == "EDIT_MESH":

            if material:

                objects = context.selected_objects

                for object in objects:

                    # if object.type == "MESH":
                    #
                    #     old_active_index = object.active_material_index
                    #
                    #     for mi, slot in enumerate(object.material_slots):
                    #         if slot.material == material:
                    #             object.active_material_index = mi
                    #             bpy.ops.object.material_slot_select()
                    #
                    #     object.active_material_index = old_active_index
                    #
                    #


                    if object.type == "MESH":
                        me = object.data
                        bm = bmesh.from_edit_mesh(me)

                        for face in bm.faces:
                            if object.material_slots[face.material_index].material == material:
                                face.select_set(True)

                        bmesh.update_edit_mesh(me, True)




        return {'FINISHED'}

class Radiant_OT_Assign_Emission_Material(bpy.types.Operator):
    """Assign Emission Material to Selected"""
    bl_idname = "radiant.assign_emission_material_to_selected"
    bl_label = "Assign Emission Material to Selected"
    bl_options = {'REGISTER', 'UNDO'}

    material: bpy.props.StringProperty()
    replace: bpy.props.BoolProperty(default=True)
    Mode: bpy.props.EnumProperty(items=ENUM_Assign_Emission_Mode)
    Scope: bpy.props.EnumProperty(items=ENUM_Replace_Slot_Scope)

    Replace_By: bpy.props.EnumProperty(items=ENUM_Replace_By)
    Replace_Use_Last: bpy.props.BoolProperty(default=False)

    Active_Object_Material_Slot: bpy.props.StringProperty()


    Slot_Index: bpy.props.IntProperty(min=0)
    Slot_Material: bpy.props.StringProperty()

    # Use_Existing_If_Available: bpy.props.BoolProperty()

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "Mode", text="Mode", expand=True)

        if self.Mode == "REPLACE":




            layout.prop(self, "Scope", text="Scope")

            if self.Scope == "ACTIVE":

                check = False

                if context.object:

                    if context.object.type == "MESH":

                        check = True

                        layout.prop_search(self, "Active_Object_Material_Slot", context.object, "material_slots", text="Slot")

                if not check:
                    layout.label(text="No Active Mesh Object Found")



            if self.Scope == "SELECTED":


                layout.prop(self, "Replace_By", text="Replace By", expand=True)

                if self.Replace_By == "INDEX":
                    layout.prop(self, "Slot_Index", text="Slot Index")
                    layout.prop(self, "Replace_Use_Last", text="Use Last Slot if index is bigger")

                if self.Replace_By == "MATERIAL":
                    layout.prop_search(self, "Slot_Material", bpy.data, "materials", text="Material")

    def invoke(self, context, event):

        if context.mode == "EDIT_MESH":
            return self.execute(context)

        if context.mode == "OBJECT":
            return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):


        material = bpy.data.materials.get(self.material)

        if context.mode == "EDIT_MESH":

            if material:

                objects = [object for object in context.selected_objects if object.type == "MESH"]

                for object in objects:
                    me = object.data
                    bm = bmesh.from_edit_mesh(me)

                    selected_faces = [face for face in bm.faces if face.select]

                    if len(selected_faces) > 0:

                        mat_index = None

                        for index, slot in enumerate(object.material_slots):
                            if slot.material == material:
                                mat_index = index
                                break

                        if mat_index == None:
                            object.data.materials.append(material)

                        for face in selected_faces:

                            if mat_index == None:
                                face.material_index = len(object.material_slots)-1
                            else:
                                face.material_index = mat_index

                    bmesh.update_edit_mesh(me, True)




        if context.mode == "OBJECT":

            objects = []

            if self.Mode == "REPLACE":

                if self.Scope == "ACTIVE":
                    if context.object:
                        if context.object.type in ["MESH", "CURVE"]:
                            objects = [context.object]

                if self.Scope == "SELECTED":
                    objects = [object for object in context.selected_objects if object.type == "MESH"]


            if self.Mode == "CLEAR":
                objects = [object for object in context.selected_objects if object.type == "MESH"]


            if material:

                if self.Mode == "CLEAR":

                    for object in objects:
                        if object.type in ["MESH", "CURVE"]:

                            object.data.materials.clear()
                            object.data.materials.append(material)

                if self.Mode == "REPLACE":

                    if self.Scope == "ACTIVE":

                        object = context.object
                        if object:
                            if object.type == "MESH":
                                material_slot = object.material_slots.get(self.Active_Object_Material_Slot)
                                if material_slot:
                                    material_slot.material = material

                    if self.Scope == "SELECTED":

                        for object in objects:
                            if object.type in ["MESH"]:

                                if self.Replace_By == "MATERIAL":

                                    for slot in object.material_slots:
                                        if slot.name == self.Slot_Material:
                                            slot.material = material

                                if self.Replace_By == "INDEX":

                                    if len(object.material_slots) > 0:
                                        if self.Slot_Index < len(object.material_slots)-1:
                                            object.material_slots[self.Slot_Index].material = material

                                        else:
                                            if self.Replace_Use_Last:
                                                object.material_slots[-1].material = material






                            #Replace Slot





                    # for slot in object.material_slots:
                    #     if slot.material == material:
                    #





        return {'FINISHED'}

def ENUM_Aim_Target_Type(self, context):

    items = [("EDITING","Editing Object","Editing Object"),("ELEMENT","Element","Element"),("OBJECT","Object","Object"),("CURSOR","Cursor","Cursor")]

    if self.Create_Mode == "INDIVIDUAL":

        if context.mode == "OBJECT":
            items = [("EDITING","Reference Object","Reference Object"), ("OBJECT","Object","Object"),("CURSOR","Cursor","Cursor")]
        if context.mode == "EDIT_MESH":
            items = [("EDITING","Editing Object","Editing Object"),("ELEMENT","Element","Element"),("OBJECT","Object","Object"),("CURSOR","Cursor","Cursor")]

    if self.Create_Mode == "MEDIAN":

        if context.mode == "OBJECT":
            items = [("ELEMENT","Midpoint","Midpoint"),("OBJECT","Object","Object"),("CURSOR","Cursor","Cursor")]
        if context.mode == "EDIT_MESH":
            items = [("ELEMENT","Midpoint","Midpoint"),("OBJECT","Object","Object"),("CURSOR","Cursor","Cursor")]

    return items

ENUM_Elements = [("VERTEX","Vertex","Vertex"),("EDGE","Edge","Edge"),("FACE","Face","Face")]
ENUM_Rotation_Mode=[("GLOBAL","Global","Global"),("LOCAL","Local","Local"),("NORMAL","Normal","Normal")]
ENUM_Offset_Orientation_Mode=[("GLOBAL","Global","Global"),("LOCAL","Local","Local"),("NORMAL","Normal","Normal")]
ENUM_Area_Shape = [("SQUARE","Square","Square"),("RECTANGLE","Rectangle","Rectangle"),("DISK","Disk","Disk"),("ELLIPSE","Ellipse","Ellipse")]
ENUM_Create_Mode = [("INDIVIDUAL","Individual","Individual"),("MEDIAN","Median","Median")]

def Update_Blackbody(self, context):
    self.color = Radiant_Properties.Blackbody_Color(self.Temperature)

def set_light_data(self, light):

    light.data.energy = self.strength
    light.data.color = self.color

    if self.type == "SPOT":
        light.data.spot_size = self.SPOT_Size
        light.data.spot_blend = self.SPOT_Blend

    if self.type == "AREA":
        light.data.shape = self.AREA_Shape
        light.data.size = self.AREA_X
        light.data.size_y = self.AREA_Y

def create_object(self, name, data=None):

    light = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(light)
    light.show_in_front = self.show_in_front
    set_light_data(self, light)

    return light

def ENUM_Orientation(self, context):

    ENUM_Items = [("LOCAL","Local","Local"),("GLOBAL","Global","Global")]

    if context.mode == "EDIT_MESH":
        ENUM_Items.append(("NORMAL","Normal","Normal"))

    return ENUM_Items


class RADIANT_MT_Radiant_Light_Ops(bpy.types.Menu):
    bl_label = "Radiant Light Add"
    bl_idname = "RADIANT_MT_radiant_light_ops"

    def draw(self, context):
        layout = self.layout
        layout.operator("radiant.add_light", text="Add Aim Light", icon="OUTLINER_OB_LIGHT")

def draw_radiant_add_menu(self, context):
    layout = self.layout
    layout.menu("RADIANT_MT_radiant_light_ops", text="Radiant", icon="LIGHT_SUN")
    layout.separator()

def draw_radiant_add_menu_edit_mesh(self, context):

    if context.mode == "EDIT_MESH":
        layout = self.layout
        layout.separator()
        layout.menu("RADIANT_MT_radiant_light_ops", text="Radiant", icon="LIGHT_SUN")

# Radiant_OT_Create_Light_At_Selected

classes = [RADIANT_MT_Radiant_Light_Ops, Radiant_OT_Assign_Emission_Material, Radiant_OT_Select_Object_By_Emission_Material, Radiant_PT_Apply_Light_Constraint, Radiant_OT_Add_Light, Radiant_PT_Aim_Light, Radiant_PT_Move_Light, Radiant_PT_Trackball_Light, Radiant_OT_Unlock_All_Light, Radiant_OT_Find_Object, Radiant_PT_Duplicate_Light, Radiant_OT_Unhide_All_Light, Radiant_OT_Solo_Light, Radiant_OT_Select, Radiant_OT_Remove]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.VIEW3D_MT_light_add.prepend(draw_radiant_add_menu)
    bpy.types.VIEW3D_MT_mesh_add.append(draw_radiant_add_menu_edit_mesh)

def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)

    bpy.types.VIEW3D_MT_light_add.remove(draw_radiant_add_menu)
    bpy.types.VIEW3D_MT_mesh_add.remove(draw_radiant_add_menu_edit_mesh)

if __name__ == "__main__":
    register()
