from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable
import numpy as np
from numpydantic import NDArray, Shape
from . import io, widgets



class Presenter(ABC):

    @abstractmethod
    def show_fusion_image(self, image: NDArray[Shape['* i, * j, * k, * time'], np.float32]):
        ...


@dataclass
class Repo:
    fusion_data: io.OpenfusFusionData = None



@dataclass
class LoadFusionFile:
    _repo: Repo
    _presenter: Presenter
    _open_dialog: Callable[[], str] = widgets.open_file_dialog
    _loader: Callable[[str], io.OpenfusFusionData] = io.load_openfus_mat

    def __call__(self):
        filepath = self._open_dialog()
        print(filepath)
        data = self._loader(filename=filepath)
        self._repo.fusion_data = data
        self._presenter.show_fusion_image(image=data.image)

