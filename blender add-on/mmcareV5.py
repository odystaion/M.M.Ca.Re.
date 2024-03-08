bl_info = {
    "name": "M.M.Ca.Re.:Module for Multi-CAmera Reconstruction",
    "author": "I. O. Stavrakakis",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > MMCaRe",
    "description": "Module for gait analysis. Import your .obj results from running ECON. Using the Boolean Modifier for Intersection gain a footprint for every frame. Combine and Sort your results into an animated sequence. ",
    "warning": "Beta Version",
    "doc_url": "",
    "category": "Add Mesh",
}


import bpy
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty
import os
import zipfile


#-----------------------------------------------------------------------------------------------------

# Global variable to keep track of import order
import_order = 1



# Function to create or get a collection
def create_new_collection(collection_name):
    # Check if the collection already exists
    existing_collection = bpy.data.collections.get(collection_name)
    if existing_collection:
        return existing_collection

    # Create a new collection and link it
    new_collection = bpy.data.collections.new(collection_name)
    bpy.context.scene.collection.children.link(new_collection)
    return new_collection



# PANEL 1 - Select Type of File for Human Mesh Importation
class OBJImportPanel(bpy.types.Panel):
    bl_label = "Import Data"
    bl_idname = "OBJECT_PT_obj_import"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "mmcare"
    bl_order = 1

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        row = layout.row()
        row.prop(context.scene, "collection_name", text="Collection Name")

        layout.operator("object.import_obj_operator")   # OBJ OPERATOR
        layout.operator("object.import_zip_operator")   # ZIP OPERATOR
        
        row = layout.row()
        layout.label(text=f"Current Import Order: {import_order}")

        # Add a button to reset import_order
        layout.operator("object.reset_import_order_operator", text="Reset Import Order")

        
        


# PANEL 1 OPERATOR 1 - Import OBJ
class OBJECT_OT_ImportOBJOperator(bpy.types.Operator, ImportHelper):
    bl_label = "Import OBJ"
    bl_idname = "object.import_obj_operator"
    filename_ext = ".obj"

    def execute(self, context):
        global import_order
        filepath = self.filepath
        bpy.ops.import_scene.obj(filepath=filepath)

        # Get the last imported object (the one just imported)
        last_imported_obj = context.selected_objects[-1]
        
        # Extract the original filename without the extension
        original_filename = os.path.splitext(os.path.basename(filepath))[0]
        
        # Rename the object using the original filename
        last_imported_obj.name = original_filename
        
        # Assign the import order to the object using a custom property
        last_imported_obj["import_order"] = import_order
        import_order += 1
        
        # Create the collection if it doesn't exist and link the object to it
        collection_name = context.scene.collection_name
        new_collection = create_new_collection(collection_name)
        new_collection.objects.link(last_imported_obj)
       
        return {'FINISHED'}


# PANEL 1 OPERATOR 2 - Import ZIP
class OBJECT_OT_ImportZipOperator(bpy.types.Operator, ImportHelper):
    bl_label = "Import ZIP"
    bl_idname = "object.import_zip_operator"
    filename_ext = ".zip"

    def execute(self, context):
        global import_order
        filepath = self.filepath
        zip_ref = zipfile.ZipFile(filepath, 'r')
        obj_files = [name for name in zip_ref.namelist() if name.lower().endswith('.obj')]

        if not obj_files:
            self.report({'ERROR'}, "No .obj files found in the ZIP archive.")
            zip_ref.close()
            return {'CANCELLED'}

        for obj_file in obj_files:
            with zip_ref.open(obj_file, 'r') as obj_data:
                temp_path = bpy.path.abspath("//temp_obj.obj")
                with open(temp_path, 'wb') as temp_file:
                    temp_file.write(obj_data.read())
                bpy.ops.import_scene.obj(filepath=temp_path)

                last_imported_obj = context.selected_objects[-1]
                original_filename = os.path.splitext(os.path.basename(obj_file))[0]
                last_imported_obj.name = original_filename
                
                last_imported_obj["import_order"] = import_order
                import_order += 1
                
                collection_name = context.scene.collection_name
                new_collection = create_new_collection(collection_name)
                new_collection.objects.link(last_imported_obj)
                
                # Unlink the object from the default collection
                bpy.context.scene.collection.objects.unlink(last_imported_obj)
                
        zip_ref.close()
        return {'FINISHED'}


