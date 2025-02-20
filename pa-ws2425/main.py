import datetime
import os

import numpy as np
import project.functions as fn

def main():
    pass

file_path = os.path.join("project", "data", "data_GdD_Datensatz_WS2425.h5")
brewing = "brewing_001"
tank_id = "B001"

measured_quantities = ("level", "temperature", "timestamp")

read_metadata()

if __name__ == "__main__":
    main()