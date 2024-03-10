import os
import pywavefront
import shutil
import random

def read_obj_file(file_path, sc=1000):
    vertices = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('v '):
                values = line.split()[1:]
                vertex = [float(value) for value in values]
                vertices.append(vertex)

    total_points = len(vertices)

    # Subsample if requested
    if sc < total_points:
        vertices = random.sample(vertices, sc)

    return vertices, total_points

def export_xyz_file(output_folder, file_name, point_cloud):
    output_path = os.path.join(output_folder, f"{file_name}_filtered.txt")
    with open(output_path, 'w') as file:
        for vertex in point_cloud:
            file.write(f"{vertex[0]} {vertex[1]} {vertex[2]}\n")

def process_files(input_folder, output_folder, sc=1000):
    # Ensure the output folder exists or create it
    os.makedirs(output_folder, exist_ok=True)

    # Iterate over OBJ files in the input folder
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".obj"):
            file_path = os.path.join(input_folder, file_name)
            point_cloud, total_points = read_obj_file(file_path, sc=sc)
            export_xyz_file(output_folder, os.path.splitext(file_name)[0], point_cloud)
            print(f"Total points in {file_name}: {total_points}")
            print(f"Number of points in the output: {len(point_cloud)}")

if __name__ == '__main__':
    # Expecting two or three command-line arguments: input folder, output folder, and optional subsample count
    import sys
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print("Usage: python script1.py <input_folder> <output_folder> [sc]")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]

    # Set the default subsample count to 1000
    sc = 5000

    # Check if a custom subsample count is provided as a command-line argument
    if len(sys.argv) == 4:
        try:
            sc = int(sys.argv[3])
        except ValueError:
            print("Invalid subsample count. Using default value (5000).")

    # Process files in the input folder and generate results in the output folder
    process_files(input_folder, output_folder, sc=sc)

    print("Script completed.")


    
    #IN: example.obj
    #OUT: example_filtered.txt 
