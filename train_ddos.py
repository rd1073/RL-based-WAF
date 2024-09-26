import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, accuracy_score
from sklearn.impute import SimpleImputer
import joblib

# Load the DDoS dataset
ddos_data = pd.read_csv('APA-DDoS-Dataset.csv', low_memory=False)

# Check for mixed types and NaN values
print("Data types in the dataset:")
print(ddos_data.dtypes)
print("\nCount of NaN values in each column:")
print(ddos_data.isna().sum())

# Handle NaN values (impute with mean)
imputer = SimpleImputer(strategy='mean')
ddos_data.fillna(0, inplace=True)  # Fill NaN values with 0, can be changed based on context

# Preprocess the dataset
le_src_ip = LabelEncoder()
le_dst_ip = LabelEncoder()
le_label = LabelEncoder()

ddos_data['ip.src'] = le_src_ip.fit_transform(ddos_data['ip.src'].astype(str))
ddos_data['ip.dst'] = le_dst_ip.fit_transform(ddos_data['ip.dst'].astype(str))
ddos_data['Label'] = le_label.fit_transform(ddos_data['Label'].astype(str))

# Select features and labels
features = ddos_data[['ip.src', 'ip.dst', 'tcp.srcport', 'tcp.dstport', 
                       'ip.proto', 'tcp.flags.syn', 'tcp.flags.reset', 
                       'tcp.flags.push', 'tcp.flags.ack', 
                       'ip.flags.mf', 'ip.flags.df', 'ip.flags.rb', 
                       'tcp.seq', 'tcp.ack', 'Packets', 'Bytes']]

labels = ddos_data['Label']

# Ensure features are numeric (if necessary)
features = features.apply(pd.to_numeric, errors='coerce')

# Drop any rows with NaN values again after conversion
features.dropna(inplace=True)
labels = labels[features.index]  # Align labels with modified features

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train the SVM model
svm_ddos_model = SVC(kernel='linear')  # Change kernel as necessary
svm_ddos_model.fit(X_train, y_train)

# Evaluate using cross-validation
cv_scores = cross_val_score(svm_ddos_model, X_train, y_train, cv=5)
print(f"Cross-validated accuracy: {np.mean(cv_scores):.2f}")

# Make predictions on the test set
y_pred = svm_ddos_model.predict(X_test)

# Evaluate the model
print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Save the model and label encoders
joblib.dump(svm_ddos_model, 'svm_ddos_model.pkl')
joblib.dump(scaler, 'scaler.pkl')  # Save the scaler for future use
joblib.dump(le_src_ip, 'le_src_ip.pkl')
joblib.dump(le_dst_ip, 'le_dst_ip.pkl')
joblib.dump(le_label, 'le_label.pkl')
