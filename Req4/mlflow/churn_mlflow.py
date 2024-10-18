import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, recall_score, precision_score
from sklearn.preprocessing import StandardScaler

EPSILON = 1e-6

def kde_plot(positive_class, negative_class):
    sns.kdeplot(positive_class, color="r", label="Positive Class", fill=True)
    sns.kdeplot(negative_class, color="b", label="Negative Class", fill=True)
    
    plt.xlabel("Probability")
    plt.ylabel("Density")
    plt.title("Probability Density Function")
    plt.legend()
    # plt.show()

def plot_threshold_plot(recall_vals, tnr_vals, thresholds, max_harmonic_mean_index):
    harmonic_mean = (
        2 * (np.array(recall_vals) * np.array(tnr_vals)) / 
        (np.array(recall_vals) + np.array(tnr_vals) + EPSILON)
    )

    max_harmonic_mean_threshold = thresholds[max_harmonic_mean_index]
    max_harmonic_mean_value = harmonic_mean[max_harmonic_mean_index]

    x_idx = 0.5
    thresholds_id = np.where(thresholds == x_idx)[0][0]

    plt.figure(figsize=(8, 6))
    for vals, label in [(recall_vals, "Recall"), (tnr_vals, "TNR"), (harmonic_mean, "Harmonic Mean")]:
        plt.plot(thresholds, vals, label=label, alpha=0.5)

    plt.xlabel("Thresholds")
    plt.ylabel("Value")
    plt.title(
        f"Metrics vs Thresholds\nMax Harmonic Mean: {max_harmonic_mean_value*100:.2f} at {max_harmonic_mean_threshold*100:.2f}\n Recall: {recall_vals[thresholds_id]*100:.2f} TNR: {tnr_vals[thresholds_id]*100:.2f}"
    )

    plt.legend()
    plt.grid(True)

    plt.axhline(y=max_harmonic_mean_value, color="r", linestyle="--", alpha=0.5)
    plt.axvline(x=x_idx, color="r", linestyle="--", alpha=0.5)

    plt.legend()
    # plt.show()

def get_monitoring_vals(df):
    thresholds = np.linspace(0, 1, 101)
    recall_vals, tnr_vals, harmonic_means = [], [], []

    for threshold in thresholds:
        true_positives = ((df["pred"] >= threshold) & (df["true"] == 1)).sum()
        false_positives = ((df["pred"] >= threshold) & (df["true"] == 0)).sum()
        true_negatives = ((df["pred"] < threshold) & (df["true"] == 0)).sum()
        false_negatives = ((df["pred"] < threshold) & (df["true"] == 1)).sum()

        recall = true_positives / (true_positives + false_negatives + EPSILON)
        tnr = true_negatives / (true_negatives + false_positives + EPSILON)

        recall_vals.append(recall)
        tnr_vals.append(tnr)

        harmonic_mean = 2 * (recall * tnr) / (recall + tnr + EPSILON)
        harmonic_means.append(harmonic_mean)

    max_harmonic_mean_index = np.argmax(harmonic_means)

    return recall_vals, tnr_vals, thresholds, max_harmonic_mean_index

# Load dataset
df = pd.read_csv("dataset_features_v3.csv")

X_1 = df.drop(columns=['churn'])
y_1 = df['churn']

# Create a list of models
models = [
    ('RandomForest', RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)),
    ('LogisticRegression', LogisticRegression()),
    ('DecisionTree', DecisionTreeClassifier()),
    ('KNN', KNeighborsClassifier()),
    ('XGBoost', XGBClassifier())
]

cv = KFold(n_splits=5, random_state=42, shuffle=True)

mlflow.set_experiment("Churn Prediction Experiment")

