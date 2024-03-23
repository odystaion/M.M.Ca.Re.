import subprocess
import os

def execute_scripts():
    # Get the current directory
    current_directory = os.getcwd()

    # Execute cc_multi_f.py
    cc_multi_script = os.path.join(current_directory, "cc_multi_fsdr.py")
    subprocess.run(["python", cc_multi_script, "--MODE", "HF"])

    # Execute sorter_f.py
    sorter_script = os.path.join(current_directory, "sorter_fsdr.py")
    subprocess.run(["python", sorter_script])

    # Execute plotter_auto.py with flags
    plotter_script = os.path.join(current_directory, "plotter_fsdr.py")
    subprocess.run(["python", plotter_script, "--increment", "30", "--degree", "5"])

if __name__ == "__main__":
    execute_scripts()
