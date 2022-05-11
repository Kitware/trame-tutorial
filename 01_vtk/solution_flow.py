import os
from trame.app import get_server
from trame.ui.vuetify import SinglePageLayout
from trame.widgets import vtk, vuetify

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import (
    vtkContourFilter,
    vtkGlyph3D,
    vtkMaskPoints,
    vtkThresholdPoints,
)
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkIOLegacy import vtkStructuredPointsReader
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

CURRENT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))

# -----------------------------------------------------------------------------
# VTK pipeline
# -----------------------------------------------------------------------------

renderer = vtkRenderer()
renderWindow = vtkRenderWindow()
renderWindow.AddRenderer(renderer)

renderWindowInteractor = vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
renderWindowInteractor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()

# Read the data

reader = vtkStructuredPointsReader()
reader.SetFileName(os.path.join(CURRENT_DIRECTORY, "../data/carotid.vtk"))

# Glyphs

threshold = vtkThresholdPoints()
threshold.SetInputConnection(reader.GetOutputPort())
threshold.ThresholdByUpper(200)

mask = vtkMaskPoints()
mask.SetInputConnection(threshold.GetOutputPort())
mask.SetOnRatio(5)

cone = vtkConeSource()
cone.SetResolution(11)
cone.SetHeight(1)
cone.SetRadius(0.25)

cones = vtkGlyph3D()
cones.SetInputConnection(mask.GetOutputPort())
cones.SetSourceConnection(cone.GetOutputPort())
cones.SetScaleFactor(0.4)
cones.SetScaleModeToScaleByVector()

lut = vtkLookupTable()
lut.SetHueRange(0.667, 0.0)
lut.Build()

scalarRange = [0] * 2
cones.Update()
scalarRange[0] = cones.GetOutput().GetPointData().GetScalars().GetRange()[0]
scalarRange[1] = cones.GetOutput().GetPointData().GetScalars().GetRange()[1]

vectorMapper = vtkPolyDataMapper()
vectorMapper.SetInputConnection(cones.GetOutputPort())
vectorMapper.SetScalarRange(scalarRange[0], scalarRange[1])
vectorMapper.SetLookupTable(lut)

vectorActor = vtkActor()
vectorActor.SetMapper(vectorMapper)

# Contours

iso = vtkContourFilter()
iso.SetInputConnection(reader.GetOutputPort())
iso.SetValue(0, 175)

isoMapper = vtkPolyDataMapper()
isoMapper.SetInputConnection(iso.GetOutputPort())
isoMapper.ScalarVisibilityOff()

isoActor = vtkActor()
isoActor.SetMapper(isoMapper)
isoActor.GetProperty().SetRepresentationToWireframe()
isoActor.GetProperty().SetOpacity(0.25)

# Outline

colors = vtkNamedColors()

outline = vtkOutlineFilter()
outline.SetInputConnection(reader.GetOutputPort())

outlineMapper = vtkPolyDataMapper()
outlineMapper.SetInputConnection(outline.GetOutputPort())

outlineActor = vtkActor()
outlineActor.SetMapper(outlineMapper)
outlineActor.GetProperty().SetColor(colors.GetColor3d("White"))

# Add the actors to the renderer

renderer.AddActor(outlineActor)
renderer.AddActor(vectorActor)
renderer.AddActor(isoActor)
renderer.ResetCamera()
renderWindow.Render()

# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

server = get_server()
ctrl = server.controller

with SinglePageLayout(server) as layout:
    layout.title.set_text("Hello trame")

    with layout.content:
        with vuetify.VContainer(
            fluid=True,
            classes="pa-0 fill-height",
        ):
            view = vtk.VtkLocalView(renderWindow)
            ctrl.on_server_ready.add(view.update)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
