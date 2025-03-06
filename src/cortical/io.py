from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from pydantic import BaseModel
import numpy as np
from numpydantic import NDArray, Shape
from scipy import io


class OpenfusFusionData(BaseModel):
    image: NDArray[Shape["* i, * j, * k, * time"], np.float32]
    time: NDArray[Shape["* time"], np.float64]
    t0: NDArray[Shape["*"], np.float64]
    origin: tuple[int, int, int]
    voxel_size: tuple[float, float, float]
    image_size: tuple[int, int, int]
    image_dims: int
    image_type: Literal['doppler']

    def __post_init__(self):
        assert self.image.ndim == 4   


def load_openfus_mat(filename: str | Path, _reader=io.loadmat) -> OpenfusFusionData:
    filepath = Path(filename)
    data = _reader(filename)
    
    image = data['I']
    time = data['metadata']['time'].item().flatten()
    t0 = data['metadata']['t0'].item().flatten()
    origin = tuple(data['metadata']['origen'].item().flatten().tolist())
    voxel_size = tuple(data['metadata']['voxelSize'].item().flatten().tolist())
    image_size = tuple(data['metadata']['imageSize'].item().flatten().tolist())
    image_dims = data['metadata']['imageDim'].item().item()  
    image_type = data['metadata']['imageType'].item().item()
    
    return OpenfusFusionData(
        image=image,
        time=time,
        origin=origin,
        t0=t0,
        voxel_size=voxel_size,
        image_size=image_size,
        image_dims=image_dims,
        image_type=image_type,
    )




