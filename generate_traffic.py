import pandas as pd
import numpy as np

print("Creating normal traffic...")

# Normal traffic (no attack) = 1 hour = 3600 seconds
normal_data = []

for second in range(3600):
    # Normal: ~100 visitors per second (± 10)
    visitors = int(np.random.normal(100, 10))
    
    # Normal: ~50 different computers
    unique_computers = np.random.randint(40, 60)
    
    # Each visitor = ~5KB
    data_sent = visitors * 5000
    
    # 0 = normal, 1 = attack
    is_attack = 0
    
    normal_data.append({
        'second': second,
        'visitors_per_second': visitors,
        'unique_computers': unique_computers,
        'data_sent': data_sent,
        'is_attack': is_attack
    })

# Convert to table
traffic_df = pd.DataFrame(normal_data)

print("Adding attack at 30-minute mark...")

# Inject attack at second 1800 (30 minutes in), lasts 5 minutes
attack_start = 1800
attack_length = 300

for second in range(attack_start, attack_start + attack_length):
    traffic_df.loc[second, 'visitors_per_second'] = np.random.randint(5000, 10000)
    traffic_df.loc[second, 'unique_computers'] = np.random.randint(10000, 20000)
    traffic_df.loc[second, 'data_sent'] *= np.random.randint(50, 100)
    traffic_df.loc[second, 'is_attack'] = 1

# Save
traffic_df.to_csv('traffic_data.csv', index=False)
print("✅ Created traffic_data.csv")
print("\nFirst 5 rows:")
print(traffic_df.head())
print("\nAttack rows:")
print(traffic_df[traffic_df['is_attack'] == 1].head())