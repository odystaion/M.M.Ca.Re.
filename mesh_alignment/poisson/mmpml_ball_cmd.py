#MULTI - MYPYMESHLAB - BALL PIVOTING RECONSTRUCTION - COMMAND LINE - SCRIPT
# M - MPML - BALL - CMD

import os
import pymeshlab as ml
import shutil

def process_xyz_files(input_directory, output_directory):
    os.makedirs(output_directory, exist_ok=True)

    for filename in os.listdir(input_directory):
        if filename.endswith(".xyz"):
            input_path = os.path.join(input_directory, filename)
            output_path = os.path.join(output_directory, os.path.splitext(filename)[0] + ".obj")

            process_xyz_file(input_path, output_path)

def process_xyz_file(input_path, output_path):
    ms = ml.MeshSet()

    ms.load_new_mesh(input_path)
    ms.apply_filter("compute_normal_for_point_clouds")

    # FOR BALL PIVOTING RECONSTRUCTION
    ms.apply_filter("generate_surface_reconstruction_ball_pivoting")

    # FOR SCREENED POISSON RECONSTRUCTION
    # ms.apply_filter("generate_surface_reconstruction_screened_poisson")
    ms.save_current_mesh(output_path)

    print("Surface reconstruction complete. Output saved to:", output_path)

if __name__ == "__main__":
    # Expecting two command-line arguments: input directory and output directory
    import sys
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_directory> <output_directory>")
        sys.exit(1)

    input_directory = sys.argv[1]
    output_directory = sys.argv[2]

    process_xyz_files(input_directory, output_directory)

    print("Script completed.")

#IN: example.xyz
#OUT: example.obj