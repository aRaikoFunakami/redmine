import pandas as pd
import matplotlib.pyplot as plt

# Load data from files
df_total_comments = pd.read_csv('data/step2_total_comments_per_user.csv')
df_mid_chars = pd.read_csv('data/step2_mid_chars_comment_per_user2.csv')

# Merge the two dataframes based on user_id
merged_df = pd.merge(df_total_comments, df_mid_chars, on='user_id', how='inner', suffixes=('_total', '_mid'))

# Create the graph
plt.figure(figsize=(10, 6))
plt.scatter(merged_df['comment_length_total'], merged_df['comment_length_mid'], color='blue')
plt.title('Correlation: Total Comments vs Median Characters per Comment')
plt.xlabel('Total Comments')
plt.ylabel('Median Characters per Comment')
plt.grid(True)

# Display the graph
plt.show()
