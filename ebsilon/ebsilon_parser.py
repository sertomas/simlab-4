import logging
from win32com.client import Dispatch
from tabulate import tabulate

# Set up logging level
logging.basicConfig(level=logging.ERROR)

# Unit mapping dictionary based on the EpDimension class
unit_mapping = {
    0: "", 1: "", 2: "", 3: "bar", 4: "°C", 5: "kJ/kg", 6: "kg/s", 7: "kW", 8: "m³/kg", 9: "m³/s",
    12: "K", 13: "kmol/kmol", 14: "kg/kg", 15: "kW/K", 16: "W/m²K", 17: "1/min", 18: "kJ/kWh",
    21: "kJ/m³", 22: "kJ/m³K", 23: "kg/m³", 24: "m", 26: "kJ/kgK", 27: "m²", 28: "kJ/kgK", 29: "kg/kg",
    30: "kg/kg", 31: "kg/kmol", 32: "kJ/kg", 33: "m/s", 34: "kg/kg", 37: "mg/Nm³", 38: "EUR/h", 
    39: "kW/kg", 40: "1/m⁶", 41: "A", 42: "EUR/kWh", 43: "EUR/kg", 44: "V", 45: "m³/m³", 46: "kg", 
    47: "EUR", 48: "m³", 49: "ph", 51: "m²K/W", 52: "W/m²", 54: "°", 55: "kVA", 56: "kVAr", 57: "kg/ms", 
    58: "W/mK", 59: "m", 60: "1/°", 70: "s", 71: "K/m", 72: "kJ/kgm", 74: "kW/kgK", 75: "bar·m", 
    83: "kJ", 84: "Nm³/s", 85: "kg/m³K", 86: "kJ/kgK²", 98: "N", 99: "1/m", 100: "m²/W", 105: "kJ/mol"
}

# Define the class to handle Ebsilon model
class EbsilonModelParser:
    def __init__(self, model_path):
        self.model_path = model_path
        self.app = None
        self.model = None
        self.material_streams = []
        self.energy_streams = []

    def initialize_model(self):
        try:
            self.app = Dispatch("EbsOpen.Application")
            self.model = self.app.Open(self.model_path)
        except Exception as e:
            logging.error(f"Failed to initialize the model: {e}")
            raise

    def simulate_model(self):
        try:
            self.model.SimulateNew()
        except Exception as e:
            logging.error(f"Failed during simulation: {e}")
            raise

    def parse_model(self):
        """
        Parses all connections in the Ebsilon model to extract relevant data for material 
        and energy (power) streams, including units.
        """
        total_objects = self.model.Objects.Count
        for j in range(1, total_objects + 1):
            obj = self.model.Objects.Item(j)
            if obj.IsKindOf(16):  # If it's a connection
                pipe_cast = self.app.ObjectCaster.CastToPipe(obj)

                # Material stream attributes
                mass_flow = getattr(pipe_cast, 'M', None)
                temperature = getattr(pipe_cast, 'T', None)
                pressure = getattr(pipe_cast, 'P', None)
                enthalpy = getattr(pipe_cast, 'H', None)
                entropy = getattr(pipe_cast, 'S', None)

                # Check if it's a material or energy stream
                if pipe_cast.FluidType not in {0, 5, 6, 9, 10, 13, 14}:  # Material stream
                    self.material_streams.append({
                        'Name': pipe_cast.Name,
                        'Mass Flow': round(mass_flow.Value, 6) if mass_flow and mass_flow.Value else None,
                        'Temperature': round(temperature.Value, 6) if temperature and temperature.Value else None,
                        'Pressure': round(pressure.Value, 6) if pressure and pressure.Value else None,
                        'Enthalpy': round(enthalpy.Value, 6) if enthalpy and enthalpy.Value else None,
                        'Entropy': round(entropy.Value, 6) if entropy and entropy.Value else None,
                        'Mass Flow Unit': unit_mapping.get(mass_flow.Dimension, '') if mass_flow else '',
                        'Temperature Unit': unit_mapping.get(temperature.Dimension, '') if temperature else '',
                        'Pressure Unit': unit_mapping.get(pressure.Dimension, '') if pressure else '',
                        'Enthalpy Unit': unit_mapping.get(enthalpy.Dimension, '') if enthalpy else '',
                        'Entropy Unit': unit_mapping.get(entropy.Dimension, '') if entropy else '',
                    })
                elif pipe_cast.FluidType in {9, 10}:  # Energy stream (power flow)
                    power_flow = getattr(pipe_cast, 'Q', None)
                    self.energy_streams.append({
                        'Name': pipe_cast.Name,
                        'Power Flow': round(power_flow.Value, 6) if power_flow and power_flow.Value else None,
                        'Power Flow Unit': unit_mapping.get(power_flow.Dimension, '') if power_flow else '',
                    })

    def print_results(self):
        """
        Prints two tables: one for material streams and one for energy streams (power flows),
        with units included in the header row only.
        """
        # Retrieve units from the first entry in material_streams and energy_streams if available
        if self.material_streams:
            mass_flow_unit = self.material_streams[0]['Mass Flow Unit']
            temperature_unit = self.material_streams[0]['Temperature Unit']
            pressure_unit = self.material_streams[0]['Pressure Unit']
            enthalpy_unit = self.material_streams[0]['Enthalpy Unit']
            entropy_unit = self.material_streams[0]['Entropy Unit']
        else:
            mass_flow_unit = temperature_unit = pressure_unit = enthalpy_unit = entropy_unit = ""

        # Material streams table
        print("Material Streams:")
        material_headers = [
            "Connection",
            f"Mass Flow [{mass_flow_unit}]",
            f"Temperature [{temperature_unit}]",
            f"Pressure [{pressure_unit}]",
            f"Enthalpy [{enthalpy_unit}]",
            f"Entropy [{entropy_unit}]"
        ]
        material_rows = [
            [stream['Name'], stream['Mass Flow'], stream['Temperature'], stream['Pressure'],
             stream['Enthalpy'], stream['Entropy']]
            for stream in self.material_streams
        ]
        print(tabulate(material_rows, headers=material_headers, tablefmt="fancy_grid"))

        # Retrieve units from the first entry in energy_streams if available
        if self.energy_streams:
            power_flow_unit = self.energy_streams[0]['Power Flow Unit']
        else:
            power_flow_unit = ""

        # Energy streams table
        print("\nEnergy Streams (Power):")
        energy_headers = [
            "Connection",
            f"Power Flow [{power_flow_unit}]"
        ]
        energy_rows = [
            [stream['Name'], stream['Power Flow']]
            for stream in self.energy_streams
        ]
        print(tabulate(energy_rows, headers=energy_headers, tablefmt="fancy_grid"))

    def get_material_streams_data(self):
        """
        Returns the material streams data as a list of dictionaries, suitable for creating a DataFrame.
        """
        return self.material_streams

    def get_energy_streams_data(self):
        """
        Returns the energy streams (power flow) data as a list of dictionaries, suitable for creating a DataFrame.
        """
        return self.energy_streams

def run_ebsilon(model_path, print_results=True):
    parser = EbsilonModelParser(model_path)
    parser.initialize_model()
    parser.simulate_model()
    parser.parse_model()
    if print_results:
        parser.print_results()
    return parser.get_material_streams_data(), parser.get_energy_streams_data()