for name, model in models:
    with mlflow.start_run(run_name=f"{name}_cross_validation"):
        print(f"Cross Validation for {name}")
        
        accuracies, recalls, precisions, tnrs = [], [], [], []

        split = 0
        for train_index, test_index in cv.split(X_1):
            X_train, X_test = X_1.iloc[train_index], X_1.iloc[test_index]
            y_train, y_test = y_1.iloc[train_index], y_1.iloc[test_index]

            # Scale the data
            if name != "RandomForest":
                scaler = StandardScaler()
                X_train = scaler.fit_transform(X_train)
                X_test = scaler.transform(X_test)

            # Train the model
            model.fit(X_train, y_train)

            # Predict the test set
            y_pred = model.predict(X_test)

            # Evaluate and collect metrics
            acc = accuracy_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            accuracies.append(acc)
            recalls.append(recall)
            precisions.append(precision)

            cm = confusion_matrix(y_test, y_pred)
            tnrs.append(cm[0, 0] / (cm[0, 0] + cm[0, 1]))

            plt.figure()
            sns.heatmap(cm, annot=True, fmt="d")
            plt.title(f"Confusion Matrix - {name}")
            plt.xlabel("Predicted")
            plt.ylabel("Actual")
            mlflow.log_figure(plt.gcf(), f"confusion_matrix_{name}_{split}.png")
            plt.close()

            # Get monitoring values and log threshold plot
            df_preds = pd.DataFrame(data={"pred": model.predict_proba(X_test)[:, 1], "true": y_test})
            recall_vals, tnr_vals, thresholds, max_harmonic_mean_index = get_monitoring_vals(df_preds)
            plot_threshold_plot(recall_vals, tnr_vals, thresholds, max_harmonic_mean_index)
            mlflow.log_figure(plt.gcf(), f"threshold_plot_{name}_{split}.png")
            plt.close()

            # Log KDE plot
            kde_plot(df_preds[df_preds["true"] == 1]['pred'], df_preds[df_preds["true"] == 0]['pred'])
            mlflow.log_figure(plt.gcf(), f"kde_plot_{name}_{split}.png")
            plt.close()

            split += 1

        # Log overall metrics
        mlflow.log_metric("avg_accuracy", np.mean(accuracies))
        mlflow.log_metric("avg_recall", np.mean(recalls))
        mlflow.log_metric("avg_tnr", np.mean(tnrs))
        mlflow.log_metric("avg_precision", np.mean(precisions))

        print(f"Average Accuracy: {np.mean(accuracies)}")
        print(f"Average Recall: {np.mean(recalls)}")
        print(f"Average TNR: {np.mean(tnrs)}")
        print(f"Average Precision: {np.mean(precisions)}")

mlflow.end_run()

# Train models on the entire dataset
X_train_1, X_test_1, y_train_1, y_test_1 = train_test_split(X_1, y_1, test_size=0.2, random_state=42)

for name, model in models:
    with mlflow.start_run(run_name=f"{name}_full_training"):
        print(f"Training {name} on the entire dataset")
        
        if name != "RandomForest":
            scaler = StandardScaler()
            X_train_1 = scaler.fit_transform(X_train_1)
            X_test_1 = scaler.transform(X_test_1)

        model.fit(X_train_1, y_train_1)

        # Predict the test set
        y_pred_1 = model.predict(X_test_1)

        # Evaluate metrics
        acc = accuracy_score(y_test_1, y_pred_1)
        recall = recall_score(y_test_1, y_pred_1)
        precision = precision_score(y_test_1, y_pred_1)

        # Log metrics
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("precision", precision)

        # Log confusion matrix
        cm = confusion_matrix(y_test_1, y_pred_1)
        tnr = cm[0, 0] / (cm[0, 0] + cm[0, 1])
        mlflow.log_metric("tnr", tnr)
        plt.figure()
        sns.heatmap(cm, annot=True, fmt="d")
        plt.title(f"Confusion Matrix - {name} (Full Training)")
        plt.xlabel("Predicted")
        plt.ylabel("Actual")
        mlflow.log_figure(plt.gcf(), f"confusion_matrix_full_{name}.png")
        plt.close()

        # Get monitoring values and log threshold plot
        df_preds_full = pd.DataFrame(data={"pred": model.predict_proba(X_test_1)[:, 1], "true": y_test_1})
        recall_vals, tnr_vals, thresholds, max_harmonic_mean_index = get_monitoring_vals(df_preds_full)
        plot_threshold_plot(recall_vals, tnr_vals, thresholds, max_harmonic_mean_index)
        mlflow.log_figure(plt.gcf(), f"threshold_plot_full_{name}.png")
        plt.close()

        # Log KDE plot
        kde_plot(df_preds_full[df_preds_full["true"] == 1]['pred'], df_preds_full[df_preds_full["true"] == 0]['pred'])
        mlflow.log_figure(plt.gcf(), f"kde_plot_full_{name}.png")
        plt.close()

        print(f"Accuracy: {acc}")
        print(f"Recall: {recall}")
        print(f"TNR: {tnr}")
        print(f"Precision: {precision}")

        mlflow.sklearn.log_model(model, f"model_{name}")

mlflow.end_run()

