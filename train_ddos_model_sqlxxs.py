'''import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import joblib

# Load the dataset
data = pd.read_csv('Modified_SQL_Dataset.csv')

# Feature extraction: Count special characters and keywords
data['special_chars_count'] = data['query'].apply(lambda x: sum([1 for char in x if char in ['\'', ';', '--', '/*', '*/', '@@']]))
data['keyword_count'] = data['query'].apply(lambda x: len([kw for kw in ['SELECT', 'INSERT', 'DELETE', 'DROP', 'UPDATE', 'UNION', 'OR', 'AND'] if kw in x.upper()]))

# Features and labels
X = data[['special_chars_count', 'keyword_count']]
y = data['label']

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the SVM model
model = SVC(kernel='linear')
model.fit(X_train, y_train)

# Evaluate the model
predictions = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, predictions))

# Save the model
joblib.dump(model, 'svm_model.pkl')
'''
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report
import joblib

# Load the dataset
dataset_path = "combined_attacks_data.csv"  # Update this with your actual dataset path
data = pd.read_csv(dataset_path)

# Prepare features and labels
X = data['query']
y = data['label']

# Convert text data to feature vectors using TF-IDF
from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer()
X_vectorized = vectorizer.fit_transform(X)

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X_vectorized, y, test_size=0.2, random_state=42)

# Train the SVM model
model = SVC(kernel='linear', probability=True)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save the model and vectorizer
joblib.dump(model, 'svm_model.pkl')
joblib.dump(vectorizer, 'tfidf_vectorizer.pkl')
