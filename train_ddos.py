import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load the DDoS dataset
ddos_data = pd.read_csv('APA-DDoS-Dataset.csv', low_memory=False)  # Update with your actual CSV file path

# Check for mixed types and NaN values
print("Data types in the dataset:")
print(ddos_data.dtypes)  # View data types of each column
print("\nCount of NaN values in each column:")
print(ddos_data.isna().sum())  # Count of NaN values in each column

# Handle NaN values (fill or drop)
ddos_data.fillna(0, inplace=True)  # Fill NaN values with 0

# Display the first few rows of the dataset for inspection
print("\nFirst few rows of the dataset:")
print(ddos_data.head())

# Preprocess the dataset
# Convert categorical features to numerical values using Label Encoding
le_src_ip = LabelEncoder()
le_dst_ip = LabelEncoder()
le_label = LabelEncoder()

ddos_data['ip.src'] = le_src_ip.fit_transform(ddos_data['ip.src'].astype(str))  # Ensure IPs are strings
ddos_data['ip.dst'] = le_dst_ip.fit_transform(ddos_data['ip.dst'].astype(str))  # Ensure IPs are strings
ddos_data['Label'] = le_label.fit_transform(ddos_data['Label'].astype(str))  # Ensure labels are strings

# Select features and labels
features = ddos_data[['ip.src', 'ip.dst', 'tcp.srcport', 'tcp.dstport', 
                       'ip.proto', 'tcp.flags.syn', 'tcp.flags.reset', 
                       'tcp.flags.push', 'tcp.flags.ack', 
                       'ip.flags.mf', 'ip.flags.df', 'ip.flags.rb', 
                       'tcp.seq', 'tcp.ack', 'Packets', 'Bytes']]

labels = ddos_data['Label']

# Check for NaN values again after encoding
print("\nCount of NaN values in each column after encoding:")
print(features.isna().sum())  # Check if there are any NaN values left

# Ensure features are numeric (if necessary)
features = features.apply(pd.to_numeric, errors='coerce')

# Drop any rows with NaN values again after conversion
features.dropna(inplace=True)
labels = labels[features.index]  # Align labels with modified features

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# Train the SVM model
svm_ddos_model = SVC(kernel='linear')  # You can change the kernel as needed
svm_ddos_model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = svm_ddos_model.predict(X_test)

# Evaluate the model
print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Save the model and label encoders
joblib.dump(svm_ddos_model, 'svm_ddos_model.pkl')
joblib.dump(le_src_ip, 'le_src_ip.pkl')
joblib.dump(le_dst_ip, 'le_dst_ip.pkl')
joblib.dump(le_label, 'le_label.pkl')
