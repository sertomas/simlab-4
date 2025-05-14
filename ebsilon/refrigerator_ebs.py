import os 
import pandas as pd
from ebsilon_parser import run_ebsilon

# Define the path to the Ebsilon model file
model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'refrigerator.ebs'))

# You can alternatively access to the results as dictionaries and create DataFrames:
material_stream, energy_streams = run_ebsilon(model_path, print_results=False)
df_material_streams = pd.DataFrame(material_stream)
df_energy_streams = pd.DataFrame(energy_streams)
df_material_streams.to_csv('ebsilon/ebs_material_streams_results.csv')
df_energy_streams.to_csv('ebsilon/ebs_energy_streams_results.csv')