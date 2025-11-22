import argparse
import pandas as pd
import csv

def parse_args():
    parser = argparse.ArgumentParser(description="Compute the confusion matrix between two annotated csv files")
    parser.add_argument("-a", "--csv_a", required=True, help="First CSV file")
    parser.add_argument("-b", "--csv_b", required=True, help="Second CSV file")
    parser.add_argument("-c", "--confusion", required=True, help="Output CSV file for confusion matrix")  
    parser.add_argument("-m", "--metrics", required=True, help="Output CSV file for metrics") 
    return parser.parse_args()

def read_csv_labels(path):
    labels = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            if len(row) >= 3:
                labels.append(row[2])
    return labels

def compute_metrics(confusion_matrix):
    metrics = []
    all_labels = sorted(set(confusion_matrix.index).union(confusion_matrix.columns))
    for label in all_labels:
        # True Positive
        if label in confusion_matrix.index and label in confusion_matrix.columns:
            tp = confusion_matrix.loc[label, label]
        else:
            tp = 0
        # False Positives: sum of column label except TP
        if label in confusion_matrix.columns:
            fp = confusion_matrix[label].sum() - tp
        else:
            fp = 0
        # False Negatives: sum of row label except TP
        if label in confusion_matrix.index:
            fn = confusion_matrix.loc[label].sum() - tp
        else:
            fn = 0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall    = tp / (tp + fn) if (tp + fn) > 0 else 0.0

        metrics.append({
            "label": label,
            "precision": precision,
            "recall": recall
        })

    return pd.DataFrame(metrics)

def main():
    args = parse_args()

    standard_labels = read_csv_labels(args.csv_a)
    test_labels = read_csv_labels(args.csv_b)

    confusion_matrix = pd.crosstab(
        pd.Series(standard_labels, name="Gold Standard Labels"), 
        pd.Series(test_labels, name="LLM Labels")
        )
    confusion_matrix.to_csv(args.confusion)

    metrics_df = compute_metrics(confusion_matrix)
    metrics_df.to_csv(args.metrics, index=False)

if __name__ == "__main__":
    main()

