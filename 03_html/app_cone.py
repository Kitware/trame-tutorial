from trame.app import TrameApp
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import vtk, vuetify3 as v3

from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

# Required for interactor initialization
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch  # noqa: F401

# Required for rendering initialization, not necessary for
# local rendering, but doesn't hurt to include it
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

class AppCone(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)
        self.vtk_pipeline()
        self._build_ui()
    
    def vtk_pipeline(self):
        self.renderer = vtkRenderer()
        self.renderWindow = vtkRenderWindow()
        self.renderWindow.AddRenderer(self.renderer)

        self.renderWindowInteractor = vtkRenderWindowInteractor()
        self.renderWindowInteractor.SetRenderWindow(self.renderWindow)
        self.renderWindowInteractor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()

        self.cone_source = vtkConeSource()
        self.mapper = vtkPolyDataMapper()
        self.mapper.SetInputConnection(self.cone_source.GetOutputPort())
        self.actor = vtkActor()
        self.actor.SetMapper(self.mapper)

        self.renderer.AddActor(self.actor)
        self.renderer.ResetCamera()

    def _build_ui(self):
        with SinglePageLayout(self.server) as self.ui:
            self.ui.title.set_text("Hello trame")

            with self.ui.content:
                with v3.VContainer(
                    fluid=True,
                    classes="pa-0 fill-height",
                ):
                    self.view = vtk.VtkLocalView(self.renderWindow)

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main():
    app = AppCone()
    app.server.start()

if __name__ == "__main__":
    main()