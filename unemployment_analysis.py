"""
CodeAlpha Data Science Internship
Task 2: Unemployment Analysis with Python

The script downloads the public CSV if it is not already present,
cleans the data, explores unemployment trends, compares periods,
and creates visualizations.
"""

import os
import urllib.request
import pandas as pd
import matplotlib.pyplot as plt

DATA_DIR = "data"
OUTPUT_DIR = "outputs"
DATA_PATH = os.path.join(DATA_DIR, "Unemployment_Rate_upto_11_2020.csv")

DATA_URL = (
    "https://raw.githubusercontent.com/jarif87/DataSets/master/"
    "Unemployment_Rate_upto_11_2020.csv"
)

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


def download_dataset():
    if not os.path.exists(DATA_PATH):
        print("Downloading dataset...")
        urllib.request.urlretrieve(DATA_URL, DATA_PATH)
    return DATA_PATH


def clean_data(path):
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()

    # Normalize column names used by this dataset.
    rename_map = {}
    for col in df.columns:
        clean = col.strip().replace(" ", "_")
        rename_map[col] = clean
    df = df.rename(columns=rename_map)

    # The dataset contains two columns named Region; pandas may rename one.
    # Select the unemployment-related columns by position/name.
    rate_col = "Estimated_Unemployment_Rate"
    employed_col = "Estimated_Employed"
    participation_col = "Estimated_Labour_Participation_Rate"

    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")

    for col in [rate_col, employed_col, participation_col]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["Date", rate_col]).copy()
    df["Month"] = df["Date"].dt.month
    df["Month_Name"] = df["Date"].dt.strftime("%b")
    df["Year"] = df["Date"].dt.year

    # Analytical period labels. March is treated as a transition month.
    df["Period"] = "Other"
    df.loc[df["Date"] < pd.Timestamp("2020-03-01"), "Period"] = "Pre-COVID"
    df.loc[df["Date"] >= pd.Timestamp("2020-04-01"), "Period"] = "COVID Period"

    return df


def save(fig, name):
    fig.savefig(os.path.join(OUTPUT_DIR, name), dpi=160, bbox_inches="tight")
    plt.close(fig)


def main():
    path = download_dataset()
    df = clean_data(path)

    rate = "Estimated_Unemployment_Rate"
    participation = "Estimated_Labour_Participation_Rate"

    print("Rows after cleaning:", len(df))
    print("Columns:", list(df.columns))

    # 1. National trend
    monthly = df.groupby("Date")[rate].mean().sort_index()
    fig = plt.figure(figsize=(10, 5))
    plt.plot(monthly.index, monthly.values, marker="o")
    plt.axvline(pd.Timestamp("2020-03-01"), linestyle="--", label="March 2020")
    plt.title("Average Unemployment Rate in India Over Time")
    plt.xlabel("Date")
    plt.ylabel("Unemployment Rate (%)")
    plt.grid(alpha=0.25)
    plt.legend()
    save(fig, "national_unemployment_trend.png")

    # 2. Regional averages
    regional = df.groupby("Region")[rate].mean().sort_values(ascending=False).head(10)
    fig = plt.figure(figsize=(10, 6))
    regional.sort_values().plot(kind="barh")
    plt.title("Top 10 Regions by Average Unemployment Rate")
    plt.xlabel("Average Unemployment Rate (%)")
    plt.ylabel("Region")
    plt.grid(axis="x", alpha=0.25)
    save(fig, "top_10_regions.png")

    # 3. Pre-COVID vs COVID period
    comp = df[df["Period"].isin(["Pre-COVID", "COVID Period"])]
    comparison = comp.groupby("Period")[rate].mean()

    fig = plt.figure(figsize=(7, 5))
    comparison.plot(kind="bar")
    plt.title("Pre-COVID vs COVID-Period Unemployment")
    plt.ylabel("Average Unemployment Rate (%)")
    plt.xticks(rotation=0)
    plt.grid(axis="y", alpha=0.25)
    save(fig, "covid_comparison.png")

    # 4. Monthly 2020 pattern
    monthly_2020 = df[df["Year"] == 2020].groupby("Month")[rate].mean()
    fig = plt.figure(figsize=(10, 5))
    plt.plot(monthly_2020.index, monthly_2020.values, marker="o")
    plt.xticks(monthly_2020.index)
    plt.title("Monthly Unemployment Pattern During 2020")
    plt.xlabel("Month Number")
    plt.ylabel("Average Unemployment Rate (%)")
    plt.grid(alpha=0.25)
    save(fig, "monthly_2020_pattern.png")

    # 5. Correlation
    pair = df[[rate, participation]].dropna()
    corr = pair.corr().iloc[0, 1]

    fig = plt.figure(figsize=(8, 5))
    plt.scatter(pair[participation], pair[rate], alpha=0.55)
    plt.title("Unemployment Rate vs Labour Participation Rate")
    plt.xlabel("Labour Participation Rate (%)")
    plt.ylabel("Unemployment Rate (%)")
    plt.grid(alpha=0.25)
    save(fig, "unemployment_vs_labour_participation.png")

    avg_pre = comparison.get("Pre-COVID")
    avg_covid = comparison.get("COVID Period")
    change = avg_covid - avg_pre

    summary = pd.DataFrame({
        "Metric": [
            "Rows after cleaning",
            "Average unemployment - Pre-COVID",
            "Average unemployment - COVID Period",
            "Change in percentage points",
            "Unemployment/Labour participation correlation",
        ],
        "Value": [len(df), avg_pre, avg_covid, change, corr],
    })
    summary.to_csv(os.path.join(OUTPUT_DIR, "analysis_summary.csv"), index=False)

    df.groupby("Region").agg(
        Average_Unemployment_Rate=(rate, "mean"),
        Maximum_Unemployment_Rate=(rate, "max"),
        Average_Labour_Participation=(participation, "mean"),
    ).sort_values("Average_Unemployment_Rate", ascending=False).to_csv(
        os.path.join(OUTPUT_DIR, "regional_summary.csv")
    )

    print("\n===== KEY RESULTS =====")
    print(f"Average unemployment - Pre-COVID: {avg_pre:.2f}%")
    print(f"Average unemployment - COVID Period: {avg_covid:.2f}%")
    print(f"Change: {change:.2f} percentage points")
    print(f"Correlation with labour participation: {corr:.3f}")
    print("\nHighest-average regions:")
    print(regional)


if __name__ == "__main__":
    main()
