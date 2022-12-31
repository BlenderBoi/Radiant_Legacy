import bpy
import mathutils
import numpy
import os
import bpy_extras
import rna_prop_ui

script_file = os.path.realpath(__file__)
addon_directory = os.path.dirname(script_file)
addon_name = os.path.basename(addon_directory)

default_color = [0.000000, 0.113775, 1.000000, 1.000000]

inf = 340282346638528859811704183484516925440


def Create_Raymesh_Properties(object):


    if object.data.type in ["AREA"]:


        if not object.data.get("Area Spread"):
            rna_prop_ui.rna_idprop_ui_create( object.data, "Area Spread", default=0.0, min=-90.0, max=179.0, soft_min=None, soft_max=None, description=None, overridable=False, subtype=None)

        if not object.data.get("Emit Light"):
            rna_prop_ui.rna_idprop_ui_create( object.data, "Emit Light", default=0.0, min=0.0, max=1.0, soft_min=None, soft_max=None, description=None, overridable=False, subtype=None)

        if not object.data.get("Glow Depth"):
            rna_prop_ui.rna_idprop_ui_create( object.data, "Glow Depth", default=2.0, min=0.0, max=inf, soft_min=None, soft_max=None, description=None, overridable=False, subtype=None)

        if not object.data.get("Glow Direction X"):
            rna_prop_ui.rna_idprop_ui_create( object.data, "Glow Direction X", default=0.0, min=-inf, max=inf, soft_min=None, soft_max=None, description=None, overridable=False, subtype=None)

        if not object.data.get("Glow Direction Y"):
            rna_prop_ui.rna_idprop_ui_create( object.data, "Glow Direction Y", default=0.0, min=-inf, max=inf, soft_min=None, soft_max=None, description=None, overridable=False, subtype=None)

        if not object.data.get("Glow Direction Z"):
            rna_prop_ui.rna_idprop_ui_create( object.data, "Glow Direction Z", default=0.0, min=0.0, max=inf, soft_min=None, soft_max=None, description=None, overridable=False, subtype=None)

        if not object.data.get("Glow Falloff"):
            rna_prop_ui.rna_idprop_ui_create( object.data, "Glow Falloff", default=5.0, min=0.0, max=inf, soft_min=None, soft_max=None, description=None, overridable=False, subtype=None)

        if not object.data.get("Glow Opacity"):
            rna_prop_ui.rna_idprop_ui_create( object.data, "Glow Opacity", default=1.0, min=0.0, max=1.0, soft_min=None, soft_max=None, description=None, overridable=False, subtype=None)

        if not object.data.get("Glow Softness"):
            rna_prop_ui.rna_idprop_ui_create( object.data, "Glow Softness", default=1.0, min=0.0, max=inf, soft_min=None, soft_max=None, description=None, overridable=False, subtype=None)

        if not object.data.get("Glow Strength"):
            rna_prop_ui.rna_idprop_ui_create( object.data, "Glow Strength", default=1.0, min=0.0, max=inf, soft_min=None, soft_max=None, description=None, overridable=False, subtype=None)

        if not object.data.get("Master Strength"):
            rna_prop_ui.rna_idprop_ui_create( object.data, "Master Strength", default=1.0, min=0.0, max=inf, soft_min=None, soft_max=None, description=None, overridable=False, subtype=None)

        if not object.data.get("Offset Z"):
            rna_prop_ui.rna_idprop_ui_create( object.data, "Offset Z", default=0.0, min=-inf, max=inf, soft_min=None, soft_max=None, description=None, overridable=False, subtype=None)

        if not object.data.get("Resolution"):
            rna_prop_ui.rna_idprop_ui_create( object.data, "Resolution", default=32, min=0, max=512, soft_min=None, soft_max=None, description=None, overridable=False, subtype=None)

        if not object.data.get("Shade Smooth"):
            rna_prop_ui.rna_idprop_ui_create( object.data, "Shade Smooth", default=1, min=0, max=1, soft_min=None, soft_max=None, description=None, overridable=False, subtype=None)

        if not object.data.get("Source"):
            rna_prop_ui.rna_idprop_ui_create( object.data, "Source", default=1, min=0, max=1, soft_min=None, soft_max=None, description=None, overridable=False, subtype=None)

        if not object.data.get("Source Strength"):
            rna_prop_ui.rna_idprop_ui_create( object.data, "Source Strength", default=1.0, min=0.0, max=inf, soft_min=None, soft_max=None, description=None, overridable=False, subtype=None)


    if object.data.type in ["SPOT"]:


        if not object.data.get("Emit Light"):
            rna_prop_ui.rna_idprop_ui_create( object.data, "Emit Light", default=0.0, min=0.0, max=1.0, soft_min=None, soft_max=None, description=None, overridable=False, subtype=None)

        if not object.data.get("Glow Depth"):
            rna_prop_ui.rna_idprop_ui_create( object.data, "Glow Depth", default=5.0, min=0.0, max=inf, soft_min=None, soft_max=None, description=None, overridable=False, subtype=None)

        if not object.data.get("Glow Falloff"):
            rna_prop_ui.rna_idprop_ui_create( object.data, "Glow Falloff", default=2.0, min=0.0, max=inf, soft_min=None, soft_max=None, description=None, overridable=False, subtype=None)

        if not object.data.get("Glow Opacity"):
            rna_prop_ui.rna_idprop_ui_create( object.data, "Glow Opacity", default=1.0, min=0.0, max=1.0, soft_min=None, soft_max=None, description=None, overridable=False, subtype=None)

        if not object.data.get("Glow Strength"):
            rna_prop_ui.rna_idprop_ui_create( object.data, "Glow Strength", default=1.0, min=0.0, max=inf, soft_min=None, soft_max=None, description=None, overridable=False, subtype=None)

        if not object.data.get("Resolution"):
            rna_prop_ui.rna_idprop_ui_create( object.data, "Resolution", default=256, min=3, max=512, soft_min=None, soft_max=None, description=None, overridable=False, subtype=None)

        if not object.data.get("Shade Smooth"):
            rna_prop_ui.rna_idprop_ui_create( object.data, "Shade Smooth", default=0, min=0, max=1, soft_min=None, soft_max=None, description=None, overridable=False, subtype=None)



    if object.data.type in ["POINT"]:

        if not object.data.get("Core Opacity"):
            rna_prop_ui.rna_idprop_ui_create( object.data, "Core Opacity", default=1.0, min=0.0, max=1.0, soft_min=None, soft_max=None, description=None, overridable=False, subtype=None)

        if not object.data.get("Core Size"):
            rna_prop_ui.rna_idprop_ui_create( object.data, "Core Size", default=0.20, min=0.0, max=inf, soft_min=None, soft_max=None, description=None, overridable=False, subtype=None)

        if not object.data.get("Core Softness"):
            rna_prop_ui.rna_idprop_ui_create( object.data, "Core Softness", default=10.0, min=0.0, max=inf, soft_min=None, soft_max=None, description=None, overridable=False, subtype=None)

        if not object.data.get("Core Strength"):
            rna_prop_ui.rna_idprop_ui_create( object.data, "Core Strength", default=5.0, min=0.0, max=inf, soft_min=None, soft_max=None, description=None, overridable=False, subtype=None)

        if not object.data.get("Emit Light"):
            rna_prop_ui.rna_idprop_ui_create( object.data, "Emit Light", default=0.0, min=0.0, max=1.0, soft_min=None, soft_max=None, description=None, overridable=False, subtype=None)

        if not object.data.get("Glow Opacity"):
            rna_prop_ui.rna_idprop_ui_create( object.data, "Glow Opacity", default=1.0, min=0.0, max=1.0, soft_min=None, soft_max=None, description=None, overridable=False, subtype=None)

        if not object.data.get("Glow Size"):
            rna_prop_ui.rna_idprop_ui_create( object.data, "Glow Size", default=1.0, min=0.0, max=inf, soft_min=None, soft_max=None, description=None, overridable=False, subtype=None)

        if not object.data.get("Glow Softness"):
            rna_prop_ui.rna_idprop_ui_create( object.data, "Glow Softness", default=10.0, min=0.0, max=inf, soft_min=None, soft_max=None, description=None, overridable=False, subtype=None)

        if not object.data.get("Glow Strength"):
            rna_prop_ui.rna_idprop_ui_create( object.data, "Glow Strength", default=1.0, min=0.0, max=inf, soft_min=None, soft_max=None, description=None, overridable=False, subtype=None)

        if not object.data.get("Master Size"):
            rna_prop_ui.rna_idprop_ui_create( object.data, "Master Size", default=1.0, min=0.0, max=inf, soft_min=None, soft_max=None, description=None, overridable=False, subtype=None)

        if not object.data.get("Master Strength"):
            rna_prop_ui.rna_idprop_ui_create( object.data, "Master Strength", default=1.0, min=0.0, max=inf, soft_min=None, soft_max=None, description=None, overridable=False, subtype=None)

        if not object.data.get("Resolution"):
            rna_prop_ui.rna_idprop_ui_create( object.data, "Resolution", default=32, min=4, max=512, soft_min=None, soft_max=None, description=None, overridable=False, subtype=None)

        if not object.data.get("Shade Smooth"):
            rna_prop_ui.rna_idprop_ui_create( object.data, "Shade Smooth", default=1, min=0, max=1, soft_min=None, soft_max=None, description=None, overridable=False, subtype=None)





