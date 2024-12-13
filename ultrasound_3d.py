import nrrd
import vtk
import numpy as np
from vtk.util import numpy_support

def numpy_to_vtk_image(numpy_array):
    vtk_data = numpy_support.numpy_to_vtk(numpy_array.ravel(), deep=True, array_type=vtk.VTK_FLOAT)
    vtk_image = vtk.vtkImageData()
    vtk_image.SetDimensions(numpy_array.shape[::-1])  # Ensure dimensions are in (x, y, z) order
    vtk_image.GetPointData().SetScalars(vtk_data)
    return vtk_image

# Load NRRD file
nrrd_file = r"C:\Users\Admin\Downloads\poop\IMG_20240515_2_10.dcm.nrrd"
data, header = nrrd.read(nrrd_file)

# Print the header information
print("NRRD Header Information:")
for key, value in header.items():
    print(f"{key}: {value}")

# Print the shape of the data
print("\nData Shape:", data.shape)

# Extract a single 3D volume (e.g., select the first channel)
if len(data.shape) == 4:
    data = data[0, :, :, :]  # Select the first channel for simplicity

# Print the shape after extraction
print("Data shape after extraction:", data.shape)

# Check if the data contains any non-zero values
print("Non-zero values in data:", np.sum(data))

# Convert the NRRD data to a VTK image data object
vtk_image = numpy_to_vtk_image(data)

# Check if vtk_image has any data
if vtk_image.GetPointData().GetNumberOfArrays() == 0:
    print("vtk_image has no data.")
else:
    print("vtk_image has data.")

# Apply Marching Cubes to extract the 3D surface
marching_cubes = vtk.vtkMarchingCubes()
marching_cubes.SetInputData(vtk_image)
marching_cubes.SetValue(0, np.max(data) / 2)  # Adjust threshold based on your data
marching_cubes.Update()  # Ensure the algorithm processes the input

# Create a 3D model
model = vtk.vtkPolyDataNormals()
model.SetInputConnection(marching_cubes.GetOutputPort())
model.Update()  # Ensure the model is updated

# Check if the model has any data
if model.GetOutput().GetNumberOfCells() == 0:
    print("Model has no data.")
else:
    print("Model has data.")

# Write the model to STL file in the same folder as the input file
stl_file = r"C:\Users\Admin\Downloads\poop\fetal_model.stl"
stl_writer = vtk.vtkSTLWriter()
stl_writer.SetFileName(stl_file)
stl_writer.SetInputConnection(model.GetOutputPort())
stl_writer.Write()

print(f"3D model saved as {stl_file}")

# Visualization code (optional)
renderer = vtk.vtkRenderer()
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window_interactor = vtk.vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Load and visualize the STL file
stl_reader = vtk.vtkSTLReader()
stl_reader.SetFileName(stl_file)

mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(stl_reader.GetOutputPort())
actor = vtk.vtkActor()
actor.SetMapper(mapper)

renderer.AddActor(actor)
renderer.SetBackground(1, 1, 1)  # Background color white
render_window.Render()
render_window_interactor.Start()