#Panel 1 Operator 3 - Import order 1
class OBJECT_OT_ResetImportOrderOperator(bpy.types.Operator):
    bl_label = "Reset Import Order"
    bl_idname = "object.reset_import_order_operator"

    def execute(self, context):
        global import_order
        import_order = 1
        self.report({'INFO'}, "Import Order reset to 1.")
        return {'FINISHED'}




#-----------------------------------------------------------------------------------------------------



# Function to create or get a collection
def create_new_collection(collection_name):
    # Check if the collection already exists
    existing_collection = bpy.data.collections.get(collection_name)
    if existing_collection:
        return existing_collection

    # Create a new collection and link it
    new_collection = bpy.data.collections.new(collection_name)
    bpy.context.scene.collection.children.link(new_collection)
    return new_collection

# PANEL 2 - Floor Creation 
class OBJECT_PT_AddPlanePanel(bpy.types.Panel):
    bl_label = "Ground Plane"
    bl_idname = "OBJECT_PT_add_plane"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'mmcare'
    bl_order = 2
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()

        # Input boxes for XYZ location, length, and width
        layout.prop(context.scene, "plane_location_x")
        layout.prop(context.scene, "plane_location_y")
        layout.prop(context.scene, "plane_location_z")
        layout.prop(context.scene, "plane_length")
        layout.prop(context.scene, "plane_width")
        
        # Primitive Plane Generation
        layout.operator("object.add_plane_operator", text="Add Plane")


# PANEL 2 OPERATOR - Plane Tile Generation 
class OBJECT_OT_AddPlaneOperator(bpy.types.Operator):
    bl_label = "Add Plane"
    bl_idname = "object.add_plane_operator"
    
    def execute(self, context):
        bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(context.scene.plane_location_x, context.scene.plane_location_y, context.scene.plane_location_z))
        last_imported_obj = bpy.context.active_object  # Assuming the last created object is the active one

        last_imported_obj.scale.x = context.scene.plane_length
        last_imported_obj.scale.y = context.scene.plane_width
        
        collection_name = "Plane Tiles"  # Adjust the collection name as needed
        new_collection = create_new_collection(collection_name)
        new_collection.objects.link(last_imported_obj)
        
        # Unlink the object from the default collection
        bpy.context.scene.collection.objects.unlink(last_imported_obj)

        return {'FINISHED'}



#-----------------------------------------------------------------------------------------------------

#Panel 3 Operator - Duplicate one of your existing Collections
class CollectionDuplicateOperator(bpy.types.Operator):
    bl_idname = "object.collection_duplicate"
    bl_label = "Duplicate Collection"
    
    def execute(self, context):
        collection_name = context.scene.collection_name

        if collection_name:
            # Get the collection
            original_collection = bpy.data.collections.get(collection_name)

            if original_collection:
                # Create a new collection
                new_collection = bpy.data.collections.new(collection_name + "_duplicate")
                bpy.context.scene.collection.children.link(new_collection)

                for obj in original_collection.objects:
                    # Make a copy of the original object's name
                    original_name = obj.name

                    # Duplicate the object
                    new_obj = obj.copy()
                    new_obj.data = obj.data.copy()
                    new_collection.objects.link(new_obj)

                    # Rename duplicated object
                    new_obj.name = f"{original_name}_duplicate"

                    # Adjust location for the duplicated object
                    new_obj.location.x += 0
                    new_obj.location.y += 0
                    new_obj.location.z += 0

                    # Set visibility keyframes
                    for frame in range(bpy.context.scene.frame_start, bpy.context.scene.frame_end + 1):
                        bpy.context.scene.frame_set(frame)
                        new_obj.hide_viewport = obj.hide_viewport
                        new_obj.keyframe_insert(data_path="hide_viewport", frame=frame)

            else:
                print("Original collection not found.")
        else:
            print("Collection name not provided.")

        return {'FINISHED'}


#Panel 3 - Collection Duplicator
class CollectionDuplicatePanel(bpy.types.Panel):
    bl_label = "Duplicate Collection"
    bl_idname = "PT_CollectionDuplicatePanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'mmcare'
    bl_order = 3

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop_search(context.scene, "collection_name", bpy.data, "collections")
        layout.operator("object.collection_duplicate")


#-----------------------------------------------------------------------------------------------------

