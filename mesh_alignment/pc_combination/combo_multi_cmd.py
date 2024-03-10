import os
import shutil

def combine_xyz_directories(directory1, directory2, output_directory):
    os.makedirs(output_directory, exist_ok=True)

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

def read_xyz_file(file_path):
    points = []
    with open(file_path, 'r') as file:
        for line in file:
            values = line.split()
            point = [float(value) for value in values]
            points.append(point)
    return points

def write_xyz_file(points, output_filename):
    with open(output_filename, 'w') as file:
        for point in points:
            file.write(f"{point[0]} {point[1]} {point[2]}\n")

if __name__ == "__main__":
    # Expecting three command-line arguments: directory1, directory2, and output_directory
    import sys
    if len(sys.argv) != 4:
        print("Usage: python script.py <directory1> <directory2> <output_directory>")
        sys.exit(1)

    directory1 = sys.argv[1]
    directory2 = sys.argv[2]
    output_directory = sys.argv[3]

    combine_xyz_directories(directory1, directory2, output_directory)

    print("Script completed.")

    #IN: example1.txt example2.txt
    #OUT: example1_example2.xyz
