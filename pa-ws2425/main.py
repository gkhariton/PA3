import datetime
import os

import numpy as np
import project.functions as fn

def main():
    #1a, declare variables
    file_path = os.path.join("project", "data", "data_GdD_Datensatz_WS2425.h5")
    brewing = "brewing_001"
    tank_id = "B001"

    #1b, declare tupel
    measured_quantities = (
        "level", 
        "temperature", 
        "timestamp"
        )

    #1d, use read_metadata to read variables for brewing
    brewing_T_env = fn.read_metadata(file_path, brewing, "T_env")
    brewing_specific_heat_capacity_beer = fn.read_metadata(file_path, brewing, "specific_heat_capacity_beer")
    brewing_density_beer = fn.read_metadata(file_path, brewing, "density_beer")

    #1e, use read_metadata to read variables for sepcific tank 
    brewing_mass_tank = fn.read_metadata(file_path, brewing+"/"+tank_id, "mass_tank")
    brewing_surface_area_tank = fn.read_metadata(file_path, brewing+"/"+tank_id, "surface_area_tank")
    brewing_footprint_tank = fn.read_metadata(file_path, brewing+"/"+tank_id, "footprint_tank")
    brewing_heat_transfer_coeff_tank = fn.read_metadata(file_path, brewing+"/"+tank_id, "heat_transfer_coeff_tank")
    brewing_specific_heat_capacity_tank = fn.read_metadata(file_path, brewing+"/"+tank_id, "specific_heat_capacity_tank")

    #1f, create df_data dictionary
    df_data = {}

    #2a, create raw_data dictionary
    raw_data = {}

    #2a adn 2d, create loop that repeats for measured_quantities times. Store data in raw_data dictionary
    for i in measured_quantities:
        raw_data[i] = fn.read_data(file_path, brewing+"/"+tank_id+"/"+i)

    #2e, check array size
    fn.check_equal_length(raw_data["level"], raw_data["temperature"], raw_data["timestamp"])

    #3f, declare dictionary and tuple
    processed_data = {}
    df_data = {}
    filter_sizes = (10, 25, 58, 204) #custom filter width


    #convert timestamp data
    df_data["time"] = fn.process_time_data(raw_data["timestamp"])

    #remove negatives from the data
    NaN_level_data = fn.remove.negatives(raw_data["level"])
    #interpolate the data
    interpolated_level_data = fn.interpolate_nan_data(raw_data["timestamp"], NaN_level_data)

    #loop
    for i in filter_sizes:
        #filter temperature data
        processed_data["temperature_k_"+str(i)] = fn.filter_data(raw_data["temperature"],i)
        #filter interpolated level data
        processed_data["leve_k_"+str(i)] = fn.filter_data(interpolated_level_data, i)
    

if __name__ == "__main__":
    main()