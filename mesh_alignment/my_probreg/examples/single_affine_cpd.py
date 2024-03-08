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

source, target = utils.prepare_source_and_target_nonrigid_3d('frame_0175_0_Front_BNI_C3_filtered.txt', 'frame_0175_0_Front_BNI_C1_filtered.txt', voxel_size=0.0175)
source = cp.asarray(source.points, dtype=cp.float32)
target = cp.asarray(target.points, dtype=cp.float32)

acpd = cpd.AffineCPD(source, use_cuda=use_cuda)
start = time.time()
tf_param, _, _ = acpd.registration(target)
elapsed = time.time() - start
print("time: ", elapsed)

print("result: ", to_cpu(tf_param.b), to_cpu(tf_param.t))

result1 = tf_param.transform(source)
pc1 = o3.geometry.PointCloud()
pc1.points = o3.utility.Vector3dVector(to_cpu(result1))
pc1.paint_uniform_color([0, 1, 0])

result2 = target
pc2 = o3.geometry.PointCloud()
pc2.points = o3.utility.Vector3dVector(to_cpu(result2))
pc2.paint_uniform_color([0, 0, 1])

result3 = source
pc3 = o3.geometry.PointCloud()
pc3.points = o3.utility.Vector3dVector(to_cpu(result3))
pc3.paint_uniform_color([1, 0, 0])

o3.visualization.draw_geometries([pc1, pc2])
#o3.visualization.draw_geometries([pc1, pc2, pc3])