#PANEL 4 Operator - Boolean Modifier
class OBJECT_OT_ApplyBoolean(bpy.types.Operator):
    bl_idname = "object.apply_boolean"
    bl_label = "Apply Boolean Modifier"
    
    def execute(self, context):
        # Get the selected collection and plane
        collection = context.scene.my_collection
        plane = context.scene.my_plane
        
        if collection and plane:
            # Iterate through objects in the collection
            for obj in collection.objects:
                # Create a new boolean modifier
                bool_mod = obj.modifiers.new(name="Boolean", type='BOOLEAN')
                bool_mod.operation = 'INTERSECT'
                
                # Set the object to be intersected
                bool_mod.use_self = True
                bool_mod.object = plane
                
                # Apply the modifier
                bpy.ops.object.modifier_apply({"object": obj}, modifier=bool_mod.name)
                
                self.report({'INFO'}, f"Boolean modifier applied to {obj.name} with operation set to INTERSECT.")
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "One or both of the collection or the plane not found.")
            return {'CANCELLED'}


#PANEL 4 - Boolean Modifier
class OBJECT_PT_BooleanPanel(bpy.types.Panel):
    bl_label = "Boolean Operator"
    bl_idname = "OBJECT_PT_boolean_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'mmcare'
    bl_order = 4

    def draw(self, context):
        layout = self.layout
        
        col = layout.column(align=True)
        col.prop(context.scene, "my_collection", text="Collection")
        col.prop(context.scene, "my_plane", text="Plane")

        row = layout.row()
        row.operator("object.apply_boolean", text="Apply Boolean")


#-----------------------------------------------------------------------------------------------------



#PANEL 5 - Select a Collection and Sort its Contents
class OBJECT_PT_SortMeshesPanel(bpy.types.Panel):
    bl_label = "Sort Meshes"
    bl_idname = "PT_SortMeshesPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'mmcare'
    bl_order = 5

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        layout.operator("object.transform_mesh_operator", icon="FILE_TEXT")

        row = layout.row()
        layout.prop_search(context.scene, "selected_sort_collection", bpy.data, "collections", text="Select Collection")

        # Add an input field for setting the starting frame
        row = layout.row()
        row.prop(context.scene, "starting_frame", text="Starting Frame")

        layout.operator("object.sort_meshes_operator")

        # Show the first and last frames with meshes
        first_last_frames = self.get_first_last_frames(context)
        if first_last_frames:
            row = layout.row()
            row.label(text=f"First Frame with Mesh: {first_last_frames[0]}")

            row = layout.row()
            row.label(text=f"Last Frame with Mesh: {first_last_frames[1]}")

    def get_first_last_frames(self, context):
        selected_collection = context.scene.selected_sort_collection

        if selected_collection:
            frames_with_mesh = []

            for obj in selected_collection.objects:
                if "import_order" in obj:
                    frame_number = obj["import_order"] + context.scene.starting_frame - 1
                    if frame_number not in frames_with_mesh:
                        frames_with_mesh.append(frame_number)

            if frames_with_mesh:
                return [min(frames_with_mesh), max(frames_with_mesh)]

        return None





# PANEL 5 OPERATOR 1 - Mesh Spatial Transformation based on example file below
class OBJECT_OT_TransformMeshOperator(bpy.types.Operator, ImportHelper):
    bl_label = "Transform Mesh"
    bl_idname = "object.transform_mesh_operator"
    filename_ext = ".txt"

    def execute(self, context):
        filepath = self.filepath
        with open(filepath, 'r') as file:
            transformation_data = file.readlines()

        for line in transformation_data:
            values = line.strip().split(',')
            if len(values) == 10:
                try:
                    obj_name, loc_x, loc_y, loc_z, rot_x, rot_y, rot_z, scale_x, scale_y, scale_z = values
                    obj = bpy.data.objects.get(obj_name)
                    if obj:
                        obj.location = (float(loc_x), float(loc_y), float(loc_z))
                        obj.rotation_euler = (float(rot_x), float(rot_y), float(rot_z))
                        obj.scale = (float(scale_x), float(scale_y), float(scale_z))
                except ValueError:
                    self.report({'ERROR'}, f"Invalid data format in line: {line}")
            else:
                self.report({'ERROR'}, f"Invalid data format in line: {line}")

        return {'FINISHED'}


#--------------------------------------------------------------------------------------------------

    #Input file format:
