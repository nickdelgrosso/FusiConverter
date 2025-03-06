from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable
from magicgui import magicgui
import napari
import numpy as np
from numpydantic import NDArray, Shape
import cortical


@dataclass
class NapariPresenter(cortical.workflow_load_fusion.Presenter):
    viewer: napari.Viewer

    def show_fusion_image(self, image):
        self.viewer.add_image(image, name='Fusion')
        

viewer = napari.Viewer()

load_fusion_file = cortical.workflow_load_fusion.LoadFusionFile(
    _repo=cortical.workflow_load_fusion.Repo(),
    _presenter=NapariPresenter(viewer=viewer),
)

load_fusion_file_widget = magicgui(call_button="Load Fusion File")(load_fusion_file)
viewer.window.add_dock_widget(load_fusion_file_widget)

napari.run()