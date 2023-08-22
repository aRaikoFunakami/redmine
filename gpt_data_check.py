import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("data/step1_data_with_username.csv")

# 1. Check for missing values
print("\n=== Checking for Missing Values ===")
print(df.isnull().sum())
df.to_csv("data/data_check_missing_values.csv", index=False)

# 2. Check for outliers
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
for col in numeric_columns:
    plt.figure()
    sns.boxplot(df[col])
    plt.title(f"Boxplot of {col}")
    plt.savefig(f"img/data_check_outliers_{col}.png")
df[numeric_columns].to_csv("data/data_check_outliers.csv", index=False)

# 3. Check data distribution
for col in numeric_columns:
    plt.figure()
    sns.histplot(df[col], kde=True)
    plt.title(f"Distribution of {col}")
    plt.savefig(f"img/data_check_distribution_{col}.png")
df[numeric_columns].to_csv("data/data_check_distribution.csv", index=False)

# 4. Check categorical data
category_columns = df.select_dtypes(include=['object']).columns
for col in category_columns:
    print("\nUnique values and their frequency for " + col + ":")
    print(df[col].value_counts())
df[category_columns].to_csv("data/data_check_categorical.csv", index=False)

# 5. Check for duplicate data
print("\n=== Checking for Duplicate Data ===")
print("Number of duplicate rows:", df.duplicated().sum())
df[df.duplicated()].to_csv("data/data_check_duplicates.csv", index=False)

# 6. Check correlations
numeric_df = df.select_dtypes(include=['float64', 'int64'])
correlation_matrix = numeric_df.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title("Correlation Matrix")
plt.savefig("img/data_check_correlation_matrix.png")
correlation_matrix.to_csv("data/data_check_correlation.csv", index=False)

plt.show()
