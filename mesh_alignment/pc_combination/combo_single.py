def read_xyz_file(filename):
    points = []
    with open(filename, 'r') as file:
        for line in file:
            if line.strip():  # Check if line is not empty
                data = line.strip().split()
                point = [float(data[0]), float(data[1]), float(data[2])]
                points.append(point)
    return points

def write_xyz_file(points, output_filename):
    with open(output_filename, 'w') as file:
        for point in points:
            file.write(f"{point[0]} {point[1]} {point[2]}\n")

def combine_xyz_files(file1, file2, output_filename):
    points1 = read_xyz_file(file1)
    points2 = read_xyz_file(file2)
    combined_points = points1 + points2
    write_xyz_file(combined_points, output_filename)
    print(f"Combined {len(points1)} points from {file1} and {len(points2)} points from {file2} into {output_filename}")

if __name__ == "__main__":
    file1 = "001.txt"
    file2 = "002.txt"
    output_filename = "003.xyz"
    combine_xyz_files(file1, file2, output_filename)
