import bpy
import os 

def import_file(dir_path, file_name, extension='.obj'):
    full_path = os.path.join(dir_path, file_name) + extension
    imported_object = bpy.ops.import_scene.obj(filepath=(full_path))
    obj = bpy.data.objects[file_name]
    obj.hide_viewport = 1
    return obj

def load_objs(dir_path):
    obj_files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)) and os.path.splitext(f)[1] == '.obj']
    obj_files.sort()
    seq_objs = []
    for i in range(0, len(obj_files)): 
        seq_objs.append(import_file(dir_path, os.path.splitext(obj_files[i])[0]))
    return seq_objs

def get_base_obj_name(dir_path):
    obj_files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)) and os.path.splitext(f)[1] == '.obj']
    obj_files.sort()
    return os.path.splitext(obj_files[0])[0]

def get_vertices(obj):
    mesh = obj.data
    return mesh.vertices

def set_shape_key(obj, shape_key_source, name, add_vertices = True, interpolation = 'KEY_LINEAR'):
    sk = obj.shape_key_add(name = name)
    sk.interpolation = interpolation

    if add_vertices :
        verts = get_vertices(shape_key_source)
        for i in range(len(verts)):
            sk.data[i].co = verts[i].co

def add_shape_key_animation(base_mesh, name, index):
    sk = base_mesh.shape_keys.key_blocks[name]
    prev_frame = index-1
    cur_frame = index
    next_frame = index+1
    sk.value = 0
    sk.keyframe_insert("value",frame = prev_frame)
    sk.value = 1
    sk.keyframe_insert("value",frame = cur_frame)
    sk.value = 0
    sk.keyframe_insert("value",frame = next_frame)

def add_action(base, length):
    name = 'action'
    start_frame = 1
    end_frame = length # +1 maybe?

    scene = bpy.context.scene
    scene.frame_end = end_frame

    scene.frame_set(start_frame)
    base.keyframe_insert(data_path="location", index=-1)

    scene.frame_set(end_frame)
    base.keyframe_insert(data_path="location", index=-1)

    action = base.animation_data.action
    newtrack = base.animation_data.nla_tracks.new()
    newtrack.name = name

    strip = newtrack.strips.new(name=action.name, start=start_frame, action=action)
    strip.name = action.name
    strip.action_frame_start = start_frame
    strip.frame_end = end_frame
    base.animation_data.action = None
    
def export(obj, output_path):
    obj.select_set(True)
    bpy.ops.export_scene.fbx(filepath=output_path, use_selection = True)

def convert_obj_seq_to_fbx(dir_path, output_path, output_file_name):
    #    1. Load All OBJ files.
    seq_objs = load_objs(dir_path)
    base = seq_objs[0]
    
    #    2. Add Default Shape Key
    set_shape_key(obj = base, shape_key_source = base, name = 'Basis', add_vertices = False)
    base.data.shape_keys.use_relative = False
    #    3. Add Other Shake Keys
    for i in range(1, len(seq_objs)):
        set_shape_key(obj = base, shape_key_source = seq_objs[i], name = 'Deform' + str(i))

    base_mesh = bpy.data.meshes[get_base_obj_name(dir_path)]
    base.data.shape_keys.use_relative = True

    #    4. Set shape key weights
    add_shape_key_animation(base_mesh = base_mesh, name = 'Basis', index = 1)
    for i in range(1, len(seq_objs)):
        add_shape_key_animation(base_mesh = base_mesh, name = 'Deform' + str(i), index = i+1)

    #    5. Add Action
    add_action(base, len(seq_objs))
    
    for o in bpy.data.objects:
        o.select_set(False)

    base.hide_viewport = 0
    base.select_set(True)
    
    export(base, output_path + '/' + output_file_name + '.fbx')
    