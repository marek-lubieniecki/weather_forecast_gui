import cantera as ct


class Engine:
    combustion_temperature = 300
    mean_molecular_weight =
    def __init__(self, thrust, combustion_pressure, thrust_time, oxidiser_fuel_ratio, nozzle_area_ratio,
                 c_star_efficiency, thrust_coefficient_efficiency):
        self.thrust = thrust
        self.combustion_pressure = combustion_pressure
        self.thrust_time = thrust_time
        self.oxidiser_fuel_ratio = oxidiser_fuel_ratio
        self.nozzle_area_ratio = nozzle_area_ratio
        self.c_star_efficiency = c_star_efficiency
        self.thrust_coefficient_efficiency = thrust_coefficient_efficiency

        self.oxidiser = 'O2'
        self.fuel = 'C3H8'

    def calculate_combustion_chamber_properties(self):
        temperature_initial = 300
        combustion_pressure = 50e5
        oxidiser_fuel_ratio = 3

        oxidiser = 'O2'
        fuel = 'C3H8'

        gas = ct.Solution('gri30.xml')
        gas()

        gas.TP = temperature_initial, combustion_pressure
        gas.set_equivalence_ratio(1, fuel, oxidiser)
        Z = gas["C3H8"].Y[0]

        print(Z)
        gas()

        gas.equilibrate('HP')

        gas()

        print(gas.T)
        print(gas.M)

        self.combustion_temperature = gas.T

    def calculate_isp(self):
        pass