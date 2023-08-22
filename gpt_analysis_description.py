# 平均値に中央値と中央値のヒストグラムのグラフを作成を加えたい。
import pandas as pd
import matplotlib.pyplot as plt
import os
import config

# Load the data
df = pd.read_csv("data/step1_data_with_username.csv")
df['comment_date'] = pd.to_datetime(df['comment_date'])

# Ensure directories exist
if not os.path.exists('data'):
    os.makedirs('data')
if not os.path.exists('img'):
    os.makedirs('img')

# Analysis and plotting
def plot_and_save(df, column, agg_func, ylabel, save_name, title):
    grouped = df.groupby('user_id')[column].agg(agg_func)
    
    # Plot bar chart
    grouped.plot(kind='bar', title=title)
    plt.ylabel(ylabel)
    plt.xlabel('User ID')
    plt.tight_layout()
    plt.savefig(f'img/{save_name}.png')
    plt.close()
    
    # Plot histogram for median
    if agg_func == 'median':
        grouped.hist()
        plt.title(f'Histogram of {title}')
        plt.xlabel(ylabel)
        plt.ylabel('Frequency')
        plt.tight_layout()
        plt.savefig(f'img/histogram_{save_name}.png')
        plt.close()
    
    # Save the grouped data to CSV in the "data" directory with name starting with "step2_"
    grouped.to_csv(f'data/step2_{save_name}.csv')

# Drop duplicates for the column issue_description_length based on issue_id and user_id
df_unique_issues = df.drop_duplicates(subset=['issue_id', 'user_id'])

# 1. Average number of characters per issue description per user
plot_and_save(df_unique_issues, 'issue_description_length', 'mean', 'Average Characters', 'avg_chars_issue_desc_per_user', 'Average Characters per Issue Description by User')

# 2. Median number of characters per issue description per user
plot_and_save(df_unique_issues, 'issue_description_length', 'median', 'Median Characters', 'median_chars_issue_desc_per_user', 'Median Characters per Issue Description by User')
