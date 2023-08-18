import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the data
df = pd.read_csv("data/step1_data.csv")
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

# 1. Average number of characters per issue description per user
plot_and_save(df, 'issue_description_length', 'mean', 'Average Characters', 'avg_chars_issue_desc_per_user', 'Average Characters per Issue Description by User')

# 2. Total number of comments per user
plot_and_save(df, 'comment_length', 'count', 'Total Comments', 'total_comments_per_user', 'Total Number of Comments by User')

# 3. Total number of characters per comment per user
plot_and_save(df, 'comment_length', 'sum', 'Total Characters', 'total_chars_comment_per_user', 'Total Characters per Comment by User')

# 4. Average number of characters per comment per user
plot_and_save(df, 'comment_length', 'mean', 'Average Characters', 'avg_chars_comment_per_user', 'Average Characters per Comment by User')

# 5. Average number of comments per user per day
df['unique_days'] = df['comment_date'].dt.date

# Specify start and end dates
START_DATE = '2023-07-01'
END_DATE = '2023-07-31'

# Compute the number of days in the analysis period
DAYS_IN_PERIOD = (pd.to_datetime(END_DATE) - pd.to_datetime(START_DATE)).days + 1

# Total number of comments by each user
total_comments_per_user = df.groupby('user_id').size()

# Average number of comments per day for each user
avg_comments_per_day = total_comments_per_user / DAYS_IN_PERIOD

# Plotting
avg_comments_per_day.plot(kind='bar', title='Average Number of Comments per Day by User')
plt.ylabel('Average Comments per Day')
plt.xlabel('User ID')
plt.tight_layout()
plt.savefig('img/avg_comments_per_day_per_user.png')
plt.close()
