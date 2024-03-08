import pymeshlab as ml

# Initialize MeshLab server
ms = ml.MeshSet()

# Load point cloud
ms.load_new_mesh("test.xyz")

# Compute normals for point sets
ms.apply_filter("compute_normal_for_point_clouds")


# compute_normal_for_point_clouds

# MeshLab filter name: ‘Compute normals for point sets’

# Compute the normals of the vertices of a mesh without exploiting the triangle connectivity, useful for dataset with no faces
# Parameters:

# k : int = 10

# Neighbour num: The number of neighbors used to estimate normals.
# smoothiter : int = 0

# Smooth Iteration: The number of smoothing iteration done on the p used to estimate and propagate normals.
# flipflag : bool = False

# Flip normals w.r.t. viewpoint: If the 'viewpoint' (i.e. scanner position) is known, it can be used to disambiguate normals orientation, so that all the normals will be oriented in the same direction.
# viewpos : numpy.ndarray[numpy.float64[3]] = [0, 0, 0]

# Viewpoint Pos.: The viewpoint position can be set by hand (i.e. getting the current viewpoint) or it can be retrieved from mesh camera, if the viewpoint position is stored there.



# Surface reconstruction: Ball Pivoting
ms.apply_filter("generate_surface_reconstruction_ball_pivoting")


# generate_surface_reconstruction_ball_pivoting

# MeshLab filter name: ‘Surface Reconstruction: Ball Pivoting’

# Given a point cloud with normals it reconstructs a surface using the Ball Pivoting Algorithm.Starting with a seed triangle, the BPA algorithm pivots a ball of the given radius around the already formed edges until it touches another point, forming another triangle. The process continues until all reachable edges have been tried. This surface reconstruction algorithm uses the existing points without creating new ones. Works better with uniformly sampled point clouds. If needed first perform a poisson disk subsampling of the point cloud.
# Bernardini F., Mittleman J., Rushmeier H., Silva C., Taubin G.
# The ball-pivoting algorithm for surface reconstruction.
# IEEE TVCG 1999
# Parameters:

# ballradius : PercentageValue = 0%

# Pivoting Ball radius (0 autoguess): The radius of the ball pivoting (rolling) over the set of points. Gaps that are larger than the ball radius will not be filled; similarly the small pits that are smaller than the ball radius will be filled.
# clustering : float = 20

# Clustering radius (% of ball radius): To avoid the creation of too small triangles, if a vertex is found too close to a previous one, it is clustered/merged with it.
# creasethr : float = 90

# Angle Threshold (degrees): If we encounter a crease angle that is too large we should stop the ball rolling
# deletefaces : bool = False

# Delete initial set of faces: if true all the initial faces of the mesh are deleted and the whole surface is rebuilt from scratch. Otherwise the current faces are used as a starting point. Useful if you run the algorithm multiple times with an increasing ball radius.



# Export the result as OBJ
output_mesh_path = "output_mesh.obj"
ms.save_current_mesh(output_mesh_path)

print("Surface reconstruction complete. Output saved to:", output_mesh_path)



#
#One Foot appear to be inverted. Need to add:
#


# meshing_invert_face_orientation.

# MeshLab filter name: ‘Invert Faces Orientation’

# Invert faces orientation, flipping the normals of the mesh.
# If requested, it tries to guess the right orientation; mainly it decide to flip all the faces if the minimum/maximum vertices have not outward point normals for a few directions.
# Works well for single component watertight objects.
# Parameters:

# forceflip : bool = True

# Force Flip: If selected, the normals will always be flipped; otherwise, the filter tries to set them outside
# onlyselected : bool = False

# Flip only selected faces: If selected, only selected faces will be affected



#
#Investigate Using
#



# generate_surface_reconstruction_screened_poisson
# MeshLab filter name: ‘Surface Reconstruction: Screened Poisson’

# This surface reconstruction algorithm creates watertight surfaces from oriented point sets.
# The filter uses the original code of Michael Kazhdan and Matthew Bolitho implementing the algorithm described in the following paper:
# Michael Kazhdan, Hugues Hoppe,
# "Screened Poisson surface reconstruction"
# Parameters:

# visiblelayer : bool = False

# Merge all visible layers: Enabling this flag means that all the visible layers will be used for providing the points.
# depth : int = 8

# Reconstruction Depth: This integer is the maximum depth of the tree that will be used for surface reconstruction. Running at depth d corresponds to solving on a voxel grid whose resolution is no larger than 2^d x 2^d x 2^d. Note that since the reconstructor adapts the octree to the sampling density, the specified reconstruction depth is only an upper bound. The default value for this parameter is 8.
# fulldepth : int = 5

# Adaptive Octree Depth: This integer specifies the depth beyond depth the octree will be adapted. At coarser depths, the octree will be complete, containing all 2^d x 2^d x 2^d nodes. The default value for this parameter is 5.
# cgdepth : int = 0

# Conjugate Gradients Depth: This integer is the depth up to which a conjugate-gradients solver will be used to solve the linear system. Beyond this depth Gauss-Seidel relaxation will be used. The default value for this parameter is 0.
# scale : float = 1.1

# Scale Factor: This floating point value specifies the ratio between the diameter of the cube used for reconstruction and the diameter of the samples' bounding cube. The default value is 1.1.
# samplespernode : float = 1.5

# Minimum Number of Samples: This floating point value specifies the minimum number of sample points that should fall within an octree node as the octree construction is adapted to sampling density. For noise-free samples, small values in the range [1.0 - 5.0] can be used. For more noisy samples, larger values in the range [15.0 - 20.0] may be needed to provide a smoother, noise-reduced, reconstruction. The default value is 1.5.
# pointweight : float = 4

# Interpolation Weight: This floating point value specifies the importants that interpolation of the point samples is given in the formulation of the screened Poisson equation. The results of the original (unscreened) Poisson Reconstruction can be obtained by setting this value to 0. The default value for this parameter is 4.
# iters : int = 8

# Gauss-Seidel Relaxations: This integer value specifies the number of Gauss-Seidel relaxations to be performed at each level of the hierarchy. The default value for this parameter is 8.
# confidence : bool = False

# Confidence Flag: Enabling this flag tells the reconstructor to use the quality as confidence information; this is done by scaling the unit normals with the quality values. When the flag is not enabled, all normals are normalized to have unit-length prior to reconstruction.
# preclean : bool = False

# Pre-Clean: Enabling this flag force a cleaning pre-pass on the data removing all unreferenced vertices or vertices with null normals.
# threads : int = 16

# Number Threads: Maximum number of threads that the reconstruction algorithm can use.



#TO COMMENT IN A LARGE SECTION USE CTRL + K + C
#TO COMMENT OUT A LARGE SECTION USE CTRL + K + U