def get_user_defined_custom_properties(source):

    items = []

    if source:
        src_type = type(source)
        type_dict = dir(src_type)

        for k, v in source.items():

            if k in type_dict:

                tmp = getattr(src_type, k)

                if isinstance(tmp, bpy.props._PropertyDeferred):
                    continue

            if not isinstance(v, (int, float)):
                continue

            item = k
            items.append(item)

    return items


def get_addon_name():

    return addon_name

def get_addon_preferences():

    addon_preferences = bpy.context.preferences.addons[addon_name].preferences

    return addon_preferences


def Create_Empty(name):

    object = bpy.data.objects.new(name, None)
    bpy.context.collection.objects.link(object)

    return object

#Preferences


def get_object_indices(object):

    if object.type == "MESH":
        indices = [vertex.index for vertex in object.data.vertices]
        return indices

    else:
        return None

#Assets
def append_object_normal(filepath, object_name):

    blendfile = filepath
    section   = "\\Object\\"
    object    = object_name

    directory = blendfile + section
    filename  = object

    bpy.ops.wm.append(filename=filename, directory=directory)
    selected_objects = [object for object in bpy.context.selected_objects]

    if len(selected_objects) > 0:
        bpy.context.view_layer.objects.active = selected_objects[0]


    return selected_objects




