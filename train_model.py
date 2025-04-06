import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Load the combined gesture data
data = pd.read_csv("gesture_data.csv")

# Separate features and labels
X = data.drop("label", axis=1)  # all columns except 'label'
y = data["label"]               # only the 'label' column

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")

# Save the trained model
joblib.dump(model, "gesture_model.pkl")
print("Model saved as gesture_model.pkl")
