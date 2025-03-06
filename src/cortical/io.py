from dataclasses import dataclass
from pathlib import Path

import numpy as np
from numpy.typing import NDArray
from scipy import io

@dataclass
class OpenfusFusionData:
    image: NDArray[np.float32]

    def __post_init__(self):
        assert self.image.ndim == 4   


def load_openfus_mat(filename: str | Path, _reader=io.loadmat) -> OpenfusFusionData:
    filepath = Path(filename)
    data = _reader(filename)
    
    image = data['I']
    return OpenfusFusionData(image=image)




