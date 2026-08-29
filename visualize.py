import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import pickle

print("Loading data...")

# Load
features = pd.read_csv('features.csv')
model = pickle.load(open('detector_model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))

print("Making predictions...")

# Predict
X = features.drop('is_attack', axis=1)
X_scaled = scaler.transform(X)
predictions = model.predict(X_scaled)

print("Creating visualization...")

# Make 2 plots
fig, axes = plt.subplots(2, 1, figsize=(14, 8))

# Plot 1: Visitors over time
axes[0].plot(features['avg_visitors'], label='Visitors/sec', color='blue', linewidth=2)
attack_indices = features[predictions == -1].index
axes[0].scatter(attack_indices, features.loc[attack_indices, 'avg_visitors'], 
               color='red', s=100, label='🚨 Attack Detected', zorder=5)
axes[0].set_title('Website Visitors Over Time', fontsize=14, fontweight='bold')
axes[0].set_ylabel('Visitors/sec', fontsize=12)
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Plot 2: Unique computers
axes[1].plot(features['avg_computers'], label='Unique Computers', color='green', linewidth=2)
axes[1].scatter(attack_indices, features.loc[attack_indices, 'avg_computers'],
               color='red', s=100, label='🚨 Attack Detected', zorder=5)
axes[1].set_title('Unique Computers Connecting Over Time', fontsize=14, fontweight='bold')
axes[1].set_ylabel('Computers', fontsize=12)
axes[1].set_xlabel('Time Window (30-sec chunks)', fontsize=12)
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('ddos_detection_report.png', dpi=150)
print("✅ Saved ddos_detection_report.png")
plt.show()