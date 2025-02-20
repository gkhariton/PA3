import datetime
import os

import numpy as np
import project.functions as fn

def main():
    file_path = os.path.join("project", "data", "data_GdD_Datensatz_WS2425.h5")
    brewing = "brewing_001"
    tank_id = "B001"

    measured_quantities = (
        "level", 
        "temperature", 
        "timestamp"
        )

    brewing_T_env = fn.read_metadata(file_path, brewing, "T_env")
    brewing_specific_heat_capacity_beer = fn.read_metadata(file_path, brewing, "specific_heat_capacity_beer")
    brewing_density_beer = fn.read_metadata(file_path, brewing, "density_beer")

    brewing_mass_tank = fn.read_metadata(file_path, brewing+"/"+tank_id, "mass_tank")
    brewing_surface_area_tank = fn.read_metadata(file_path, brewing+"/"+tank_id, "surface_area_tank")
    brewing_footprint_tank = fn.read_metadata(file_path, brewing+"/"+tank_id, "footprint_tank")
    brewing_heat_transfer_coeff_tank = fn.read_metadata(file_path, brewing+"/"+tank_id, "heat_transfer_coeff_tank")
    brewing_specific_heat_capacity_tank = fn.read_metadata(file_path, brewing+"/"+tank_id, "specific_heat_capacity_tank")

if __name__ == "__main__":
    main()