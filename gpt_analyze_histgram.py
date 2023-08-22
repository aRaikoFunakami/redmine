import pandas as pd
import matplotlib.pyplot as plt
import os
import config

# Load the data
df = pd.read_csv("data/step1_data_with_username.csv")
df['comment_date'] = pd.to_datetime(df['comment_date'])
df_comment = df[df['comment_length'] > 0]

# Ensure directories exist
if not os.path.exists('data'):
    os.makedirs('data')
if not os.path.exists('img'):
    os.makedirs('img')
    
# Specify start and end dates
START_DATE = config.start_date.strftime('%Y-%m-%d')
END_DATE = config.end_date.strftime('%Y-%m-%d')

# Compute the number of days in the analysis period
DAYS_IN_PERIOD = (pd.to_datetime(END_DATE) - pd.to_datetime(START_DATE)).days + 1
# 365（全日数） - 104（土日の合計） - 16（祝日の数）= 245日
DAYS_IN_PERIOD = 365 - 104 - 16

def plot_histogram(data, xlabel, save_name, title, bins=10):
    data.plot(kind='hist', bins=bins, title=title, edgecolor='black')
    plt.xlabel(xlabel)
    plt.tight_layout()
    plt.savefig(f'img/{save_name}.png')
    plt.close()

# ... [The rest of the program remains unchanged] ...

# Histograms
# 1. Histogram for average comments per day
avg_comments_per_day = df_comment.groupby('user_id').size() / DAYS_IN_PERIOD
plot_histogram(avg_comments_per_day, 'Average Comments per Day', 'hist_avg_comments_per_day', 'Histogram of Average Comments per Day')

# 2. Histogram for total number of comments per user
total_comments_per_user = df_comment.groupby('user_id').size()
plot_histogram(total_comments_per_user, 'Total Comments', 'hist_total_comments', 'Histogram of Total Comments per User')

# 3. Histogram for average number of characters per issue description per user
avg_chars_issue_desc_per_user = df.drop_duplicates(subset=['issue_id', 'user_id']).groupby('user_id')['issue_description_length'].mean()
plot_histogram(avg_chars_issue_desc_per_user, 'Average Characters per Issue Description', 'hist_avg_chars_issue_desc', 'Histogram of Average Characters per Issue Description by User')
