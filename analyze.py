__author__ = 'Tobin'

import json
import sys
import matplotlib.pyplot as plt

from characterization import *

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("Expected data file location")

    data_file = open(sys.argv[1], 'r')
    data = json.load(data_file)
    data_file.close()

    throat_area = data["throat_area"]
    density = data["density"]
    geometry = data["geometry"]
    times = [line[0] for line in data["time_pressure"]]
    pressures = [line[1] for line in data["time_pressure"]]
    mass = mass_from_geometry(geometry, density)
    area = area_from_geometry(geometry)

    c_star = characteristic_velocity(pressures, times, throat_area, mass)

    start, end = find_steady_state(pressures, threshold=0.7)

    plt.plot(times, pressures)
    plt.xlabel("Time")
    plt.ylabel("Pressure")
    plt.axvline(start, color='k')
    plt.axvline(end-1, color='k')
    plt.show()

    times = times[start:end]
    pressures = pressures[start:end]

    burn_rates = get_burn_rates(pressures, times, throat_area, density, area, c_star)

    print burn_rates
