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

    #1f, create a dictionary
    df_data={}

if __name__ == "__main__":
    main()