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
def read_metadata(file: str, path: str, attr_key: str) -> Any | None:
    try:
        file_read = h5.File(file,"r")
        file_read = file_read[path]
        output = file_read.attrs[attr_key]
        return (output)
    
    except KeyError:
        print("Error: invalid data")

    except:
        print("Error")
        
    

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
    if not arrays: 
        return False

    array_size = len(arrays[0].shape)
    for i in arrays:
        if(array_size != len(i.shape)):
            raise ValueError("invalid array")
    return True

#3a, convert time data from miliseconds into seconds
def process_time_data(data: NDArray) -> NDArray:
    #if data is empty return data
    if data.size == 0:
        return data
    
    start_time = data[0]
    output = data.copy()
    #convert data in miliseconds into seconds
    for key, value in enumerate(output):
        output[key] = (value - start_time)/1000

    return(output)

#3b, remove negative elements from the data
def remove_negatives(array: NDArray) -> NDArray:
    if array.size == 0:
        return array

    output = array.copy()

    #if value is negative replace value with np.nan
    for key,value in enumerate(output):
        if value < 0:
            output[key] = np.nan
    return output


#3c, interpolate the array
def linear_interpolation(
    time: NDArray, start_time: float, end_time: float, start_y: float, end_y: float
) -> NDArray:
    # if empty, return empty
    if time.size == 0:
        return time
    
    output = time.copy()

    temp1 = end_y-start_y
    temp2 = end_time-start_time

    for key,value in enumerate(time):
        output[key] = start_y + (temp1 * ((value-start_time)/temp2)) #mathematical equation

    return output


#3d, Interpolate NaN data
def interpolate_nan_data(time: NDArray, y_data: NDArray) -> NDArray:
    #Check if interpolation is possible
    if np.isnan.isnan(y_data[0]) or np.isnan(y_data[-1]):
        raise ValueError("Data cannot be interpolated")
    
    #Declare variables
    active_gap = False
    interpolated_data = y_data.copy()

    for key,value in enumerate(y_data):
        #Start an index
        if(not active_gap and np.isnan(value)):
            start_index = key
            active_gap = True
        #Stop indexing and interpolate
        elif(active_gap and not np.isnan(value)):
            end_index = key
            active_gap = False

            #time[start_index-1]=x1,time[end_index]=x2
            #y_data[start_index-1]=y1,y_data[end_index]=y2
            #run linear_interpolation on specific section of the array
            interpolated_data[start_index:end_index] = linear_interpolation(time[start_index:end_index], time[start_index-1], time[end_index], y_data[start_index-1], y_data[end_index])

    return interpolated_data


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
        # Set upper boundary
        if(i-pad_width<=pad_width):
            left_window_index = pad_width
        else:
            left_window_index = i-pad_width

        # Set lower boundary
        if(i+pad_width>=(padded_data.size-pad_width)):
            right_window_index = (padded_data.size - pad_width)
        else:
            right_window_index = i+pad_width+1
        sma = padded_data[left_window_index:right_window_index] #slice
        sma = np.mean(sma)

        output.append(sma) #add to data list
    return np.array(output)



def calc_heater_heat_flux(P_heater: float, eta_heater: float) -> float:
    return (P_heater*eta_heater)


def calc_convective_heat_flow(
    k_tank: float, area_tank: float, t_total: float, t_env: float
) -> float:
    return (k_tank*area_tank*(t_total-t_env))


def calc_mass_flow(
    level_data: NDArray, tank_footprint: float, density: float
) -> NDArray:
    output = level_data.copy()
    for key,value in enumerate(level_data):
        output[key] = value*tank_footprint*density
    return output


def calc_transported_power(
    mass_flow: float, specific_heat_capacity: float, temperature: float
) -> float:
    return(mass_flow*specific_heat_capacity*temperature)


def store_plot_data(
    data: dict[str, NDArray], file_path: str, group_path: str, metadata: dict[str, Any]
) -> None:
    #convert dictionary to DataFrane
    dataframe = pd.DataFrame(data)

    with pd.HDFStore(file_path, mode="w") as file_write:
        file_write.put(group_path, dataframe, format="table")

        #store metadata as attributes
        for key,value in metadata.items():
            file_write.get_storer(group_path).attrs[key] = value
    
    print("Data and Metadata stored in "+file_path+"under"+group_path)

def read_plot_data(
    file_path: str, group_path: str
) -> tuple[pd.DataFrame, dict[str, Any]]:
    with pd.HDFStore(file_path, mode="r") as file_read:
        dataframe = file_read.get(group_path)

        output_metadata = {}

        try:
            output_metadata["legend_title"] - file_read.get_storer(group_path).attrs.legend_title
            output_metadata["x_label"] = file_read.get_storer(group_path).attrs.x_label
            output_metadata["x_unit"] = file_read.get_storer(group_path).attrs.x_unit
            output_metadata["y_label"] = file_read.get_storer(group_path).attrs.y_label
            output_metadata["y_unit"] = file_read.get_storer(group_path).attrs.y_unit
        except KeyError:
            print("No metadata found")

    return dataframe, output_metadata


def plot_data(data: pd.DataFrame, formats: dict[str, str]) -> Figure:
    fig, current_plot = plt.subplots(figsize=(10, 10))

    time_second = data["time"]
    time_hour = time_second / 3600

    inner_energy_204_giga = data["inner_energy_k_204"] / 1000000
    inner_energy_58_giga = data["inner_energy_k_58"] / 1000000
    inner_energy_25_giga = data["inner_energy_k_25"] / 1000000
    inner_energy_10_giga = data["inner_energy_k_10"] / 1000000

    #plot for every filter size
    current_plot.plot(time_hour, inner_energy_204_giga, label="Internal Energy k_204", color="#1f77b4", linewidth=0.5, alpha=0.7)
    current_plot.plot(time_hour, inner_energy_58_giga, label="Internal Energy k_58", color="#1f77b4", linewidth=0.5, alpha=0.7)
    current_plot.plot(time_hour, inner_energy_25_giga, label="Internal Energy k_25", color="#1f77b4", linewidth=0.5, alpha=0.7)
    current_plot.plot(time_hour, inner_energy_10_giga, label="Internal Energy k_10", color="#1f77b4", linewidth=0.5, alpha=0.7)

    #format from dictionary
    current_plot.set_xlabel(formats.get("xlabel", "Time (s)"))
    current_plot.set_ylabel(formats.get("ylabel", "Internal Energy (GJ)"))
    current_plot.set_title(formats.get("title", "Internal Energy over time (GJ/s)"))
    current_plot.legend()

    current_plot.grid(True, linestyle="--", alpha=0.7)

    return fig

def publish_plot(
    fig: Figure, source_paths: str | list[str], destination_path: str
) -> None:
    #Save with tagplot
    try:
        plot_id = tagplot(fig, engine="matplotlib", figure_ids =["GdD_WS_2425_2593450"], id_on_plot=True, fontsize=12)
        publish(plot_id, source_paths, destination_path)
    except:
        print("Error")

    print("Plot and data published to "+destination_path)

if __name__ == "__main__":
    pass
