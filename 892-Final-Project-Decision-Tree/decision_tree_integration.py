# decision_tree_integration.py

import joblib
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

# Load the dataset
dataset = pd.read_csv('transportation_dataset.csv')

# Preprocess the data
# Separate features (X) and target variable (y)
X = dataset.drop(['Order ID', 'Transportation Cost ($)'], axis=1)
y = dataset['Transportation Cost ($)']

# Define the columns to be one-hot encoded
categorical_features = ['Start Location', 'End Location', 'Urgency', 'Transportation Method']

# Apply one-hot encoding to categorical features
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(), categorical_features)],
    remainder='passthrough')

X_encoded = preprocessor.fit_transform(X)

# Train the decision tree model
model = DecisionTreeRegressor()
model.fit(X_encoded, y)

# Visualize the decision tree
plt.figure(figsize=(20, 10))
plot_tree(model, feature_names=preprocessor.get_feature_names_out(), filled=True, fontsize=10)
plt.savefig('decision_tree.png')
plt.show()

# Save the trained model
joblib.dump(model, 'decision_tree_model.joblib')

print("Decision Tree Integration completed.")


