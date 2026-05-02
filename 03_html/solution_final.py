from trame.app import TrameApp
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import vtk, vuetify3 as v3
from trame.decorators import change

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

DEFAULT_RESOLUTION = 6

class AppButtons(TrameApp):
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
    
    @change("resolution")
    def update_resolution(self, resolution, **_kwargs):
        self.cone_source.SetResolution(resolution)
        self.ctrl.view_update()

    def reset_resolution(self):
        self.state.resolution = DEFAULT_RESOLUTION

    def _build_ui(self):
        with SinglePageLayout(self.server, theme=("theme", "light")) as self.ui:
            self.ui.title.set_text("Hello trame")

            with self.ui.content:
                with v3.VContainer(
                    fluid=True,
                    classes="pa-0 fill-height",
                ):
                    self.view = vtk.VtkLocalView(self.renderWindow)
                    self.ctrl.view_reset_camera = self.view.reset_camera
                    self.ctrl.view_update = self.view.update

            with self.ui.toolbar:
                v3.VSpacer()
                v3.VSlider(
                    v_model=("resolution", DEFAULT_RESOLUTION), # (var_name, initial_value)
                    min=3, max=60, step=1,                      # min/max/step
                    hide_details=True, density="compact",       # presentation params
                    style="max-width: 300px",                   # css style
                )
                v3.VBtn(icon="mdi-restore", click=self.reset_resolution)
                v3.VDivider(vertical=True, classes="mx-2")
                v3.VSwitch(
                    v_model="theme",
                    false_value="light",
                    true_value="dark",
                    hide_details=True,
                    density="compact",
                )
                v3.VBtn(icon="mdi-crop-free", click=self.ctrl.view_reset_camera)

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main():
    app = AppButtons()
    app.server.start()

if __name__ == "__main__":
    main()
