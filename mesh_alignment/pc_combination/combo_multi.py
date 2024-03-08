import os

def combine_xyz_directories(directory1, directory2, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    files1 = sorted(os.listdir(directory1))
    files2 = sorted(os.listdir(directory2))
    
    for file1, file2 in zip(files1, files2):
        file1_path = os.path.join(directory1, file1)
        file2_path = os.path.join(directory2, file2)
        
        output_filename = os.path.join(output_directory, f"{os.path.splitext(file1)[0]}_{os.path.splitext(file2)[0]}.xyz")
        
        combine_xyz_files(file1_path, file2_path, output_filename)

def combine_xyz_files(file1, file2, output_filename):
    points1 = read_xyz_file(file1)
    points2 = read_xyz_file(file2)
    combined_points = points1 + points2
    write_xyz_file(combined_points, output_filename)
    print(f"Combined {len(points1)} points from {file1} and {len(points2)} points from {file2} into {output_filename}")

if __name__ == "__main__":
    directory1 = "dir_1"
    directory2 = "dir_2"
    output_directory = "combo_results"
    combine_xyz_directories(directory1, directory2, output_directory)
