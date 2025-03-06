from dataclasses import dataclass
from typing import Callable
from magicgui import magicgui
import napari
import cortical


@dataclass
class LoadFusionFile:
    _viewer: napari.Viewer
    _open_dialog: Callable[[], str] = cortical.open_file_dialog
    _loader: Callable[[str], cortical.OpenfusFusionData] = cortical.load_openfus_mat

    def __call__(self):
        filepath = self._open_dialog()
        print(filepath)
        data = self._loader(filename=filepath)
        self._viewer.add_image(data.image, name='Fusion')



viewer = napari.Viewer()

load_fusion_file_widget = magicgui(call_button="Load Fusion File")(LoadFusionFile(_viewer=viewer))
viewer.window.add_dock_widget(load_fusion_file_widget)

napari.run()