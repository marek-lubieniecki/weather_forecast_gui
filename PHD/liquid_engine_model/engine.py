import cantera as ct
import math
import numpy as np

class Engine:

    def __init__(self, thrust, combustion_pressure, thrust_time, oxidiser_fuel_ratio,
                 c_star_efficiency, thrust_coefficient_efficiency):
        self.thrust = thrust
        self.combustion_pressure = combustion_pressure
        self.thrust_time = thrust_time

        self.c_star_efficiency = c_star_efficiency
        self.thrust_coefficient_efficiency = thrust_coefficient_efficiency
        self.total_efficiency = self.c_star_efficiency * self.thrust_coefficient_efficiency

        self.heat_capacity_cv = 0
        self.heat_capacity_cp = 0
        self.heat_capacity_ratio = 1
        self.individual_gas_constant = 1
        self.universal_gas_constant = 8.31446261815324

        self.initial_temperature = 300
        self.combustion_temperature = 300
        self.mean_molecular_weight = 28.2

        self.oxidiser_fuel_ratio = 1

        self.equivalence_ratio = 1
        self.stoichiometric_of_ratio = 1
        self.nozzle_area_ratio = 1
        self.pressure_ratio = 1

        self.oxidiser = 'O2'
        self.fuel = 'C3H8'
        self.gas = ct.Solution('gri30.xml')


        self.gas.TP = self.initial_temperature, ct.one_atm*self.combustion_pressure/1e5
        #self.calculate_stoichiometric_of_ratio()

        self.exhaust_velocity = 0
        self.mass_flow = 0
        self.oxidiser_mass_flow = 0
        self.fuel_mass_flow = 0
        self.specific_impulse = 0

    def set_oxidiser_fuel_ratio(self, of_ratio):
        self.oxidiser_fuel_ratio = of_ratio
        self.equivalence_ratio = of_ratio / self.stoichiometric_of_ratio

    #def calculate_stoichiometric_of_ratio(self):
    ##    self.gas.set_equivalence_ratio(1, self.fuel, self.oxidiser)
     #   fuel = self.gas["C3H8"].Y[0]
     #   oxidiser = self.gas["O2"].Y[0]
     #   self.stoichiometric_of_ratio = oxidiser/fuel

    def calculate_combustion_chamber_properties(self):
        self.gas = ct.Solution('gri30.xml')
        nsp = self.gas.n_species
        iFu = self.gas.species_index(self.fuel)  # index of Fuel
        iOx = self.gas.species_index(self.oxidiser)  # index of Oxidize
        phi = self.oxidiser_fuel_ratio

        y = np.zeros(nsp)
        y[iFu] = 1.0  # we want mass fractions
        y[iOx] = phi

        self.gas.TP = 300.0, ct.one_atm * self.combustion_pressure/1e5
        self.gas.Y = y
        self.gas.equilibrate('HP', solver="gibbs")

        self.combustion_temperature = self.gas.T
        self.mean_molecular_weight = self.gas.mean_molecular_weight
        self.heat_capacity_cp = self.gas.cp
        self.heat_capacity_cv = self.gas.cv
        self.heat_capacity_ratio = self.gas.cp / self.gas.cv
        self.individual_gas_constant = self.universal_gas_constant/(self.gas.mean_molecular_weight/1e3)

    def calculate_area_ratio(self, atmospheric_pressure):
        self.pressure_ratio = atmospheric_pressure/self.combustion_pressure
        A = 2 * self.heat_capacity_ratio / (self.heat_capacity_ratio-1)
        B = math.pow(self.pressure_ratio, (2/self.heat_capacity_ratio))
        C = 1 - math.pow(self.pressure_ratio,(self.heat_capacity_ratio-1)/self.heat_capacity_ratio)
        self.nozzle_area_ratio = v_function(self.heat_capacity_ratio) / math.sqrt(A*B*C)

    def calculate_pressure_ratio(self):
        pass

    def calculate_exhaust_velocity(self):
        A = self.heat_capacity_ratio/(self.heat_capacity_ratio-1)
        B = 1 - math.pow(self.pressure_ratio, (self.heat_capacity_ratio-1)/self.heat_capacity_ratio)
        self.exhaust_velocity = math.sqrt(2*A*self.individual_gas_constant*self.combustion_temperature*B)

    def calculate_isp(self, atmospheric_pressure):
        self.specific_impulse = self.exhaust_velocity/9.81

    def print_engine_properties(self):
        print("Combustion pressure: ", self.combustion_pressure)
        print("Combustion temperature: ", self.combustion_temperature)
        print("Heat capacity ratio: ", self.heat_capacity_ratio)
        print("Mean molecular weight: ", self.gas.mean_molecular_weight)
        print("Individual gas constant: ", self.individual_gas_constant)
        print("Pressure ratio: ", self.pressure_ratio)
        print("Area ratio : ", self.nozzle_area_ratio)
        print("Exhaust velocity: ", self.exhaust_velocity)
        print("Ideal specific impulse: ", self.specific_impulse)

    def update_performance(self, atmospheric_pressure):
        self.calculate_combustion_chamber_properties()
        self.calculate_area_ratio(atmospheric_pressure)
        self.calculate_exhaust_velocity()
        self.calculate_isp(atmospheric_pressure)

def v_function(specific_heat_ratio):
    value = math.sqrt(specific_heat_ratio) * math.pow((2/(specific_heat_ratio+1)), ((specific_heat_ratio+1)/(2*(specific_heat_ratio-1))))
    return value
