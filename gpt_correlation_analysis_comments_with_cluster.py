import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


# Load data from files
df_total_comments = pd.read_csv('data/step2_total_comments_per_user.csv')
df_mid_chars = pd.read_csv('data/step2_mid_chars_comment_per_user2.csv')

# Merge the two dataframes based on user_id
merged_df = pd.merge(df_total_comments, df_mid_chars, on='user_id', how='inner', suffixes=('_total', '_mid'))

# Standardize the data (important for K-Means)
scaler = StandardScaler()
scaled_data = scaler.fit_transform(merged_df[['comment_length_total', 'comment_length_mid']])

# Apply K-Means clustering
n_clusters = 3  # You can change this value based on your requirements
kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(scaled_data)

# Add cluster labels to the dataframe
merged_df['cluster'] = kmeans.labels_

# Save the merged and clustered data to the 'data' directory
if not os.path.exists('data'):
    os.makedirs('data')
merged_df.to_csv('data/clustered_comments_data.csv', index=False)


# Plot the clusters
plt.figure(figsize=(10, 6))
for i in range(n_clusters):
    cluster_data = merged_df[merged_df['cluster'] == i]
    plt.scatter(cluster_data['comment_length_total'], cluster_data['comment_length_mid'], label=f'Cluster {i}')

plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=300, c='red', marker='X', label='Centroids')
plt.title('K-Means Clustering: Total Comments vs Median Characters per Comment')
plt.xlabel('Total Comments')
plt.ylabel('Median Characters per Comment')
plt.legend()
plt.grid(True)

plt.savefig('img/kmeans_clustering_comments.png')

plt.show()
