import pandas as pd
from domain.dialogue_manager import DialogueManager, Message, Intent
from tqdm import tqdm

# Initialize the DialogueManager
dialogue_manager = DialogueManager()

# Read the CSV file, limiting to the first 5 rows
df = pd.read_csv("updated_customer_support_dataset.csv", nrows=5)

# Function to get predicted intent and thought process
def get_predictions(row):
    chat_history = [
        Message(role="user", content=row['instruction'])
    ]
    response = dialogue_manager.get_response(chat_history)
    return pd.Series({
        'predicted_intent': response.intent,
        'thought_process': response.thought_process_for_intent
    })

# Add predicted_intent and thought_process columns
tqdm.pandas(desc="Predicting intents")
df[['predicted_intent', 'thought_process']] = df.progress_apply(get_predictions, axis=1)

# Save the updated DataFrame to a new CSV file
df.to_csv("customer_support_dataset_with_predictions_sample.csv", index=False)

print("Predictions added and saved to customer_support_dataset_with_predictions_sample.csv")

# Function to extract just the intent name from the full enum string
def extract_intent_name(full_intent_string):
    return full_intent_string.split('.')[-1]

# Print some statistics
total_samples = len(df)
correct_predictions = (df['intent_enum'] == df['predicted_intent']).sum()
accuracy = correct_predictions / total_samples

print(f"\nTotal samples: {total_samples}")
print(f"Correct predictions: {correct_predictions}")
print(f"Accuracy: {accuracy:.2%}")

# Display all examples
print("\nAll predictions:")
print(df[['instruction', 'intent_enum', 'predicted_intent', 'thought_process']])