def append_object(filepath, object_name):

    blendfile = filepath
    section   = "\\Object\\"
    object    = object_name

    directory = blendfile + section
    filename  = object

    bpy.ops.wm.append(filename=filename, directory=directory)
    selected_objects = [object for object in bpy.context.selected_objects]

    bpy.context.view_layer.objects.active = selected_objects[0]

    if len(selected_objects) == 0:
        return None

    if len(selected_objects) == 1:
        return selected_objects[0]

    if len(selected_objects) > 1:
        return selected_objects

def get_asset_folder():

    script_file = os.path.realpath(__file__)
    addon_directory = os.path.dirname(script_file)
    Assets_Folder = os.path.join(addon_directory, "Assets")

    return Assets_Folder

def get_asset_file(filename):

    Assets_Folder = get_asset_folder()
    filepath = os.path.join(Assets_Folder, filename)

    return filepath

#UI
def update_UI():
    for screen in bpy.data.screens:
        for area in screen.areas:
            area.tag_redraw()





def draw_subpanel(self, boolean, property, label, layout):

    if boolean:
        ICON = "TRIA_DOWN"
    else:
        ICON = "TRIA_RIGHT"

    row = layout.row(align=True)
    row.alignment = "LEFT"
    row.prop(self, property, text=label, emboss=False, icon=ICON)

    return boolean

def draw_subpanel_left(self, boolean, property, label, layout):

    if boolean:
        ICON = "TRIA_DOWN"
    else:
        ICON = "TRIA_LEFT"

    row = layout.row(align=True)
    row.alignment = "LEFT"
    row.prop(self, property, text=label, emboss=False, icon=ICON)

    return boolean

def draw_subpanel_style02(self, boolean, property, label, layout):

    if boolean:
        ICON = "TRIA_DOWN"
    else:
        ICON = "TRIA_LEFT"

    row = layout.row(align=True)
    row.alignment = "LEFT"
    row.prop(self, property, text=label, emboss=False, icon=ICON)

    return boolean

