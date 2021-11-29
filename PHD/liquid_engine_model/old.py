from engine import *
from atmosphere import *
import cantera as ct
import numpy as np
import matplotlib.pyplot as plt


species = {S.name: S for S in ct.Species.listFromFile('gri30.cti')}

liquid_engine = Engine(
    thrust=30e3,
    combustion_pressure=50e5,
    thrust_time=120,
    oxidiser_fuel_ratio=3,
    c_star_efficiency=0.95,
    thrust_coefficient_efficiency=0.97
)

atmosphere = StandardAtmosphere(0)

liquid_engine.calculate_combustion_chamber_properties()
liquid_engine.calculate_area_ratio(atmosphere.pressure)
liquid_engine.calculate_exhaust_velocity()
liquid_engine.calculate_isp(atmosphere.pressure)
liquid_engine.print_engine_properties()


pressures = np.arange(10, 20, 10)
of_ratios = np.arange(1, 6.5, 0.25)
temperatures = np.empty([pressures.size, of_ratios.size])
specific_impulses = np.empty([pressures.size, of_ratios.size])
mean_weights = np.empty([pressures.size, of_ratios.size])


for pressure_id, pressure in enumerate(pressures):
    for of_ratio_id, of_ratio in enumerate(of_ratios):
        liquid_engine.combustion_pressure = pressure*1e5
        liquid_engine.set_oxidiser_fuel_ratio(of_ratio)
        liquid_engine.update_performance(atmosphere.pressure)
        temperatures[pressure_id, of_ratio_id] = liquid_engine.combustion_temperature
        specific_impulses[pressure_id, of_ratio_id] = liquid_engine.specific_impulse
        mean_weights[pressure_id, of_ratio_id] = liquid_engine.mean_molecular_weight
        liquid_engine.print_engine_properties()
        #print("Combustion pressure: ", pressure, "OF ratio:", of_ratio, "Equivalence ratio: ", liquid_engine.equivalence_ratio)


fig, ax = plt.subplots()  # Create a figure and an axes.
for pressure_id, pressure in enumerate(pressures):
   ax.plot(of_ratios, temperatures[pressure_id, :], label = pressure)  # Matplotlib plo
ax.set_xlabel('x label')  # Add an x-label to the axes.
ax.set_ylabel('y label')  # Add a y-label to the axes.
ax.set_title("Simple Plot")  # Add a title to the axes.
ax.legend()  # Add a legend.

fig, ax1 = plt.subplots()  # Create a figure and an axes.
for pressure_id, pressure in enumerate(pressures):
   ax1.plot(of_ratios, specific_impulses[pressure_id, :], label = pressure)  # Matplotlib plo
ax1.set_xlabel('x label')  # Add an x-label to the axes.
ax1.set_ylabel('y label')  # Add a y-label to the axes.
ax1.set_title("Simple Plot")  # Add a title to the axes.
ax1.legend()  # Add a legend.

fig, ax2 = plt.subplots()  # Create a figure and an axes.
for pressure_id, pressure in enumerate(pressures):
   ax2.plot(of_ratios, mean_weights[pressure_id, :], label = pressure)  # Matplotlib plo
ax2.set_xlabel('x label')  # Add an x-label to the axes.
ax2.set_ylabel('y label')  # Add a y-label to the axes.
ax2.set_title("Simple Plot")  # Add a title to the axes.
ax2.legend()  # Add a legend.

plt.show()