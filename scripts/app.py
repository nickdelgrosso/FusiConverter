from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable
from magicgui import magicgui
import napari
import numpy as np
from numpydantic import NDArray, Shape
import cortical


class Presenter(ABC):

    @abstractmethod
    def show_fusion_image(self, image: NDArray[Shape['* i, * j, * k, * time'], np.float32]):
        ...


@dataclass
class NapariPresenter(Presenter):
    viewer: napari.Viewer

    def show_fusion_image(self, image):
        self.viewer.add_image(image, name='Fusion')
        


@dataclass
class Repo:
    fusion_data: cortical.OpenfusFusionData = None



@dataclass
class LoadFusionFile:
    _repo: Repo
    _presenter: Presenter
    _open_dialog: Callable[[], str] = cortical.open_file_dialog
    _loader: Callable[[str], cortical.OpenfusFusionData] = cortical.load_openfus_mat

    def __call__(self):
        filepath = self._open_dialog()
        print(filepath)
        data = self._loader(filename=filepath)
        self._repo.fusion_data = data
        self._presenter.show_fusion_image(image=data.image)



viewer = napari.Viewer()

load_fusion_file = LoadFusionFile(
    _repo=Repo(),
    _presenter=NapariPresenter(viewer=viewer),
)

load_fusion_file_widget = magicgui(call_button="Load Fusion File")(load_fusion_file)
viewer.window.add_dock_widget(load_fusion_file_widget)

napari.run()