import os

from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vtk, vuetify

from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

# Required for interactor initialization
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch  # noqa

# Required for rendering initialization, not necessary for
# local rendering, but doesn't hurt to include it
import vtkmodules.vtkRenderingOpenGL2  # noqa

CURRENT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))

# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# VTK pipeline
# -----------------------------------------------------------------------------

renderer = vtkRenderer()
renderWindow = vtkRenderWindow()
renderWindow.AddRenderer(renderer)

renderWindowInteractor = vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
renderWindowInteractor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()

# Read Data

# Extract Array/Field information

# Mesh
# Mesh: Setup default representation to surface
# Mesh: Apply rainbow color map
# Mesh: Color by default array

# Contour
# Contour: ContourBy default array
# Contour: Setup default representation to surface
# Contour: Apply rainbow color map
# Contour: Color by default array

# Cube Axes
# Cube Axes: Boundaries, camera, and styling

renderer.ResetCamera()

# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Views
# -----------------------------------------------------------------------------

local_view = vtk.VtkLocalView(renderWindow)
remote_view = vtk.VtkRemoteView(renderWindow, interactive_ratio=(1,))
html_view = local_view

# -----------------------------------------------------------------------------
# GUI elements
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

layout = SinglePage("Viewer", on_ready=html_view.update)
layout.title.set_text("Viewer")

with layout.toolbar:
    # toolbar components
    pass

with layout.content:
    # content components
    vuetify.VContainer(
        fluid=True,
        classes="pa-0 fill-height",
        children=[html_view],
    )

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    layout.start()
