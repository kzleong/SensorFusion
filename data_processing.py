import pandas as pd
import re

# Load the CSV file
file_path = 'history.csv'  # Replace with your actual file path
data = pd.read_csv(file_path)


def clean_last_changed(value):
    return re.sub(r'\.\d+Z$', '', value)

# Apply the function to the column
data['last_changed'] = data['last_changed'].apply(clean_last_changed)

# Filter for the specific entity_id
filtered_data = data[data['entity_id'] == 'sensor.device_f0f5bd06f5a0_sound']

# Ensure 'state' is treated as a numeric column for aggregation
filtered_data['state'] = pd.to_numeric(filtered_data['state'], errors='coerce')

# Group by 'last_changed' and calculate the mean for duplicate timestamps
mean_states = (
    filtered_data.groupby('last_changed', as_index=False)
    .agg({'state': 'mean'})
)

# Merge the mean states back into the original dataset
# Drop the original rows for sensor.device_f0f5bd06f5a0_sound
data = data[data['entity_id'] != 'sensor.device_f0f5bd06f5a0_sound']

# Add the updated rows with mean states
mean_states['entity_id'] = 'sensor.device_f0f5bd06f5a0_sound'  # Add back the entity_id
data = pd.concat([data, mean_states], ignore_index=True)

processed_history = data.pivot_table(
    index='last_changed',
    columns='entity_id',
    values='state'
)

# Forward fill missing values for each entity_id
processed_history.ffill(inplace=True)

# Reset index to make last_changed a column again
processed_history.reset_index(inplace=True)

processed_history = processed_history[processed_history['last_changed'] >= '2024-12-13T17:42:39']

# Save the result to a new CSV
output_path = 'processed_history.csv'  # Replace with your desired output path
processed_history.to_csv(output_path, index=False)

print(f"The data has been arranged and saved to {output_path}")

