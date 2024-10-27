import pandas as pd
from domain.dialogue_manager import Intent
import os
from add_predictions import get_predictions
from tqdm import tqdm

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

# Add a new column 'Ticket_Id' with unique identifiers
df['Ticket_Id'] = range(1, len(df) + 1)

# Create directories to store the chunks and predictions
os.makedirs("dataset_chunks", exist_ok=True)
os.makedirs("prediction_results", exist_ok=True)

# Separate the dataset into chunks of 1000 tickets each and run predictions
chunk_size = 1000
for i, chunk in enumerate(range(0, len(df), chunk_size)):
    chunk_df = df.iloc[chunk:chunk+chunk_size].copy()
    chunk_filename = f"dataset_chunks/customer_support_dataset_chunk_{i+1}.csv"
    chunk_df.to_csv(chunk_filename, index=False)
    print(f"Chunk {i+1} saved: {chunk_filename}")
    
    # Run predictions on the chunk
    tqdm.pandas(desc=f"Predicting intents for chunk {i+1}")
    chunk_df[['predicted_intent', 'thought_process']] = chunk_df.progress_apply(get_predictions, axis=1)
    
    # Update the original DataFrame with the predictions
    df.loc[chunk_df.index, ['predicted_intent', 'thought_process']] = chunk_df[['predicted_intent', 'thought_process']]
    
    # Save predictions to a CSV file
    predictions_filename = f"prediction_results/predictions_chunk_{i+1}.csv"
    chunk_df.to_csv(predictions_filename, index=False)
    print(f"Predictions for chunk {i+1} saved: {predictions_filename}")

print(f"Dataset separated into {i+1} chunks of {chunk_size} tickets each, and predictions completed.")

# Save the updated DataFrame to a new CSV file
df.to_csv("updated_customer_support_dataset_with_predictions.csv", index=False)
print("Updated CSV file with predictions saved successfully.")

# Read the newly created CSV file
new_df = pd.read_csv("updated_customer_support_dataset_with_predictions.csv")

# Debugging: Print information about the new DataFrame after reading
print("\nNew DataFrame after reading the updated CSV:")
print(f"Shape: {new_df.shape}")
print(new_df.head())
print(new_df.columns)
print(new_df['intent_enum'].unique())
print(new_df['Ticket_Id'].head())

print("Updated CSV file saved and read successfully.")
