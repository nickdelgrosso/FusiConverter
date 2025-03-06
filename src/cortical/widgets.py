from pathlib import Path
import sys
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget, QVBoxLayout
from contextlib import contextmanager

@contextmanager
def qt_app():
    app = QApplication.instance()
    app_already_existed = bool(app)
    if not app_already_existed:
        app = QApplication(sys.argv)
    yield app


def open_file_dialog(message='Open OpenFus Fusion File', default="OpenFus Files (*.mat)") -> Path | None:
    with qt_app():
        filepath, _ = QFileDialog.getOpenFileName(None, message, "", default)
        if filepath:
            path = Path(filepath)
            if not path.exists():
                raise FileNotFoundError(filepath)
            return filepath
        else:
            return None
        