def draw_subpanel_checkbox(self, boolean, property, self2, property2, label, layout):

    if boolean:
        ICON = "TRIA_DOWN"
    else:
        ICON = "TRIA_RIGHT"

    row = layout.row(align=True)
    row.alignment = "LEFT"
    row.prop(self, property, text="", emboss=False, icon=ICON)
    row.prop(self2, property2, text="")
    row.prop(self, property, text=label, emboss=False)

    return boolean

#Calculation

def get_bounding_box(object):

    bbox_corners = [object.matrix_world * mathutils.Vector(corner) for corner in object.bound_box]

    return bbox_corners

def midpoint(coordinates, mode):

    if len(coordinates) > 0:

        if mode == "BOUNDING_BOX":

            x= []
            y= []
            z= []

            for coordinate in coordinates:
                x.append(coordinate[0])
                y.append(coordinate[1])
                z.append(coordinate[2])

            range_x = (max(x), min(x))
            range_y = (max(y), min(y))
            range_z = (max(z), min(z))

            bounding_box_coordinate = []

            for a in range_x:
                for b in range_y:
                    for c in range_z:
                        bounding_box_coordinate.append((a, b, c))

            return mathutils.Vector(numpy.array(bounding_box_coordinate).mean(axis=0))

        if mode == "CENTER":
            return mathutils.Vector(numpy.array(coordinates).mean(axis=0))
    else:
        return None

def Set_Tags(Tag_Name, object):

    scn = bpy.context.scene
    scn_properties = scn.Radiant_Light_Properties

    Tags_List = scn_properties.Tags_List
    Tags_Check = [Tag.name for Tag in scn_properties.Tags_List]

    if not Tag_Name in Tags_Check:
        scn_properties.Tags_List_Index = len(Tags_List)
        Item = Tags_List.add()
        Item.name = Tag_Name

    object.Radiant_Light_Properties.Tags = Tag_Name

def get_selected_midpoint(mode="BOUNDING_BOX"):

    points = [obj.matrix_world.to_translation() for obj in bpy.context.selected_objects]

    location = (0, 0, 0)

    if len(points) > 0:
        location = midpoint(points, mode)

    return location

def get_object_center(object, mode):

    if mode == "ORIGIN":
        # return object.matrix_world.inverted() @ object.location
        return object.matrix_world.inverted() @ object.matrix_world.to_translation()

    if mode in ["CENTER", "BOUNDING_BOX"]:

        if not object.type in ["MESH","CURVE" , "ARMATURE"]:
            # return object.matrix_world.inverted() @ object.location
            return object.matrix_world.inverted() @ object.matrix_world.to_translation()

        if object.type == "MESH":
            # create_lists = [object.matrix_world @ vert.co for vert in object.data.vertices]
            create_lists = [vert.co for vert in object.data.vertices]

        if object.type == "CURVE":

            create_lists = []

            for spline in object.data.splines:

                for point in spline.points:
                    # create_lists.append(object.matrix_world @ point.co)
                    create_lists.append(point.co.xyz)

                for bezier_point in spline.bezier_points:
                    # create_lists.append(object.matrix_world @ bezier_point.co)
                    create_lists.append(bezier_point.co.xyz)

        if object.type == "ARMATURE":

            create_lists = []

            for bone in object.data.bones:
                # create_lists.append(object.matrix_world @ bone.head)
                # create_lists.append(object.matrix_world @ bone.tail)

                create_lists.append(bone.head)
                create_lists.append(bone.tail)

        if mode == "CENTER":
            return midpoint(create_lists, "CENTER")

        if mode == "BOUNDING_BOX":
            return midpoint(create_lists, "BOUNDING_BOX")

