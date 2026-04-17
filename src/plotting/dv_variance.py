import sys
import os
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(parent_folder)
import pandas as pd
import matplotlib.pyplot as plt
from src.params import INPUTS

baseline = INPUTS
baseline["LCOW"] = 3.97

def load_and_clean(file_path):
    # Read raw CSV (no headers)
    df = pd.read_csv(file_path, header=None)

    # Fix last column: remove brackets and convert to float
    last_col = df.columns[-1]
    df[last_col] = df[last_col].astype(str).str.strip("[]").astype(float)

    return df

def normalize_about_baseline(df, baseline_dict):
    df_norm = df.copy()

    for col in df.columns:
        if col in baseline_dict:
            base = baseline_dict[col]
            df_norm[col] = (df[col] - base) / base

    return df_norm


def plot_boxplots(df):
    plt.figure()
    df.boxplot()
    plt.axhline(0, color='red', linestyle='--')  # Add a horizontal line at y=0 for reference
    plt.xticks(rotation=45)
    plt.ylabel("Deviation from Yu and Jenne (2017)")

    plt.tight_layout()
    plt.show()

def plot_individual(df):
    for col in df.columns:
        plt.figure()
        df.boxplot(column=col)
        plt.title(f"Boxplot of Column {col}")  # Add a horizontal line at y=0 for reference
        plt.show()

# ---- Run ----
file_path = "data/sensitivity_results.csv"

df = load_and_clean(file_path)

df = df.drop(columns=[0])

df.columns = list(baseline.keys())

df = df.apply(pd.to_numeric, errors='coerce')

df_norm = normalize_about_baseline(df, baseline)

# All columns in one plot
plot_boxplots(df_norm)
