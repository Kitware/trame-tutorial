from paraview.web import venv  # Available in PV 5.10

import os

from trame.app import get_server
from trame.widgets import vuetify, paraview
from trame.ui.vuetify import SinglePageLayout

from paraview import simple

# -----------------------------------------------------------------------------
# trame setup
# -----------------------------------------------------------------------------

server = get_server()
state, ctrl = server.state, server.controller

# -----------------------------------------------------------------------------
# ParaView code
# -----------------------------------------------------------------------------

layout = None


def load_data():
    # CLI
    server.cli.add_argument("--data", help="Path to state file", dest="data")
    args, _ = server.cli.parse_known_args()

    full_path = os.path.abspath(args.data)
    working_directory = os.path.dirname(full_path)

    # ParaView
    simple.LoadState(
        full_path,
        data_directory=working_directory,
        restrict_to_data_directory=True,
    )
    view = simple.GetActiveView()
    view.MakeRenderWindowInteractor(True)

    # HTML
    with layout:
        with layout.content:
            with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
                html_view = paraview.VtkRemoteView(view)
                ctrl.view_reset_camera = html_view.reset_camera
                ctrl.view_update = html_view.update


# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------
state.trame__title = "State Viewer"

with SinglePageLayout(server) as layout:
    layout.icon.click = ctrl.view_reset_camera
    layout.title.set_text("ParaView State Viewer")

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    server.start()
