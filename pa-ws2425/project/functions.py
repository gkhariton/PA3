from typing import Any

import h5py as h5
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
from numpy.typing import NDArray
import pandas as pd
from plotid.publish import publish
from plotid.tagplot import tagplot

#1c, implement fucntion read_metadata, read the metadata and attribute of h5
def read_metadata(file, path: str, attr_key: str) -> Any | None:
    try:
        file_read = h5.File(file,"r")
        file_read = file_read[path]
        output = np. array(file_read)
        return output
    except:
        print("Error: invalid data")
    

#2b, implement fucntion read_metadata, read the metadata and attribute of h5
def read_data(file: str, path: str) -> NDArray | None:
    try:
        file_read = h5.File(file,"r")
        file_read = file_read[path]
        output = np.array(file_read)
        return output
    except:
        print("Error: invalid file/path")
        return None

#2c, check if array length are uniform
def check_equal_length(*arrays: NDArray) -> bool:
    # if array is empty return false
    if arrays: 
        return False

    array_size = len(arrays[0].shape)
    for i in arrays:
        if(array_size != len(i.shape)):
            raise ValueError("invalid array")
    return True

def process_time_data(data: NDArray) -> NDArray:
    pass


def remove_negatives(array: NDArray) -> NDArray:
    pass


def linear_interpolation(
    time: NDArray, start_time: float, end_time: float, start_y: float, end_y: float
) -> NDArray:
    pass


def interpolate_nan_data(time: NDArray, y_data: NDArray) -> NDArray:
    pass


def filter_data(data: NDArray, window_size: int) -> NDArray:
    """Filter data using a moving average approach.

    Args:
        data (NDArray): Data to be filtered
        window_size (int): Window size of the filter

    Returns:
        NDArray: Filtered data
    """
    output = []
    pad_width = window_size // 2
    padded_data = np.pad(array=data, pad_width=pad_width, mode="empty")
    for i in range(pad_width, padded_data.size - pad_width):
        # Implementieren Sie hier den SMA!
        sma = []
        output.append(sma)
    return np.array(output)



def calc_heater_heat_flux(P_heater: float, eta_heater: float) -> float:
    pass


def calc_convective_heat_flow(
    k_tank: float, area_tank: float, t_total: float, t_env: float
) -> float:
    pass


def calc_mass_flow(
    level_data: NDArray, tank_footprint: float, density: float
) -> NDArray:
    pass


def calc_transported_power(
    mass_flow: float, specific_heat_capacity: float, temperature: float
) -> float:
    pass


def store_plot_data(
    data: dict[str, NDArray], file_path: str, group_path: str, metadata: dict[str, Any]
) -> None:
    pass


def read_plot_data(
    file_path: str, group_path: str
) -> tuple[pd.DataFrame, dict[str, Any]]:
    pass


def plot_data(data: pd.DataFrame, formats: dict[str, str]) -> Figure:
    pass


def publish_plot(
    fig: Figure, source_paths: str | list[str], destination_path: str
) -> None:
    pass


if __name__ == "__main__":
    pass
