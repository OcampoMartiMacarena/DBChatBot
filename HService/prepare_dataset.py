import pandas as pd
from domain.dialogue_manager import Intent

# Read the CSV file
df = pd.read_csv("hf://datasets/bitext/Bitext-customer-support-llm-chatbot-training-dataset/Bitext_Sample_Customer_Support_Training_Dataset_27K_responses-v11.csv")

# Debugging: Print information about the DataFrame after reading
print("DataFrame after reading:")
print(f"Shape: {df.shape}")
print(df.head())
print(df.columns)
print(df['intent'].unique())

# Create a mapping dictionary from string to Intent enum
intent_mapping = {intent.name: intent for intent in Intent}

# Add a new column 'intent_enum' with the Intent Enum values
df['intent_enum'] = df['intent'].map(intent_mapping)

# Save the updated DataFrame to a new CSV file
df.to_csv("updated_customer_support_dataset.csv", index=False)

# Read the newly created CSV file
new_df = pd.read_csv("updated_customer_support_dataset.csv")

# Debugging: Print information about the new DataFrame after reading
print("\nNew DataFrame after reading the updated CSV:")
print(f"Shape: {new_df.shape}")
print(new_df.head())
print(new_df.columns)
print(new_df['intent_enum'].unique())

print("Updated CSV file saved and read successfully.")