def Blackbody_Color(t):

    blackbody_table_r = [
        [2.52432244e+03, -1.06185848e-03, 3.11067539e+00],
        [3.37763626e+03, -4.34581697e-04, 1.64843306e+00],
        [4.10671449e+03, -8.61949938e-05, 6.41423749e-01],
        [4.66849800e+03, 2.85655028e-05, 1.29075375e-01],
        [4.60124770e+03, 2.89727618e-05, 1.48001316e-01],
        [3.78765709e+03, 9.36026367e-06, 3.98995841e-01],
    ];

    blackbody_table_g = [
        [-7.50343014e+02, 3.15679613e-04, 4.73464526e-01],
        [-1.00402363e+03, 1.29189794e-04, 9.08181524e-01],
        [-1.22075471e+03, 2.56245413e-05, 1.20753416e+00],
        [-1.42546105e+03, -4.01730887e-05, 1.44002695e+00],
        [-1.18134453e+03, -2.18913373e-05, 1.30656109e+00],
        [-5.00279505e+02, -4.59745390e-06, 1.09090465e+00],
    ];

    blackbody_table_b = [
        [0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0],
        [-2.02524603e-11, 1.79435860e-07, -2.60561875e-04, -1.41761141e-02],
        [-2.22463426e-13, -1.55078698e-08, 3.81675160e-04, -7.30646033e-01],
        [6.72595954e-13, -2.73059993e-08, 4.24068546e-04, -7.52204323e-01],
    ];


    if t >= 12000.0:
        return [0.826270103, 0.994478524, 1.56626022];
    if t < 965.0:
        return [4.70366907, 0.0, 0.0]

    i = 0
    if t >= 6365.0:
        i = 5
    elif t >= 3315.0:
        i = 4
    elif t >= 1902.0:
        i = 3
    elif t >= 1449.0:
        i = 2
    elif t >= 1167.0:
        i = 1
    else:
        i = 0

    r = blackbody_table_r[i]
    g = blackbody_table_g[i]
    b = blackbody_table_b[i]

    t_inv = 1 / t
    return [r[0] * t_inv + r[1] * t + r[2],
           g[0] * t_inv + g[1] * t + g[2],
           ((b[0] * t + b[1]) * t + b[2]) * t + b[3]]

#Normals Calculation

def Average_Normals(Normals):
    average_normals = mathutils.Vector(numpy.sum(Normals, axis=0) / len(Normals))
    return average_normals

def Normal_To_Orientation(object, location, normal):

    mw = object.matrix_world.copy()

    o = location
    axis_src = normal
    axis_dst = mathutils.Vector((0, 0, -1))

    matrix_rotate = mw.to_3x3()
    matrix_rotate = matrix_rotate @ axis_src.rotation_difference(axis_dst).to_matrix().inverted()
    matrix_translation = mathutils.Matrix.Translation(mw @ o)

    Normal_Matrix = matrix_translation @ matrix_rotate.to_4x4()

    return Normal_Matrix

def Normal_To_Offset(object, location, normal, offset):

    mw = object.matrix_world.copy()

    o = location
    axis_src = normal
    axis_dst = mathutils.Vector((0, 0, 1))

    matrix_rotate = mw.to_3x3()
    matrix_rotate = matrix_rotate @ axis_src.rotation_difference(axis_dst).to_matrix().inverted()
    matrix_translation = mathutils.Matrix.Translation(mw @ o)

    Normal_Matrix = matrix_translation @ matrix_rotate.to_4x4() @ mathutils.Vector(offset)
    Normal_Offset = object.matrix_world.inverted() @ Normal_Matrix

    return Normal_Offset

#Utility

def object_switch_mode(object, mode):

    bpy.context.view_layer.update()

    Previous_Mode = object.mode

    if not object.visible_get():

        if not bpy.context.collection.objects.get(object.name):

            bpy.context.collection.objects.link(object)



    object.hide_viewport = False
    object.hide_set(False)

    object.hide_select = False

    if object.visible_get():

        object.select_set(True)
        bpy.context.view_layer.objects.active = object
        bpy.ops.object.mode_set(mode=mode, toggle=False)

        return Previous_Mode

def get_objects(mode, context):

    objects = context.selected_objects

    if mode == "EDIT_MESH":
        objects = [object for object in context.objects_in_mode]

    if mode == "OBJECT":
        objects = [object for object in context.selected_objects]

    return objects

def Add_Aim_Constraint(object, target):
    constraint = object.constraints.new("TRACK_TO")
    constraint.target = target

    return constraint

