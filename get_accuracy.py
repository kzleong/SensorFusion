import pandas as pd

# Load the CSV file
file_path = 'sensor_dataset.csv'  # Replace with your actual file path
data = pd.read_csv(file_path)

# Ensure 'occupancy' and 'radar_sensor' columns are numeric
data['occupancy'] = pd.to_numeric(data['occupancy'], errors='coerce')
data['radar_sensor'] = pd.to_numeric(data['radar_sensor'], errors='coerce')

# Drop rows where either column has missing values
data = data.dropna(subset=['occupancy', 'radar_sensor'])

# Calculate the number of correct predictions
correct_predictions = (data['radar_sensor'] == data['occupancy']).sum()

# Calculate the total number of predictions
total_predictions = len(data)

# Compute accuracy
accuracy = (correct_predictions / total_predictions) * 100

print(f"Accuracy of radar_sensor compared to ground truth: {accuracy:.2f}%")
print(total_predictions)
print(correct_predictions)
