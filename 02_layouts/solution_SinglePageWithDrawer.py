from trame.layouts import SinglePageWithDrawer
from trame.html import vtk, vuetify

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
# GUI
# -----------------------------------------------------------------------------

html_view = vtk.VtkLocalView(renderWindow)

layout = SinglePageWithDrawer("Hello trame", on_ready=html_view.update)
layout.title.set_text("Hello trame")

layout.content.children += [
    vuetify.VContainer(
        fluid=True,
        classes="pa-0 fill-height",
        children=[html_view],
    )
]

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    layout.start()