#object_name,loc_x,loc_y,loc_z,rot_x,rot_y,rot_z,scale_x,scale_y,scale_z

    #Examples:
#Cube,2.0,1.0,0.5,0.0,0.0,1.57,2.0,2.0,2.0
#Sphere,-1.0,0.0,0.0,0.0,1.57,0.0,1.5,1.5,1.5


#----------------------------------------------------------------------------------------------------




# PANEL 5 OPERATOR 2 - Sort Meshes in a Collection
class OBJECT_OT_SortMeshesOperator(bpy.types.Operator):
    bl_label = "Sort Meshes"
    bl_idname = "object.sort_meshes_operator"

    def execute(self, context):
        selected_collection = context.scene.selected_sort_collection

        if selected_collection:
            frames_to_hide = set(range(context.scene.starting_frame, bpy.context.scene.frame_end + 1))
            frames_to_show = set()

            original_z_locations = {}

            for obj in selected_collection.objects:
                if "import_order" in obj:
                    frame_number = obj["import_order"] + context.scene.starting_frame - 1
                    frames_to_show.add(frame_number)

                    if frame_number not in original_z_locations:
                        original_z_locations[frame_number] = obj.location.z

            for frame in frames_to_hide:
                for obj in selected_collection.objects:
                    obj.hide_viewport = True
                    obj.keyframe_insert(data_path="hide_viewport", frame=frame)

            for frame in frames_to_show:
                for obj in selected_collection.objects:
                    original_z = original_z_locations.get(frame, 0.0)

                    if frame == obj.get("import_order", 0) + context.scene.starting_frame - 1:
                        obj.location.z = original_z
                    else:
                        obj.location.z = original_z + 10.0

                    obj.keyframe_insert(data_path="location", frame=frame)

                    obj.hide_viewport = frame != obj.get("import_order", 0) + context.scene.starting_frame - 1
                    obj.keyframe_insert(data_path="hide_viewport", frame=frame)

            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "No collection selected for sorting.")
            return {'CANCELLED'}





#-----------------------------------------------------------------------------------------------------

# PANEL 6 - Apply Red Material to Collection
class OBJECT_PT_ApplyRedMaterialPanel(bpy.types.Panel):
    bl_label = "Apply Colour"
    bl_idname = "OBJECT_PT_apply_red_material_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'mmcare'
    bl_order = 6

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        layout.prop_search(context.scene, "selected_material_collection", bpy.data, "collections", text="Select Collection")

        layout.operator("object.apply_red_material_operator", text="Apply")


# OPERATOR - Apply Red Material to Collection
class OBJECT_OT_ApplyRedMaterialOperator(bpy.types.Operator):
    bl_label = "Apply Red Material"
    bl_idname = "object.apply_red_material_operator"

    def execute(self, context):
        selected_collection = context.scene.selected_material_collection

        if selected_collection:
            red_material = bpy.data.materials.new(name="Red Material")
            red_material.diffuse_color = (1.0, 0.0, 0.0, 1.0)  # Set the color to red (RGB values)

            for obj in selected_collection.objects:
                if obj.type == 'MESH':
                    obj.data.materials.clear()  # Clear any existing materials
                    obj.data.materials.append(red_material)  # Assign the red material

            self.report({'INFO'}, f"Red material applied to objects in collection: {selected_collection.name}")
        else:
            self.report({'ERROR'}, "No collection selected for applying the red material.")
            return {'CANCELLED'}

        return {'FINISHED'}






#----------------------------------------------------------------------------------------------------



def register():

#1-----------------------------------------------------------------------------------------------------
    bpy.types.Scene.collection_name = StringProperty(
        name="Collection Name",
        default="Imported Human Objects"
    )
    bpy.utils.register_class(OBJImportPanel)
    bpy.utils.register_class(OBJECT_OT_ImportOBJOperator)
    bpy.utils.register_class(OBJECT_OT_ImportZipOperator)
    bpy.utils.register_class(OBJECT_OT_ResetImportOrderOperator)




#2-----------------------------------------------------------------------------------------------------

    bpy.types.Scene.plane_length = bpy.props.FloatProperty(name="Length", default=1.0)
    bpy.types.Scene.plane_width = bpy.props.FloatProperty(name="Width", default=1.0)
    bpy.types.Scene.plane_location_x = bpy.props.FloatProperty(name="X", default=0.0)
    bpy.types.Scene.plane_location_y = bpy.props.FloatProperty(name="Y", default=0.0)
    bpy.types.Scene.plane_location_z = bpy.props.FloatProperty(name="Z", default=0.0)
    bpy.types.Scene.square_side_length = bpy.props.FloatProperty(name="Side Length", default=0.1)

    bpy.utils.register_class(OBJECT_PT_AddPlanePanel)
    bpy.utils.register_class(OBJECT_OT_AddPlaneOperator)


