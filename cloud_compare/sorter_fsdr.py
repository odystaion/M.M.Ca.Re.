import os
import shutil
import datetime

# Function to get mean distance and std deviation metrics
def get_info(src_filename, dest_filename):
    with open(src_filename, 'r') as file:
        lines = file.readlines()
        if len(lines) >= 9:
            line = lines[-9].strip()  # 9th line from the bottom
            file_name = os.path.splitext(os.path.basename(src_filename))[0]  # Extract file name without extension
            line_parts = line.split()
            modified_line = ' '.join(line_parts[2:])  # Join the parts starting from the third word
            with open(dest_filename, 'a') as dest_file:
                dest_file.write(f"{file_name} {modified_line}\n")

# Function to move files containing "_C2C_" in their names to a "point clouds" folder
def move_to_point_clouds_folder():
    current_directory = os.getcwd()
    test_folder = os.path.join(current_directory, "source")
    point_clouds_folder = os.path.join(current_directory, "point clouds FSDR")

    if not os.path.exists(point_clouds_folder):
        os.makedirs(point_clouds_folder)

    files_to_move = [f for f in os.listdir(test_folder) if "_C2C_" in f]

    for file in files_to_move:
        src = os.path.join(test_folder, file)
        dest = os.path.join(point_clouds_folder, file)
        shutil.move(src, dest)
        print(f"Moved {file} to 'point clouds' folder.")

# Function to move files containing "_C2C_" in their names to a "point clouds" folder
def move_to_other_meshes_folder_i():
    current_directory = os.getcwd()
    test_folder = os.path.join(current_directory, "source")
    point_clouds_folder = os.path.join(current_directory, "other meshes FSDR")

    if not os.path.exists(point_clouds_folder):
        os.makedirs(point_clouds_folder)

    files_to_move = [f for f in os.listdir(test_folder) if "_REGIST" in f]

    for file in files_to_move:
        src = os.path.join(test_folder, file)
        dest = os.path.join(point_clouds_folder, file)
        shutil.move(src, dest)
        print(f"Moved {file} to 'other meshes' folder.")

def move_to_other_meshes_folder_ii():
    current_directory = os.getcwd()
    test_folder = os.path.join(current_directory, "target")
    point_clouds_folder = os.path.join(current_directory, "other meshes FSDR")

    if not os.path.exists(point_clouds_folder):
        os.makedirs(point_clouds_folder)

    files_to_move = [f for f in os.listdir(test_folder) if "_SAMPLED" in f]

    for file in files_to_move:
        src = os.path.join(test_folder, file)
        dest = os.path.join(point_clouds_folder, file)
        shutil.move(src, dest)
        print(f"Moved {file} to 'other meshes' folder.")

def move_to_log_folder():
    current_directory = os.getcwd()
    point_clouds_folder = os.path.join(current_directory, "LOGfiles")

    if not os.path.exists(point_clouds_folder):
        os.makedirs(point_clouds_folder)

    files_to_move = [f for f in os.listdir(current_directory) if "LOG_" in f]

    for file in files_to_move:
        src = os.path.join(current_directory, file)
        dest = os.path.join(point_clouds_folder, file)
        shutil.move(src, dest)
        print(f"Moved {file} to 'LOG' folder.")

def main():
    # Get the current date
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    # Get the current directory
    current_directory = os.getcwd()

    # List all files in the directory
    files = os.listdir(current_directory)

    # Create a new directory "results"
    results_folder = os.path.join(current_directory, f"results FSDR {current_date}")
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)
        

    # Create a new file to store the copied data inside "results" directory
    output_file = os.path.join(results_folder, "output FSDR.txt")
    with open(output_file, 'w') as _:
        pass  # Create the file or clear existing content

    # Iterate over the files in the directory and extract information
    for file in files:
        if file.startswith("LOG_2_") and file.endswith(".txt"):
            src_file_path = os.path.join(current_directory, file)
            get_info(src_file_path, output_file)
    
    # Call function to move files containing "_C2C_" in their names to "point clouds" folder
    move_to_point_clouds_folder()

    # Move files containing "_REGIST" in their names to "other_meshes" directory
    move_to_other_meshes_folder_i()

    # Move files containing "_SAMPLED_" in their names to "other_meshes" directory
    move_to_other_meshes_folder_ii()

    # Move files containing "LOG_" in their names to "LOG" directory
    move_to_log_folder()

    # Move the "point clouds" folder into the "results" directory
    shutil.move(os.path.join(current_directory, "point clouds FSDR"), os.path.join(results_folder, "point clouds FSDR"))
    shutil.move(os.path.join(current_directory, "other meshes FSDR"), os.path.join(results_folder, "other meshes FSDR"))
    shutil.move(os.path.join(current_directory, "LOGfiles"), os.path.join(results_folder, "LOGfiles"))

if __name__ == "__main__":
    main()


