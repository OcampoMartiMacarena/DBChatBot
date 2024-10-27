from typing import Dict, List, Tuple
import pandas as pd
from domain.dialogue_manager import Intent

def read_dataset_with_predictions(file_path: str) -> pd.DataFrame:
    """
    Read the CSV file containing the dataset with predictions.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame containing the dataset with predictions.
    """
    df = pd.read_csv(file_path)
    print(f"Dataset loaded. Shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    return df

def evaluate_accuracy(df: pd.DataFrame) -> float:
    """
    Calculate the accuracy of the predictions.

    Args:
        df (pd.DataFrame): DataFrame containing true and predicted intents.

    Returns:
        float: Accuracy score.
    """
    correct_predictions = (df['intent_enum'] == df['predicted_intent']).sum()
    total_predictions = len(df)
    accuracy = correct_predictions / total_predictions
    return accuracy

def create_contingency_table(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, List[float]]]:
    """
    Create a contingency table and calculate precision, recall, and F1-score for each intent.

    Args:
        df (pd.DataFrame): DataFrame containing true and predicted intents.

    Returns:
        Tuple[pd.DataFrame, Dict[str, List[float]]]: Contingency table and metrics dictionary.
    """
    intents = Intent.__members__.keys()
    contingency_table = pd.DataFrame(0, index=intents, columns=intents)
    
    for true_intent, pred_intent in zip(df['intent_enum'], df['predicted_intent']):
        contingency_table.loc[true_intent, pred_intent] += 1
    
    metrics = {}
    for intent in intents:
        true_positives = contingency_table.loc[intent, intent]
        false_positives = contingency_table[intent].sum() - true_positives
        false_negatives = contingency_table.loc[intent].sum() - true_positives
        
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        metrics[intent] = [precision, recall, f1_score]
    
    return contingency_table, metrics

def print_results(accuracy: float, contingency_table: pd.DataFrame, metrics: Dict[str, List[float]]) -> None:
    """
    Print the evaluation results.

    Args:
        accuracy (float): Overall accuracy score.
        contingency_table (pd.DataFrame): Contingency table.
        metrics (Dict[str, List[float]]): Dictionary containing precision, recall, and F1-score for each intent.
    """
    print(f"\nOverall Accuracy: {accuracy:.4f}")
    print("\nContingency Table:")
    print(contingency_table)
    print("\nMetrics per Intent:")
    for intent, scores in metrics.items():
        print(f"{intent}:")
        print(f"  Precision: {scores[0]:.4f}")
        print(f"  Recall: {scores[1]:.4f}")
        print(f"  F1-score: {scores[2]:.4f}")

if __name__ == "__main__":
    file_path = "dataset_with_predictions_5k.csv"
    df = read_dataset_with_predictions(file_path)
    
    accuracy = evaluate_accuracy(df)
    contingency_table, metrics = create_contingency_table(df)
    
    print_results(accuracy, contingency_table, metrics)
