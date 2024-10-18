# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, recall_score, precision_score
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold

import optuna

EPSILON = 1e-6

# %%
def kde_plot(positive_class, negative_class):
    sns.kdeplot(positive_class, color="r", label="Positive Class", fill=True)
    sns.kdeplot(negative_class, color="b", label="Negative Class", fill=True)
    
    plt.xlabel("Probability")
    plt.ylabel("Density")
    plt.title("Probability Density Function")
    plt.legend()
    plt.show()

# %%
def plot_threshold_plot(recall_vals, tnr_valus, thresholds, max_harmonic_mean_index):
    harmonic_mean = (
        2 
        * (np.array(recall_vals) * np.array(tnr_valus))
        / (np.array(recall_vals) + np.array(tnr_valus) + EPSILON)
    )

    max_harmonic_mean_threshold = thresholds[max_harmonic_mean_index]
    max_harmonic_mean_value = harmonic_mean[max_harmonic_mean_index]

    x_idx = 0.5

    thresholds_id = np.where(thresholds == x_idx)[0][0]

    plt.figure(figsize=(8, 6))
    for vals, label in [(recall_vals, "Recall"), (tnr_valus, "TNR"), (harmonic_mean, "Harmonic Mean")]:
        plt.plot(thresholds, vals, label=label, alpha=0.5)

    plt.xlabel("Thresholds")
    plt.ylabel("Value")
    plt.title(
        f"Metrics vs Thresholds\nMax Harmonic Mean: {max_harmonic_mean_value*100:.2f} at {max_harmonic_mean_threshold*100:.2f}\n Recall: {recall_vals[thresholds_id]*100:.2f} TNR: {tnr_valus[thresholds_id]*100:.2f}"
    )

    plt.legend()
    plt.grid(True)

    plt.axhline(
        y=max_harmonic_mean_value,
        color="r",
        linestyle="--",
        label=f"Max Harmonic Mean Value",
        alpha=0.5,
    )

    plt.axvline(
        x=x_idx,
        color="r",
        linestyle="--",
        label=f"Threshold: {x_idx}",
        alpha=0.5,
    )

    plt.legend()
    plt.show()


# %%
def get_monitoring_vals(df):
    thresholds = np.linspace(0, 1, 101)
    recall_vals = []
    tnr_vals = []
    harmonic_means = []

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

# %%
df = pd.read_csv("dataset_features_v2.csv")

# %% [markdown]
# # Predicting  Churn

# %%
X_1 = df.drop(columns=['churn'])
y_1 = df['churn']

# %%
# create a list of models
models = []
models.append(('RandomForest', RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)))
models.append(('LogisticRegression', LogisticRegression()))
models.append(('DecisionTree', DecisionTreeClassifier()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('XGBoost', XGBClassifier()))

# %%
# perform cross validation
cv = KFold(n_splits=5, random_state=42, shuffle=True)


for name, model in models:
    print(f"Cross Validation for {name}")
    for train_index, test_index in cv.split(X_1):
        X_train, X_test, y_train, y_test = X_1.iloc[train_index], X_1.iloc[test_index], y_1.iloc[train_index], y_1.iloc[test_index]

        # scale the data
        if name != "RandomForest":
            scaler = StandardScaler()
            X_train = scaler.fit_transform(X_train)
            X_test = scaler.transform(X_test)

        # train the model
        model.fit(X_train, y_train)

        # predict the test set
        y_pred = model.predict(X_test)

        # get the confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        print(cm)

        # get the classification report
        cr = classification_report(y_test, y_pred)
        print(cr)

        # get the accuracy
        acc = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {acc}")

        # get the recall
        recall = recall_score(y_test, y_pred)
        print(f"Recall: {recall}")

        # get the precision
        precision = precision_score(y_test, y_pred)
        print(f"Precision: {precision}")

        # get the monitoring values
        df = pd.DataFrame(data={"pred": model.predict_proba(X_test)[:, 1], "true": y_test})
        recall_vals, tnr_vals, thresholds, max_harmonic_mean_index = get_monitoring_vals(df)
        plot_threshold_plot(recall_vals, tnr_vals, thresholds, max_harmonic_mean_index)
        kde_plot(df[df["true"] == 1]['pred'], df[df["true"] == 0]['pred'])


# %%
# fit the data for all models
X_train_1, X_test_1, y_train_1, y_test_1 = train_test_split(X_1, y_1, test_size=0.2, random_state=42)

# %%
for name, model in models:
    print(f"Training {name}")
    if name != "RandomForest":
        scaler = StandardScaler()
        X_train_1 = scaler.fit_transform(X_train_1)
        X_test_1 = scaler.transform(X_test_1)

    model.fit(X_train_1, y_train_1)

    y_pred_1 = model.predict(X_test_1)

    cm = confusion_matrix(y_test_1, y_pred_1)
    print(cm)

    cr = classification_report(y_test_1, y_pred_1)
    print(cr)

    acc = accuracy_score(y_test_1, y_pred_1)
    print(f"Accuracy: {acc}")

    recall = recall_score(y_test_1, y_pred_1)
    print(f"Recall: {recall}")

    precision = precision_score(y_test_1, y_pred_1)
    print(f"Precision: {precision}")

    df = pd.DataFrame(data={"pred": model.predict_proba(X_test_1)[:, 1], "true": y_test_1})
    recall_vals, tnr_vals, thresholds, max_harmonic_mean_index = get_monitoring_vals(df)
    plot_threshold_plot(recall_vals, tnr_vals, thresholds, max_harmonic_mean_index)
    kde_plot(df[df["true"] == 1]['pred'], df[df["true"] == 0]['pred'])

# %%



