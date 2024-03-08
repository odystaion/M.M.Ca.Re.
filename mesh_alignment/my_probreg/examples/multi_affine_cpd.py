import os
import numpy as np
use_cuda = True
if use_cuda:
    import cupy as cp
    to_cpu = cp.asnumpy
    cp.cuda.set_allocator(cp.cuda.MemoryPool().malloc)
else:
    cp = np
    to_cpu = lambda x: x
import open3d as o3
from probreg import cpd
from probreg import callbacks
import utils
import time

# Specify the directories containing the .txt files
source_directory = 'source'
target_directory = 'target'

# Get the list of files in each directory
source_files = sorted(os.listdir(source_directory))
target_files = sorted(os.listdir(target_directory))

# Output directory for saving resulting meshes
output_directory = 'results'
os.makedirs(output_directory, exist_ok=True)

# Iterate over corresponding files in the two directories
for source_file, target_file in zip(source_files, target_files):
    # Extract frame number and camera number from source file name
    source_frame_number = source_file.split('_')[1]
    source_camera_number = source_file.split('_')[-2].split('.')[0]

    # Extract frame number and camera number from target file name
    target_frame_number = target_file.split('_')[1]
    target_camera_number = target_file.split('_')[-2].split('.')[0]

    # Construct the full paths to the files
    source_path = os.path.join(source_directory, source_file)
    target_path = os.path.join(target_directory, target_file)

    # Prepare source and target from the current pair of files
    source_mesh, target_mesh = utils.prepare_source_and_target_nonrigid_3d(source_path, target_path, voxel_size=0.0175)
    source_points = cp.asarray(source_mesh.points, dtype=cp.float32)
    target_points = cp.asarray(target_mesh.points, dtype=cp.float32)

    # Perform registration
    acpd = cpd.AffineCPD(source_points, use_cuda=use_cuda)
    start = time.time()
    tf_param, _, _ = acpd.registration(target_points)
    elapsed = time.time() - start
    print(f"Registration for {source_file} (source) and {target_file} (target) - Time: {elapsed}")

    # Transform the source point cloud using the obtained transformation
    result_points = tf_param.transform(source_points)

    # Convert Cupy arrays to NumPy for saving
    result_np = to_cpu(result_points)

    # Save the resulting point cloud to a .txt file in the "results" directory
    result_output_path = os.path.join(output_directory, f'result_{source_frame_number}_{source_camera_number}.txt')
    np.savetxt(result_output_path, result_np, delimiter=' ')

    # Save the target point cloud to a .txt file in the "results" directory
    target_output_path = os.path.join(output_directory, f'target_{target_frame_number}_{target_camera_number}.txt')
    np.savetxt(target_output_path, to_cpu(target_points), delimiter=' ')

    # Display the results if needed
    source_pc = o3.geometry.PointCloud()
    source_pc.points = o3.utility.Vector3dVector(to_cpu(source_points))
    source_pc.paint_uniform_color([1, 0, 0]) #RED

    target_pc = o3.geometry.PointCloud()
    target_pc.points = o3.utility.Vector3dVector(to_cpu(target_points))
    target_pc.paint_uniform_color([0, 0, 1]) #BLUE

    result_pc = o3.geometry.PointCloud()
    result_pc.points = o3.utility.Vector3dVector(result_np)
    result_pc.paint_uniform_color([0, 1, 0]) #GREEN

    #o3.visualization.draw_geometries([target_pc, result_pc])

    # Uncomment the line below if you want to display all three point clouds
    #o3.visualization.draw_geometries([source_pc, target_pc, result_pc])