#3-----------------------------------------------------------------------------------------------------

    bpy.utils.register_class(CollectionDuplicateOperator)
    bpy.utils.register_class(CollectionDuplicatePanel)
    bpy.types.Scene.collection_name = bpy.props.StringProperty(name="Collection Name")


#4-----------------------------------------------------------------------------------------------------


    bpy.utils.register_class(OBJECT_OT_ApplyBoolean)
    bpy.utils.register_class(OBJECT_PT_BooleanPanel)
    bpy.types.Scene.my_collection = bpy.props.PointerProperty(type=bpy.types.Collection)
    bpy.types.Scene.my_plane = bpy.props.PointerProperty(type=bpy.types.Object)

#5-----------------------------------------------------------------------------------------------------
    bpy.types.Scene.selected_sort_collection = bpy.props.PointerProperty(
        type=bpy.types.Collection,
        name="Selected Collection for Sorting",
    )
    bpy.utils.register_class(OBJECT_PT_SortMeshesPanel)
    bpy.utils.register_class(OBJECT_OT_TransformMeshOperator)
    bpy.utils.register_class(OBJECT_OT_SortMeshesOperator)
    bpy.types.Scene.starting_frame = bpy.props.IntProperty(
        name="Starting Frame",
        default=1,
        min=1,
        description="The starting frame for object animations."
    )



#------------------------------------------------------------------------------------------------------

bpy.types.Scene.selected_material_collection = bpy.props.PointerProperty(
    type=bpy.types.Collection,
    name="Selected Collection for Material",
)

bpy.utils.register_class(OBJECT_PT_ApplyRedMaterialPanel)
bpy.utils.register_class(OBJECT_OT_ApplyRedMaterialOperator)



#------------------------------------------------------------------------------------------------------


def unregister():

#1-----------------------------------------------------------------------------------------------------


    bpy.utils.unregister_class(OBJImportPanel)
    bpy.utils.unregister_class(OBJECT_OT_ImportOBJOperator)
    bpy.utils.unregister_class(OBJECT_OT_ImportZipOperator)
    bpy.utils.unregister_class(OBJECT_OT_ResetImportOrderOperator)
    del bpy.types.Scene.collection_name



#2-----------------------------------------------------------------------------------------------------

    bpy.utils.unregister_class(OBJECT_PT_AddPlanePanel) 
    bpy.utils.unregister_class(OBJECT_OT_AddPlaneOperator)   

    del bpy.types.Scene.plane_length
    del bpy.types.Scene.plane_width
    del bpy.types.Scene.plane_location_x
    del bpy.types.Scene.plane_location_y
    del bpy.types.Scene.plane_location_z
    del bpy.types.Scene.square_side_length

#3-----------------------------------------------------------------------------------------------------

    bpy.utils.unregister_class(CollectionDuplicateOperator)
    bpy.utils.unregister_class(CollectionDuplicatePanel)
    del bpy.types.Scene.collection_name

#4-----------------------------------------------------------------------------------------------------

    bpy.utils.unregister_class(OBJECT_OT_ApplyBoolean)
    bpy.utils.unregister_class(OBJECT_PT_BooleanPanel)
    del bpy.types.Scene.my_collection
    del bpy.types.Scene.my_plane

#5-----------------------------------------------------------------------------------------------------

    del bpy.types.Scene.selected_sort_collection
    bpy.utils.unregister_class(OBJECT_PT_SortMeshesPanel)
    bpy.utils.unregister_class(OBJECT_OT_TransformMeshOperator)
    bpy.utils.unregister_class(OBJECT_OT_SortMeshesOperator)
    del bpy.types.Scene.starting_frame

#------------------------------------------------------------------------------------------------------

    del bpy.types.Scene.selected_material_collection
    bpy.utils.unregister_class(OBJECT_PT_ApplyRedMaterialPanel)
    bpy.utils.unregister_class(OBJECT_OT_ApplyRedMaterialOperator)


#------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    register()