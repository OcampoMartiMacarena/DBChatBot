import pandas as pd
from domain.dialogue_manager import DialogueManager, Message
import time
import numpy as np

# Initialize the DialogueManager
dialogue_manager = DialogueManager()

def process_chunk(chunk_df):
    # Prepare the chat history for all 1000 tickets
    chat_history = []
    for _, row in chunk_df.iterrows():
        chat_history.extend([
            Message(role="user", content=row['instruction']),
            Message(role="assistant", content=row['response'])
        ])
    
    # Get predictions for all 1000 tickets in one go
    response = dialogue_manager.get_response(chat_history)
    
    # Process the response
    # Assuming the response contains a single intent and thought process for the entire batch
    return pd.DataFrame({
        'predicted_intent': [response.intent] * len(chunk_df),
        'thought_process': [response.thought_process_for_intent] * len(chunk_df)
    })

# Read the CSV file
df = pd.read_csv("hf://datasets/bitext/Bitext-customer-support-llm-chatbot-training-dataset/Bitext_Sample_Customer_Support_Training_Dataset_27K_responses-v11.csv")

# Print DataFrame info for debugging
print("DataFrame columns:")
print(df.columns)
print("\nFirst few rows:")
print(df.head())

# Shuffle the entire dataset
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Process one chunk of 1000 tickets
chunk_size = 1000
chunk = df.iloc[:chunk_size].copy()

print(f"Processing chunk of {chunk_size} tickets")
start_time = time.time()
results = process_chunk(chunk)
end_time = time.time()

print(f"Processing completed in {end_time - start_time:.2f} seconds")

# Merge results with original chunk
chunk[['predicted_intent', 'thought_process']] = results

# Save the updated chunk to a new CSV file
chunk.to_csv("updated_customer_support_dataset_with_predictions_1k_shuffled.csv", index=False)
print("Updated CSV file with predictions saved successfully.")

# Print some statistics
total_samples = len(chunk)
correct_predictions = (chunk['intent'] == chunk['predicted_intent']).sum()
accuracy = correct_predictions / total_samples

print(f"\nTotal samples: {total_samples}")
print(f"Correct predictions: {correct_predictions}")
print(f"Accuracy: {accuracy:.2%}")

# Display first few predictions
print("\nFirst few predictions:")
print(chunk[['instruction', 'intent', 'predicted_intent', 'thought_process']].head(10))

# Function to extract just the intent name from the full enum string
def extract_intent_name(full_intent_string):
    return full_intent_string.split('.')[-1]

# Print distribution of intents in the original dataset and the processed chunk
print("\nIntent distribution in original dataset:")
print(df['intent'].value_counts(normalize=True).head())

print("\nIntent distribution in processed chunk:")
print(chunk['intent'].value_counts(normalize=True).head())
