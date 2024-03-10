# for file-structure:
# mesh-alignment
#  -master_script_demo.py
#  -obj2txt_resamp
#       -obj2txt_resamp_cmd.py
#       -obj_input1
#       -obj_input2
#       (-txt_output1)
#       (-txt_output2)
#  -my_probreg
#       -examples
#           -multi_affine_cmd.py
#           -cpd_results
#           -cpd_target
#  -pc_combination
#       -combo_multi_cmd.py
#       -combo_results
#  -poisson
#       -mmpml_poisson_cmd.py 
#       -mmpml_ball_cmd.py 
#       -output_dir_poisson
#       -output_dir_ball


import os
import subprocess

# Function to run script in a specific directory
def run_script1(directory, script_name, input_folder, output_folder, sc):
    script_path = os.path.join(directory, script_name)
    subprocess.run(["python", script_path, input_folder, output_folder, sc])

def run_script2(directory, script_name, input_folder_1, input_folder_2, output_folder_1, output_folder_2):
    script_path = os.path.join(directory, script_name)
    subprocess.run(["python", script_path, input_folder_1, input_folder_2, output_folder_1, output_folder_2])

def run_script3(directory, script_name, input_folder_1, input_folder_2, output_folder):
    script_path = os.path.join(directory, script_name)
    subprocess.run(["python", script_path, input_folder_1, input_folder_2, output_folder])

def run_script4(directory, script_name, input_folder, output_folder):
    script_path = os.path.join(directory, script_name)
    subprocess.run(["python", script_path, input_folder, output_folder])

if __name__ == '__main__':
    # Get the main directory path
    main_directory = os.path.dirname(os.path.abspath(__file__))

    # Script 1.1
    script_directory_11 = os.path.join(main_directory, "obj2txt_resamp")
    input_folder_11 = os.path.join(script_directory_11, "obj_input1")
    output_folder_11 = os.path.join(script_directory_11, "txt_output1")
    subsampled_points = 10000
    run_script1(script_directory_11, "obj2txt_resamp_cmd.py", input_folder_11, output_folder_11, subsampled_points)

    #IN: example1.obj
    #i.e. : frame_0184_0_Front_BNI_C1.obj
    
    #OUT: example1.txt / example1.xyz
    #i.e. : frame_0184_0_Front_BNI_C1_filtered.txt

    # Script 1.2
    script_directory_12 = os.path.join(main_directory, "obj2txt_resamp")
    input_folder_12 = os.path.join(script_directory_12, "obj_input2")
    output_folder_12 = os.path.join(script_directory_12, "txt_output2")
    run_script1(script_directory_12, "obj2txt_resamp_cmd.py", input_folder_12, output_folder_12)

    #IN: example1.obj
    #i.e. : frame_0184_0_Front_BNI_C2_filtered.obj

    #OUT: example1.txt / example1.xyz
    #i.e. : frame_0184_0_Front_BNI_C2_filtered.txt

    # Script 2
    script_directory_2 = os.path.join(main_directory, "my_probreg", "examples")
    source_folder = output_folder_11  # Use the output of script 11 as source for script 2
    target_folder = output_folder_12  # Use the output of script 12 as target for script 2
    output_folder_21 = os.path.join(script_directory_2, "cpd_results")
    output_folder_22 = os.path.join(script_directory_2, "cpd_target")
    run_script2(script_directory_2, "multi_affine_cmd.py", source_folder, target_folder, output_folder_21, output_folder_22)
    
    #IN: preffix_<frame_number>_middle_<camera_number>_suffix.txt
    #i.e. : frame_0184_0_Front_BNI_C1_filtered.txt
    #i.e. : frame_0184_0_Front_BNI_C2_filtered.txt
    
    #OUT: result_<frame_number>_<camera_number>.txt
    #i.e. : result_0184_C1.txt
    #i.e. : target_0184_C2.txt
    
    # Script 3
    script_directory_3 = os.path.join(main_directory, "pc_combination")
    input_folder_31 = output_folder_21  # Use the target of script 2 as input 1 for script 3
    input_folder_32 = output_folder_22  # Use the output of script 2 as input 2 for script 3
    output_folder_3 = os.path.join(script_directory_3, "combo_results")
    run_script3(script_directory_3, "pc_combo_cmd.py", input_folder_31, input_folder_32, output_folder_3)

    #IN: example1.txt example2.txt
    #i.e. : result_0184_C1.txt target_0184_C2.txt

    #OUT: example1_example2.xyz
    #i.e. : result_0184_C1_target_0184_C2.xyz

    # Script 4.1
    script_directory_41 = os.path.join(main_directory, "poisson")
    input_folder_41 = output_folder_3  # Use the output of script 2 as input for script 3
    output_folder_41 = os.path.join(script_directory_41, "output_dir_ball")
    run_script4(script_directory_41, "mmpml_ball_cmd.py", input_folder_41, output_folder_41)

    # Script 4.2
    script_directory_42 = os.path.join(main_directory, "poisson")
    input_folder_42 = output_folder_3  # Use the output of script 2 as input for script 3
    output_folder_42 = os.path.join(script_directory_42, "output_dir_poisson")
    run_script4(script_directory_42, "mmpml_poisson_cmd.py", input_folder_42, output_folder_42)

    #IN: example.xyz
    #i.e. : result_0184_C1_target_0184_C2.xyz

    #OUT: example.obj
    #i.e. : result_0184_C1_target_0184_C2.obj
