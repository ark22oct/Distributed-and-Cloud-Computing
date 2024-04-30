# dataset_creation.py

import pandas as pd
import numpy as np
import random
import csv

# Define the range of values for each feature
locations = ["New York City, US", "Tokyo, JP", "London, UK", "Los Angeles, US", "Cairo, EG", "Paris, FR"]
distances = np.random.randint(100, 5000, size=(1000,))
urgency_levels = ['High', 'Medium', 'Low']
transportation_methods = ['Ship', 'Train', 'Plane']

# Create a list to store the data
data = []

# Generate random data for the dataset
for _ in range(1000):
    start_location = random.choice(locations)
    end_location = random.choice(locations)
    distance = random.choice(distances)
    urgency = random.choice(urgency_levels)
    transportation_method = random.choice(transportation_methods)
    
    # Calculate transportation cost based on distance and urgency
    if urgency == 'High':
        transportation_cost = distance * 0.05
    elif urgency == 'Medium':
        transportation_cost = distance * 0.03
    else:
        transportation_cost = distance * 0.02
    
    # Generate random values for fuel efficiency and emissions
    fuel_efficiency = random.uniform(0.1, 0.5)
    emissions = random.uniform(50, 500)
    
    # Generate a unique order ID
    order_id = 'ORD' + str(_ + 1000)
    
    # Append the data to the list
    data.append([order_id, start_location, end_location, distance, urgency, transportation_method,
                 transportation_cost, fuel_efficiency, emissions])

# Create a DataFrame from the list of data
df = pd.DataFrame(data, columns=['Order ID', 'Start Location', 'End Location', 'Distance (km)', 'Urgency',
                                 'Transportation Method', 'Transportation Cost ($)', 'Fuel Efficiency (km/l)',
                                 'Emissions (gCO2/km)'])

# Save the DataFrame to a CSV file
df.to_csv('transportation_dataset.csv', index=False)

print("Dataset created successfully.")