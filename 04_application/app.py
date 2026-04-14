import os

from trame.app import TrameApp
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import vuetify3 as v3
from trame.widgets import vtk, trame
from trame.decorators import change

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
# Trame setup
# -----------------------------------------------------------------------------

class App(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)

# -----------------------------------------------------------------------------
# Callbacks
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# GUI elements
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

    def _build_ui(self):
        with SinglePageLayout(self.server) as self.ui:
            self.ui.title.set_text("Viewer")

            with self.ui.toolbar:
                # toolbar components
                pass

            with self.ui.content:
                # content components
                with v3.VContainer(
                    fluid=True,
                    classes="pa-0 fill-height",
                ):
                    view = vtk.VtkLocalView(renderWindow)
                    self.ctrl.view_update = view.update
                    self.ctrl.view_reset_camera = view.reset_camera

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main():
    app = App()
    app.server.start()

if __name__ == "__main__":
    main()