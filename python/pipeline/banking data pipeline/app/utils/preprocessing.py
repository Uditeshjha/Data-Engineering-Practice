import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def optimize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Optimize numeric dtypes:
      - Integers → int8 / int16 / int32
      - Floats   → float16 / float32
    Returns a DataFrame with reduced memory usage.
    """
    before = df.memory_usage(deep=True).sum() / 1024**2
    optimized = df.copy()

    for col in optimized.columns:
        s = optimized[col]

        # --- Integers ---
        if pd.api.types.is_integer_dtype(s):
            vals = s.astype("int64")  # safe for bound checks
            if vals.min() >= np.iinfo(np.int8).min and vals.max() <= np.iinfo(np.int8).max:
                optimized[col] = s.astype("int8")
            elif vals.min() >= np.iinfo(np.int16).min and vals.max() <= np.iinfo(np.int16).max:
                optimized[col] = s.astype("int16")
            elif vals.min() >= np.iinfo(np.int32).min and vals.max() <= np.iinfo(np.int32).max:
                optimized[col] = s.astype("int32")
            # else: leave unchanged if too large

        # --- Floats ---
        elif pd.api.types.is_float_dtype(s):
            s64 = s.astype("float64")
            if np.allclose(s64, s64.astype("float16"), rtol=1e-03, atol=1e-06, equal_nan=True):
                optimized[col] = s64.astype("float16")
            else:
                optimized[col] = s64.astype("float32")

    after = optimized.memory_usage(deep=True).sum() / 1024**2
    print(f"Memory: {before:.3f} MB → {after:.3f} MB ({(before - after) / before * 100:.2f}% reduction)")

    return optimized

def treat_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """
    Treat null values in the DataFrame:
      - Drop columns with >30% nulls
      - Fill numeric columns with median
      - Fill categorical/object columns with mode
      - Fill datetime columns with forward fill, then backward fill
    Returns a cleaned DataFrame.
    """
    cleaned = df.copy()

    # 1. Drop columns with >60% nulls
    threshold = 0.6
    null_ratio = cleaned.isna().mean()
    to_drop = null_ratio[null_ratio > threshold].index
    cleaned = cleaned.drop(columns=to_drop)
    # Dict = {
    #     "threshold": threshold,
    #     "dropped_columns": [],
    #     "filled_numeric": {},
    #     "filled_categorical": {},
    #     "timeseries_fill": timeseries_fill,
    #     "time_used": None
    # }

    # 2. Handle remaining nulls
    for col in cleaned.columns:
        if cleaned[col].isna().any():
            # Numeric columns
            if pd.api.types.is_numeric_dtype(cleaned[col]):
                median_val = cleaned[col].median()
                cleaned[col] = cleaned[col].fillna(median_val)

            # Datetime columns
            elif pd.api.types.is_datetime64_any_dtype(cleaned[col]):
                cleaned[col] = cleaned[col].fillna(method="ffill").fillna(method="bfill")

            # Categorical / Object columns
            else:
                mode_val = cleaned[col].mode(dropna=True)
                if not mode_val.empty:
                    cleaned[col] = cleaned[col].fillna(mode_val[0])
                else:
                    cleaned[col] = cleaned[col].fillna("")

    return cleaned

def find_outliers_iqr(df: pd.DataFrame, cols=None) -> dict:
    """
    Detect outliers in numeric columns using IQR method.
    Returns a dictionary of column -> list of outlier indices.
    """
    if cols is None:
        cols = df.select_dtypes(include=np.number).columns

    outliers = {}
    for col in cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        mask = (df[col] < lower) | (df[col] > upper)
        outliers[col] = df[mask].index.tolist()
    return outliers

def visualize_dataset(df: pd.DataFrame) -> None:
    """
    Automatically generate common EDA visualizations from a DataFrame.
    - Numeric columns: histogram, boxplot, violin plot
    - Categorical columns: countplot
    - Numeric vs numeric: scatter, correlation heatmap, pairplot
    - Numeric vs categorical: boxplot
    - Categorical vs categorical: crosstab heatmap
    """
    sns.set(style="whitegrid", palette="Set2")

    # Identify column types
    num_cols = df.select_dtypes(include=["number"]).columns.tolist()
    cat_cols = [c for c in df.columns if df[c].dtype == "object" or df[c].nunique() <= 20]

    # --- Summary ---
    print("Shape:", df.shape)
    print("\nMissing Values:\n", df.isna().sum())
    print("\nBasic Statistics:\n", df.describe(include="all").T)

    # --- Numeric Univariate ---
    for col in num_cols:
        fig, axes = plt.subplots(1, 3, figsize=(16, 4))

        sns.histplot(df[col].dropna(), bins=30, kde=True, ax=axes[0])
        axes[0].set_title(f"Histogram + KDE: {col}")

        sns.boxplot(x=df[col], ax=axes[1])
        axes[1].set_title(f"Boxplot: {col}")

        sns.violinplot(x=df[col], ax=axes[2])
        axes[2].set_title(f"Violin Plot: {col}")

        plt.show()

    # --- Categorical Univariate ---
    for col in cat_cols:
        plt.figure(figsize=(8, 4))
        sns.countplot(x=df[col], order=df[col].value_counts().index)
        plt.title(f"Count Plot: {col}")
        plt.xticks(rotation=45)
        plt.show()

    # --- Correlation Heatmap ---
    if len(num_cols) > 1:
        plt.figure(figsize=(10, 6))
        corr = df[num_cols].corr()
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Correlation Heatmap")
        plt.show()

    # --- Scatterplots (Numeric vs Numeric) ---
    if len(num_cols) >= 2:
        for i in range(len(num_cols)):
            for j in range(i+1, len(num_cols)):
                plt.figure(figsize=(6, 4))
                sns.scatterplot(x=df[num_cols[i]], y=df[num_cols[j]])
                plt.title(f"Scatter: {num_cols[i]} vs {num_cols[j]}")
                plt.show()

    # --- Numeric vs Categorical ---
    for cat in cat_cols:
        for num in num_cols:
            plt.figure(figsize=(8, 4))
            sns.barplot(x=df[cat], y=df[num])
            plt.title(f"{num} by {cat}")
            plt.xticks(rotation=45)
            plt.show()