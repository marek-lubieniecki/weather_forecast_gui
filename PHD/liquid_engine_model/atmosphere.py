class StandardAtmosphere:

    def __init__(self, altitude):
        self.altitude = altitude
        self.pressure = self.calculate_pressure()
        self.temperature = self.calculate_temperature()

    def calculate_pressure(self):
        self.pressure = 1e5
        return self.pressure

    def calculate_temperature(self):
        self.temperature = 293
        return self.temperature

