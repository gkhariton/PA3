import datetime
import os




def main():
    pass
file_path = os.path.join("project", "data", "data_GdD_Datensatz_WS2425.h5")
brewing = "brewing_001"
tank_id = "B001"

print("HDF5 File Path:", file_path)
print("Brewing Process ID:", brewing)
print("Tank ID:", tank_id)


if __name__ == "__main__":
    main()