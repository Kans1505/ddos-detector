import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.metrics import confusion_matrix, precision_score, recall_score
from sklearn.model_selection import train_test_split
import pickle

print("Loading features...")

features_df = pd.read_csv('features.csv')

print("Preparing data...")

X = features_df.drop('is_attack', axis=1)
y = features_df['is_attack']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("Training IsolationForest...")

model = IsolationForest(contamination=0.08, random_state=42)
model.fit(X_train_scaled)

print("✅ Model trained!")
print("\nTesting on new data...")

predictions = model.predict(X_test_scaled)
predictions_binary = (predictions == -1).astype(int)

print("\n=== RESULTS ===\n")

cm = confusion_matrix(y_test, predictions_binary)
tn, fp, fn, tp = cm.ravel()

print(f"✅ Caught attacks: {tp}")
print(f"❌ False alarms: {fp}")
print(f"⚠️  Missed attacks: {fn}")
print(f"✅ Correct normal: {tn}")

precision = tp / (tp + fp) if (tp + fp) > 0 else 0
print(f"\nPrecision: {precision:.1%}")

recall = tp / (tp + fn) if (tp + fn) > 0 else 0
print(f"Recall: {recall:.1%}")

pickle.dump(model, open('detector_model.pkl', 'wb'))
pickle.dump(scaler, open('scaler.pkl', 'wb'))

print("\n✅ Model saved!")