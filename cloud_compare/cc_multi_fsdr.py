import os
import subprocess
import argparse

# Define the paths to the directories
test01_dir = r"C:\Users\odyst_zong4m\Desktop\CloudCompare Automation\CCC\source"
test02_dir = r"C:\Users\odyst_zong4m\Desktop\CloudCompare Automation\CCC\target"

# Parse command-line arguments
parser = argparse.ArgumentParser(description='CloudCompare Automation Script')
parser.add_argument('--MODE', choices=['LS', 'TRI', 'HF'], default='LS', help='Mode for model')
args = parser.parse_args()

# Get the list of files in each directory
test01_files = os.listdir(test01_dir)
test02_files = os.listdir(test02_dir)

target_number = 0

# Get the first file in the target directory
if test02_files:
    target_file = os.path.join(test02_dir, test02_files[target_number])
else:
    raise FileNotFoundError("Target directory is empty.")

# Iterate over corresponding files in both directories
for file1 in test01_files:
    file1_path = os.path.join(test01_dir, file1)
    
    # Construct log filenames
    filename1 = file1.split('.')[0]
    log1_filename = f"LOG_1_{filename1}.txt"
    log2_filename = f"LOG_2_{filename1}.txt"

    # Define the command with flags
    command = [
        r"C:\Program Files\CloudCompare\CloudCompare.exe",
        "-SILENT",
        "-C_EXPORT_FMT", "PLY",
        "-M_EXPORT_FMT", "PLY",
        "-O", file1_path,
        "-O", target_file,  # Use the {target_number} file in the target directory
        "-LOG_FILE", log1_filename,
        "-ICP",
        # "-REFERENCE_IS_FIRST",
        "-MIN_ERROR_DIFF", "0.00001",
        # "-ADJUST_SCALE",
        "-SAMPLE_MESH", "POINTS", "10000",
        "-C2C_DIST",
        "-MODEL", args.MODE, "KNN", "6",
        "-LOG_FILE", log2_filename,
        "-CLEAR"
    ]

    # Execute the command
    subprocess.run(command)

#i.e. python script.py --MODE TRI
