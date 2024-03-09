import os
import pywavefront

def read_obj_file(file_path):
    vertices = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('v '):
                values = line.split()[1:]
                vertex = [float(value) for value in values]
                vertices.append(vertex)
    return vertices

def export_xyz_file(output_folder, file_name, point_cloud):
    output_path = os.path.join(output_folder, f"{file_name}.txt")
    with open(output_path, 'w') as file:
        for vertex in point_cloud:
            file.write(f"{vertex[0]} {vertex[1]} {vertex[2]}\n")

if __name__ == '__main__':
    # Get the script's directory
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Specify the input folder (in_dir) path
    folder_path = os.path.join(script_directory, "obj_input")

    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        print("Invalid folder path. Exiting...")
        exit()

    output_folder = os.path.join(script_directory, "txt_output")
    os.makedirs(output_folder, exist_ok=True)

    # Iterate over OBJ files in the selected folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".obj"):
            file_path = os.path.join(folder_path, file_name)
            point_cloud = read_obj_file(file_path)
            export_xyz_file(output_folder, os.path.splitext(file_name)[0], point_cloud)

    print("Point clouds exported to TXT files in the output folder.")
