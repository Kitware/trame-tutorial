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
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleSwitch  # noqa

# Required for rendering initialization, not necessary for
# local rendering, but doesn't hurt to include it
import vtkmodules.vtkRenderingOpenGL2  # noqa


# -----------------------------------------------------------------------------
# VTK pipeline
# -----------------------------------------------------------------------------

renderer = vtkRenderer()
renderWindow = vtkRenderWindow()
renderWindow.AddRenderer(renderer)

renderWindowInteractor = vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
renderWindowInteractor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()

cone_source = vtkConeSource()
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(cone_source.GetOutputPort())
actor = vtkActor()
actor.SetMapper(mapper)

renderer.AddActor(actor)
renderer.ResetCamera()

# -----------------------------------------------------------------------------
# Trame
# -----------------------------------------------------------------------------

class AppLayouts(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)
        self._build_ui()

    def _build_ui(self):
        with SinglePageLayout(self.server) as self.ui:
            self.ui.title.set_text("Hello trame")

            with self.ui.content:
                with v3.VContainer(
                    fluid=True,
                    classes="pa-0 fill-height",
                ):
                    html_view = vtk.VtkLocalView(renderWindow)
                    self.ctrl.on_server_ready.add(html_view.update)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main():
    app = AppLayouts()
    app.server.start()

if __name__ == "__main__":
    main()
