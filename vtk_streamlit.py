import os
import streamlit as st
import numpy as np
import pydicom
import vtk
from vtk.util.numpy_support import numpy_to_vtk
import pyvista as pv
from stpyvista import stpyvista
import tempfile

# Title
st.title("DICOM 3D Volume Visualization and STL Export")

# Upload DICOM directory
uploaded_files = st.file_uploader("Upload DICOM Files", type="dcm", accept_multiple_files=True)

if uploaded_files:
    # Load DICOM files and create 3D volume
    slices = [pydicom.dcmread(f).pixel_array for f in uploaded_files]
    volume = np.stack(slices, axis=0)

    # Create VTK ImageData object from the volume
    vtk_data = vtk.vtkImageData()
    vtk_data.SetDimensions(volume.shape[2], volume.shape[1], volume.shape[0])
    vtk_data.SetSpacing(1, 1, 1)
    vtk_data.SetOrigin(0, 0, 0)

    # Convert the volume to VTK-compatible format
    vtk_array = numpy_to_vtk(volume.ravel(), deep=True)
    vtk_data.GetPointData().SetScalars(vtk_array)

    # Slider for threshold adjustment
    threshold = st.slider("Threshold", min_value=0, max_value=1000, value=300)

    # Extract surface using Marching Cubes
    contour_filter = vtk.vtkMarchingCubes()
    contour_filter.SetInputData(vtk_data)
    contour_filter.SetValue(0, threshold)
    contour_filter.Update()

    # Convert the contour to PyVista mesh
    surface_mesh = pv.wrap(contour_filter.GetOutput())

    # Display the 3D model using PyVista with customized colors
    plotter = pv.Plotter(window_size=[400, 400])
    
    # Set the background color to light blue and the mesh color to yellow
    plotter.set_background("lightblue")  # Light blue background
    plotter.add_mesh(surface_mesh, color='yellow', show_edges=True)  # Yellow foreground (mesh)

    # Adjust camera view to isometric
    plotter.view_isometric()
    
    # Display using stpyvista
    stpyvista(plotter)

    # Save STL file to a temporary location for download
    temp_stl = tempfile.NamedTemporaryFile(delete=False, suffix=".stl")
    output_stl_file = temp_stl.name

    # Write the STL file
    stl_writer = vtk.vtkSTLWriter()
    stl_writer.SetInputData(contour_filter.GetOutput())
    stl_writer.SetFileName(output_stl_file)
    stl_writer.Write()

    # Provide a download link for the STL file
    with open(output_stl_file, "rb") as f:
        st.download_button(
            label="Download STL File",
            data=f,
            file_name="extracted_surface.stl",
            mime="application/octet-stream"
        )
