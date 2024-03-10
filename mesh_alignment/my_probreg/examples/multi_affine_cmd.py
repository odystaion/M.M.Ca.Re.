import os
import numpy as np
import shutil
import cupy as cp
import open3d as o3
from probreg import cpd
from probreg import callbacks
import utils
import time

def process_pointcloud_files(source_directory, target_directory, output_directory_1, output_directory_2):
    os.makedirs(output_directory_1, exist_ok=True)
    os.makedirs(output_directory_2, exist_ok=True)

    source_files = sorted(os.listdir(source_directory))
    target_files = sorted(os.listdir(target_directory))

    for source_file, target_file in zip(source_files, target_files):
        source_frame_number = source_file.split('_')[1]
        source_camera_number = source_file.split('_')[-2].split('.')[0]

        target_frame_number = target_file.split('_')[1]
        target_camera_number = target_file.split('_')[-2].split('.')[0]

        source_path = os.path.join(source_directory, source_file)
        target_path = os.path.join(target_directory, target_file)

        source_mesh, target_mesh = utils.prepare_source_and_target_nonrigid_3d(source_path, target_path, voxel_size=0.0175)
        source_points = cp.asarray(source_mesh.points, dtype=cp.float32)
        target_points = cp.asarray(target_mesh.points, dtype=cp.float32)

        acpd = cpd.AffineCPD(source_points, use_cuda=True)
        start = time.time()
        tf_param, _, _ = acpd.registration(target_points)
        elapsed = time.time() - start
        print(f"Registration for {source_file} (source) and {target_file} (target) - Time: {elapsed}")

        result_points = tf_param.transform(source_points)
        result_np = cp.asnumpy(result_points)

        result_output_path = os.path.join(output_directory_1, f'result_{source_frame_number}_{source_camera_number}.txt')
        target_output_path = os.path.join(output_directory_2, f'target_{target_frame_number}_{target_camera_number}.txt')

        np.savetxt(result_output_path, result_np, delimiter=' ')
        np.savetxt(target_output_path, cp.asnumpy(target_points), delimiter=' ')

        source_pc = o3.geometry.PointCloud()
        source_pc.points = o3.utility.Vector3dVector(cp.asnumpy(source_points))
        source_pc.paint_uniform_color([1, 0, 0])  # RED

        target_pc = o3.geometry.PointCloud()
        target_pc.points = o3.utility.Vector3dVector(cp.asnumpy(target_points))
        target_pc.paint_uniform_color([0, 0, 1])  # BLUE

        result_pc = o3.geometry.PointCloud()
        result_pc.points = o3.utility.Vector3dVector(result_np)
        result_pc.paint_uniform_color([0, 1, 0])  # GREEN

        # Uncomment the line below if you want to display the target and the result
        #o3.visualization.draw_geometries([target_pc, result_pc])

        # Uncomment the line below if you want to display all three point clouds (source, target, result)
        #o3.visualization.draw_geometries([source_pc, target_pc, result_pc])

if __name__ == "__main__":
    # Expecting four command-line arguments: source directory, target directory, output directory 1, output directory 2
    import sys
    if len(sys.argv) != 5:
        print("Usage: python script.py <source_directory> <target_directory(old)> <result_directory> <target_directory(new)>")
        sys.exit(1)

    source_directory = sys.argv[1]      #source
    target_directory = sys.argv[2]      #target_old
    output_directory_1 = sys.argv[3]    #results
    output_directory_2 = sys.argv[4]    #target_new

    process_pointcloud_files(source_directory, target_directory, output_directory_1, output_directory_2)

    print("Script completed.")


#IN: preffix_<frame_number>_middle_<camera_number>_suffix.txt
#i.e. : frame_0184_0_Front_BNI_C1_filtered.txt
#i.e. : frame_0184_0_Front_BNI_C2_filtered.txt
    
#OUT: result_<frame_number>_<camera_number>.txt
#i.e. : result_0184_C1.txt
#i.e. : target_0184_C2.txt