import pandas as pd

# Load the XSS dataset
xss_df = pd.read_csv('XSS_dataset.csv')

# Load the SQL injection dataset (assuming you have it in the same format)
sql_df = pd.read_csv('Modified_SQL_Dataset.csv')
'''
# Ensure that both DataFrames have the same column names
xss_df.columns = ['query', 'label']
sql_df.columns = ['query', 'label']

# Combine both DataFrames
combined_df = pd.concat([sql_df, xss_df], ignore_index=True)

# Save the combined dataset to a new CSV file
combined_df.to_csv('combined_attacks_data.csv', index=False)

print("Datasets combined and saved to 'combined_attacks_data.csv'")'''


sql_df['label'] = 1  # SQLi label
xss_df['label'] = 2   # XSS label

# Combine both DataFrames
combined_df = pd.concat([sql_df, xss_df], ignore_index=True)

# Save the combined dataset to a new CSV file
combined_df.to_csv('combined_attacks_data.csv', index=False)

print("Datasets combined and saved to 'combined_attacks_data.csv'")
