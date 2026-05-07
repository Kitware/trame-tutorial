#!/usr/bin/env python

# Web imports
import os
from trame.app import TrameApp
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import vtk, vuetify3 as v3

# -----------------------------------------------------------------------------
# Example:    SimpleRayCast
# taken from: https://kitware.github.io/vtk-examples/site/Python/
# -----------------------------------------------------------------------------

# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction
from vtkmodules.vtkIOLegacy import vtkStructuredPointsReader
from vtkmodules.vtkRenderingCore import (
    vtkColorTransferFunction,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkVolume,
    vtkVolumeProperty,
)
from vtkmodules.vtkRenderingVolume import vtkFixedPointVolumeRayCastMapper

# noinspection PyUnresolvedReferences
from vtkmodules.vtkRenderingVolumeOpenGL2 import vtkOpenGLRayCastImageDisplayHelper


CURRENT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))

# -----------------------------------------------------------------------------
# VTK pipeline
# -----------------------------------------------------------------------------

colors = vtkNamedColors()

# This is a simple volume rendering example that
# uses a vtkFixedPointVolumeRayCastMapper

# Create the standard renderer, render window
# and interactor.
ren1 = vtkRenderer()

renWin = vtkRenderWindow()
renWin.AddRenderer(ren1)

iren = vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.GetInteractorStyle().SetCurrentStyleToTrackballCamera()  # +++

# Create the reader for the data.
reader = vtkStructuredPointsReader()
reader.SetFileName(os.path.join(CURRENT_DIRECTORY, "../data/ironProt.vtk"))

# Create transfer mapping scalar value to opacity.
opacityTransferFunction = vtkPiecewiseFunction()
opacityTransferFunction.AddPoint(20, 0.0)
opacityTransferFunction.AddPoint(255, 0.2)

# Create transfer mapping scalar value to color.
colorTransferFunction = vtkColorTransferFunction()
colorTransferFunction.AddRGBPoint(0.0, 0.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(64.0, 1.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(128.0, 0.0, 0.0, 1.0)
colorTransferFunction.AddRGBPoint(192.0, 0.0, 1.0, 0.0)
colorTransferFunction.AddRGBPoint(255.0, 0.0, 0.2, 0.0)

# The property describes how the data will look.
volumeProperty = vtkVolumeProperty()
volumeProperty.SetColor(colorTransferFunction)
volumeProperty.SetScalarOpacity(opacityTransferFunction)
volumeProperty.ShadeOn()
volumeProperty.SetInterpolationTypeToLinear()

# The mapper / ray cast function know how to render the data.
volumeMapper = vtkFixedPointVolumeRayCastMapper()
volumeMapper.SetInputConnection(reader.GetOutputPort())

# The volume holds the mapper and the property and
# can be used to position/orient the volume.
volume = vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)

ren1.AddVolume(volume)
ren1.SetBackground(colors.GetColor3d("Wheat"))
ren1.GetActiveCamera().Azimuth(45)
ren1.GetActiveCamera().Elevation(30)
ren1.ResetCameraClippingRange()
ren1.ResetCamera()

# -----------------------------------------------------------------------------
# Web Application setup
# -----------------------------------------------------------------------------

class RayCastApp(TrameApp):
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
                    view = vtk.VtkRemoteView(renWin)
                    # view = vtk.VtkLocalView(renWin)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main():
    app_ray_cast = RayCastApp()
    app_ray_cast.server.start()

if __name__ == "__main__":
    main()
