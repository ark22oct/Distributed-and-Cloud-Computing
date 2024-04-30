import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, classification_report
import joblib
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv('transportation_dataset.csv')

# Drop the 'Order ID' column
data = data.drop(columns=['Order ID'])

# Perform one-hot encoding for categorical variables
data_encoded = pd.get_dummies(data, columns=['Start Location', 'End Location', 'Urgency'])

# Separate features (X) and target variable (y)
X = data_encoded.drop(['Transportation Method'], axis=1)  # Features
y = data_encoded['Transportation Method']  # Target variable

# Split the dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the decision tree classifier
clf = DecisionTreeClassifier(random_state=42)

# Define hyperparameters to tune
param_grid = {
    'max_depth': [3, 5, 7, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# Perform grid search to find the best hyperparameters
grid_search = GridSearchCV(estimator=clf, param_grid=param_grid, cv=5)
grid_search.fit(X_train, y_train)

# Get the best hyperparameters
best_params = grid_search.best_params_

# Initialize the decision tree classifier with the best hyperparameters
clf = DecisionTreeClassifier(**best_params, random_state=42)

# Train the decision tree classifier
clf.fit(X_train, y_train)

# Save the trained model
joblib.dump(clf, 'decision_tree_model.joblib')

# Save the column names used during training
joblib.dump(X.columns.tolist(), 'column_names.joblib')

print("Decision tree model trained and saved successfully.")
