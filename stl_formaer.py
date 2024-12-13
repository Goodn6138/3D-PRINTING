import numpy as np
from skimage import measure
import trimesh


voxel_data = np.zeros((10, 10,10))
voxel_data[3:7, 3:7 , 3:7] = 1

vertices, faces, normals, values = measure.marching_cubes(voxel_data, level=0.5)

mesh = trimesh.Trimesh(vertices = vertices, faces=faces, vertex_normals = normals)

output_stl_file = r'C:/Users/Admin/Desktop/drawing.stl'
mesh.export(output_stl_file, file_type = 'stl')