def Apply_Constraint(object, constraint):

    bpy.context.view_layer.update()
    mw = object.matrix_world.copy()
    object.constraints.remove(constraint)
    object.matrix_world = mw

#Create Object

def Create_Target_Empty(name, collection=None):

    object = bpy.data.objects.new(name, None)

    if collection:
        collection.objects.link(object)
    else:
        bpy.context.collection.objects.link(object)

    return object

def Create_Light_Data(name, type):
    data = bpy.data.lights.new(name, type)
    return data

def Create_Light(name, type="SUN", light_data=None, collection=None):

    if light_data:
        light = light_data
    else:
        light = bpy.data.lights.new(name, type=type)

    object = bpy.data.objects.new(name, light)


    if collection:
        collection.objects.link(object)
    else:
        bpy.context.collection.objects.link(object)

    return object


#Collection
def Find_Or_Create_Collection(use_collection, name):

    bpy.context.view_layer.update()

    Collection = None

    if use_collection:

        Collection = bpy.data.collections.get(name)

        if not Collection:
            Collection = bpy.data.collections.new(name)
            bpy.context.collection.children.link(Collection)

    return Collection

#Nodes
def Get_Node_Inputs(node, slots):

    input = [link.from_node for link in node.inputs[slots].links]
    if len(input) == 0:
        return None
    else:
        return input[0]

def New_Node_To_Slot(node_tree, node_type ,from_node, from_slot, to_slot):

    nodes = node_tree.nodes
    new_node = nodes.new(node_type)
    new_node.location = from_node.location
    new_node.location.x -= 250

    node_tree.links.new(from_node.inputs[from_slot], new_node.outputs[to_slot])

    return new_node

def New_Node_To_Slot_Conflict_Check(node_tree, node_type ,from_node, from_slot, to_slot, conflict_solver):

    input_check = Get_Node_Inputs(from_node, from_slot)

    conflict = None

    if input_check:
        if input_check.type == node_type.replace("ShaderNode", "").upper():
            new_node = input_check

        else:

            if conflict_solver == "SKIP":
                message = "Node Tree Confict, Operation Skipped"

                new_node = None
                conflict = message

                return {"node": new_node, "conflict": conflict}

            if conflict_solver == "FORCE":

                new_node = New_Node_To_Slot(node_tree, node_type ,from_node, from_slot, to_slot)
                message = "Disconnected " + input_check.name + " and reconnected " + new_node.name + " to " + from_node.name
                conflict = message

                return {"node": new_node, "conflict": conflict}

    else:
        new_node = New_Node_To_Slot(node_tree, node_type ,from_node, from_slot, to_slot)
        conflict = None

        return {"node": new_node, "conflict": conflict}

    return {"node": new_node, "conflict": conflict}

def get_input_nodes(self, node, types):

    for input in node.inputs:
        for link in input.links:

            from_node = link.from_node

            get_input_nodes(self, from_node, types)

            if from_node.type in types:
                self.is_emission = True
                self.input_nodes.append(from_node)

def find_input_nodes(self, data, types):

    self.input_nodes = []
    self.is_emission = False

    node_tree = data.node_tree
    output_node = node_tree.get_output_node('CYCLES')

    for input in output_node.inputs:
        for link in input.links:

            from_node = link.from_node

            get_input_nodes(self, from_node, types)

            if from_node.type == "EMISSION":
                self.is_emission = True

            if from_node.type in types:
                self.is_emission = True
                self.input_nodes.append(from_node)



def Append_New_Emission_Material(object, color=(1, 1, 1, 1), strength=1000):

    material = bpy.data.materials.new(object.name)
    object.data.materials.append(material)
    material.use_nodes = True

    principled_bsdf = material.node_tree.nodes.get("Principled BSDF")
    output_node = material.node_tree.get_output_node("ALL")

    material.node_tree.nodes.remove(principled_bsdf)
    emission = material.node_tree.nodes.new(type="ShaderNodeEmission")

    material.node_tree.links.new(emission.outputs["Emission"], output_node.inputs["Surface"])

    emission.inputs["Color"].default_value = color
    emission.inputs["Strength"].default_value = strength

    return material



def check_bone_select(bone, mode):

    if mode == "EDIT_ARMATURE":
        return bone.select

    if mode == "POSE":
        return bone.bone.select
