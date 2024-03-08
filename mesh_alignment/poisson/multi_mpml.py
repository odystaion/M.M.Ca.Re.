import os
import pymeshlab as ml

# Function to process a single XYZ file
def process_xyz_file(input_path, output_path):
    # Initialize MeshLab server
    ms = ml.MeshSet()
    
    # Load point cloud
    ms.load_new_mesh(input_path)

    # Compute normals for point sets
    ms.apply_filter("compute_normal_for_point_clouds")

    # Surface reconstruction: Ball Pivoting
    ms.apply_filter("generate_surface_reconstruction_ball_pivoting")

    # Export the result as OBJ
    ms.save_current_mesh(output_path)
    print("Surface reconstruction complete. Output saved to:", output_path)

# Directory containing XYZ files
input_directory = "input_dir"
output_directory = "output_dir"

# Create output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Iterate over files in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith(".xyz"):
        input_path = os.path.join(input_directory, filename)
        output_path = os.path.join(output_directory, os.path.splitext(filename)[0] + ".obj")
        
        # Process the XYZ file
        process_xyz_file(input_path, output_path)

