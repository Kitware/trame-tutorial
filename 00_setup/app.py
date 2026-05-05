from trame.app import TrameApp
from trame.ui.vuetify3 import SinglePageLayout

# -----------------------------------------------------------------------------
# Get a server to work with
# -----------------------------------------------------------------------------

class App(TrameApp):
    def __init__(self, server=None):
        super().__init__(server)
        self._build_ui()

# -----------------------------------------------------------------------------
# GUI
# -----------------------------------------------------------------------------
    def _build_ui(self):
        with SinglePageLayout(self.server) as self.ui:
            self.ui.title.set_text("Hello trame")

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

def main():
    app = App()
    app.server.start()

if __name__ == "__main__":
    main()