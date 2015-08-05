__author__ = 'Tobin'

import math


def find_steady_state(pressures, threshold=0.8):
    # for now use 80% of peak pressure. This is probably ok for most Bates grains, not sure about other geometries
    steady_state_threshold = max(pressures) * threshold
    start = 0
    best_start = 0
    best_end = -1
    good_region = False
    for i in range(len(pressures)):
        if pressures[i] >= steady_state_threshold and not good_region:
            start = i
            good_region = True
        if pressures[i] < steady_state_threshold and good_region:
            good_region = False
            if i-start > best_end-best_start:
                best_start = start
                best_end = i

    return best_start, best_end


def area_from_geometry(geometry):
    if geometry["type"] == "bates":
        return bates_area(**geometry["parameters"])
    else:
        raise KeyError("Unknown geometry: %s" % geometry["type"])


def mass_from_geometry(geometry, density):
    if geometry["type"] == "bates":
        return bates_mass(density=density, **geometry["parameters"])
    else:
        raise KeyError("Unknown geometry: %s" % geometry["type"])


def bates_mass(length, core_diameter, diameter, number, density):
    return density * number * length * math.pi * (diameter**2 - core_diameter**2) / 4.0


def bates_area(length, core_diameter, diameter, number):
    def area(s):
        if s > length or s > ((diameter - core_diameter) / 2.0):
            # all propellant has burned
            return 0
        else:
            return (length - s) * math.pi * (core_diameter + s*2) * number
    return area


def characteristic_velocity(pressures, times, throat_area, mass):
    return throat_area / mass * sum((p+next_p)/2.0 * (next_t-t)
                                    for p, next_p, t, next_t
                                    in zip(pressures, pressures[1:], times, times[1:]))


def get_burn_rates(pressures, times, throat_area, density, area, c_star, s0=0):
    # ds/dt = P(t) / (Kn rho c*)
    # Kn = throat / area(s)
    burn_rates = list()
    s = s0
    for (p, t, next_t) in zip(pressures, times, times[1:]):
        rate = p * area(s) / (throat_area * density * c_star)
        s += rate * (next_t - t)
        burn_rates.append(rate)
    return burn_rates
