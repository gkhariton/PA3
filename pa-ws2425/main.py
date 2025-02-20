import datetime
import os

import numpy as np
import project.functions as fn

import h5py

def main():
    #1a, declare variables
    file_path = "C:\\Users\ACER\Downloads\pa-ws2425\pa-ws2425\project\data\data_GdD_Datensatz_WS2425.h5"
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
    NaN_level_data = fn.remove_negatives(raw_data["level"])
    #interpolate the data
    interpolated_level_data = fn.interpolate_nan_data(raw_data["timestamp"], NaN_level_data)

    brewing_heater_power = fn.read_metadata(file_path, brewing+"/"+tank_id, "power_heater")
    brewing_heater_efficiency = fn.read_metadata(file_path, brewing+"/"+tank_id, "efficiency_heater")

    #power supplied by heating plate
    supplied_power = fn.calc_heater_heat_flux(brewing_heater_power, brewing_heater_efficiency)
    #initial internal energy
    initial_internal_energy = fn.calc_transported_power(brewing_mass_tank, brewing_specific_heat_capacity_tank, brewing_T_env)
    
    #filter sizes loop,  
    for i in filter_sizes:
        #filter temperature data
        processed_data["temperature_k_"+str(i)] = fn.filter_data(raw_data["temperature"],i)
        #filter interpolated level data
        processed_data["leve_k_"+str(i)] = fn.filter_data(interpolated_level_data, i)
        inner_energy = []
    
        converted_interpolated_level_data = processed_data["leve_k_"+str(i)].copy()

        for key,value in enumerate(converted_interpolated_level_data):
            #convert fill level from mm to m
            converted_interpolated_level_data[key] = value / 1000

        #mass of brew array over time
        mass_over_time = fn.calc_mass_flow(converted_interpolated_level_data, brewing_footprint_tank, brewing_density_beer)

    #time loop
    for key,value in enumerate(df_data["time"]):
        heat_waste = fn.calc_convective_heat_flow(brewing_heat_transfer_coeff_tank, brewing_surface_area_tank, raw_data["temperature"][key], brewing_T_env)

        #internal energy of beer assuming its temperature is identical to that of the tank
        energy_of_brew = fn.calc_transported_power(mass_over_time[key], brewing_specific_heat_capacity_beer, processed_data["temperature_k_"+str(i)][key])

        #total energy
        calculated_energy = supplied_power-heat_waste+energy_of_brew+initial_internal_energy
        inner_energy.append(calculated_energy)

    df_data["inner_energy_k_"+str(i)] = np.array(inner_energy)

    h5_path = "C:\\Users\ACER\Downloads\pa-ws2425\pa-ws2425\tests\data_GdD_plot_WS2425.h5"
    group_path = "energy_level"
    metadata = {
    "legend_title": "Energy level of Brew001, Tank001 over time",
    "x_label": "Time",
    "x_unit" : "seconds",
    "y_label": "Energy level",
    "y_unit" : "Joules"
    }

    fn.store_plot_data(df_data, h5_path, group_path, metadata) #store data

if __name__ == "__main__":
    main()
    