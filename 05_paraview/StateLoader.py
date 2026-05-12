from trame.app import TrameApp
from trame.ui.vuetify3 import SinglePageLayout
from trame.widgets import vuetify3 as v3
from trame.widgets import paraview, client

from pathlib import Path

from paraview import simple

# -----------------------------------------------------------------------------
# Trame setup
# -----------------------------------------------------------------------------

class StateLoaderApp(TrameApp):

    def __init__(self, server=None):
        super().__init__(server)
        self.server.cli.add_argument("--data", help="Path to state file", dest="data")

        # Preload paraview modules onto server
        paraview.initialize(self.server)

        self.ctrl.on_server_ready.add(self.load_data)
        self._build_ui()


# -----------------------------------------------------------------------------
# ParaView code
# -----------------------------------------------------------------------------


    def load_data(self, **_):
        # CLI
        args, _ = self.server.cli.parse_known_args()

        full_path = str(Path(args.data).resolve().absolute())
        working_directory = str(Path(args.data).parent.resolve().absolute())

        # ParaView
        simple.LoadState(
            full_path,
            data_directory=working_directory,
            restrict_to_data_directory=True,
        )
        self.view = simple.GetActiveView()
        self.view.MakeRenderWindowInteractor(True)
        simple.Render(self.view)

        # HTML
        with SinglePageLayout(self.server) as self.ui:
            self.ui.icon.click = self.ctrl.view_reset_camera
            self.ui.title.set_text("ParaView State Viewer")

            with self.ui.content:
                with v3.VContainer(fluid=True, classes="pa-0 fill-height"):
                    html_view = paraview.VtkRemoteView(self.view)
                    self.ctrl.view_reset_camera = html_view.reset_camera
                    self.ctrl.view_update = html_view.update 

# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------

    def _build_ui(self):
        self.state.trame__title = "State Viewer"

        with SinglePageLayout(self.server) as self.ui:
            self.ui.icon.click = self.ctrl.view_reset_camera
            self.ui.title.set_text("ParaView State Viewer")

            with self.ui.content:
                with v3.VContainer(fluid=True, classes="pa-0 fill-height"):
                    client.Loading("Loading state")


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main():
    app = StateLoaderApp()
    app.server.start()

if __name__ == "__main__":
    main()
