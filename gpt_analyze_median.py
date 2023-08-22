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
    grouped.plot(kind='bar', title=title)
    plt.ylabel(ylabel)
    plt.xlabel('User ID')
    plt.tight_layout()
    plt.savefig(f'img/{save_name}.png')
    plt.close()
    
    # Save the grouped data to CSV in the "data" directory with name starting with "step2_"
    grouped.to_csv(f'data/step2_{save_name}.csv')

# ... [The rest of the program remains unchanged] ...

# 6. Mid number of characters per comment per user
plot_and_save(df, 'comment_length', 'median', 'Median Characters', 'mid_chars_comment_per_user', 'Median Characters per Comment by User')


# 6-1 異常値排除のためコメント数の少ないメンバーは排除する
# comment_length > 0 の行で、user_id ごとのカウントを取得
comment_counts = df[df['comment_length'] > 0]['user_id'].value_counts()

# カウントが10以上の user_id のみを取得
valid_users = comment_counts[comment_counts >= 10].index

# 元のデータフレームを valid_users の条件でフィルタリング
filtered_df = df[df['user_id'].isin(valid_users)]
plot_and_save(filtered_df, 'comment_length', 'median', 'Median Characters', 'mid_chars_comment_per_user2', 'Median Characters per Comment by User')

def plot_histogram(data, xlabel, save_name, title, bins=10):
    data.plot(kind='hist', bins=bins, title=title, edgecolor='black')
    plt.xlabel(xlabel)
    plt.tight_layout()
    plt.savefig(f'img/{save_name}.png')
    plt.close()

# 6-2 異常値排除のためコメント数の少ないメンバーは排除したデータでmidも作っておく
mid_df = filtered_df.groupby('user_id')['comment_length'].median()
plot_histogram(mid_df , 'Median Characters', 'hist_median_characters_per_comment_by_user', 'Histogram of Median Characters per Comment by User')
