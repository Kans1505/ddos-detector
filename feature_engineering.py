import pandas as pd
import numpy as np

print("Loading traffic data...")

# Load the CSV you just created
traffic = pd.read_csv('traffic_data.csv')

print("Creating features from 30-second windows...")

# We'll look at EVERY 30-second chunk and ask smart questions
features_list = []

window_size = 30  # Look at 30 seconds at a time

for i in range(len(traffic) - window_size):
    # Get 30 seconds of data
    window = traffic.iloc[i : i + window_size]
    
    # Question 1: Average visitors in this 30-sec window?
    avg_visitors = window['visitors_per_second'].mean()
    
    # Question 2: Did visitors jump around? (max - min)
    visitor_change = window['visitors_per_second'].max() - window['visitors_per_second'].min()
    
    # Question 3: Average unique computers in this window?
    avg_computers = window['unique_computers'].mean()
    
    # Question 4: Did new computers suddenly connect?
    computer_growth = window['unique_computers'].iloc[-1] - window['unique_computers'].iloc[0]
    
    # Question 5: Average data sent?
    avg_data = window['data_sent'].mean()
    
    # Question 6: Is there an attack in this window?
    is_attack = window['is_attack'].iloc[-1]
    
    # Store all answers
    features_list.append({
        'avg_visitors': avg_visitors,
        'visitor_change': visitor_change,
        'avg_computers': avg_computers,
        'computer_growth': computer_growth,
        'avg_data': avg_data,
        'is_attack': is_attack
    })

# Turn into table
features_df = pd.DataFrame(features_list)

# Save
features_df.to_csv('features.csv', index=False)
print("✅ Created features.csv")
print("\nFirst 10 rows:")
print(features_df.head(10))
print("\nAttack rows:")
print(features_df[features_df['is_attack'] == 1].head())