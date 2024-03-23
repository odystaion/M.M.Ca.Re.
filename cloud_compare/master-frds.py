import subprocess
import os

def execute_scripts():
    # Get the current directory
    current_directory = os.getcwd()

    # Execute cc_multi_f.py
    cc_multi_script = os.path.join(current_directory, "cc_multi_frds.py")
    subprocess.run(["python", cc_multi_script, "--MODE", "5"])

    # Execute sorter_f.py
    sorter_script = os.path.join(current_directory, "sorter_frds.py")
    subprocess.run(["python", sorter_script])

    # Execute plotter_auto.py with flags
    plotter_script = os.path.join(current_directory, "plotter_frds.py")
    subprocess.run(["python", plotter_script, "--increment", "1", "--degree", "5"])

if __name__ == "__main__":
    execute_scripts()
