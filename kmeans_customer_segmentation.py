import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# ---------------- LOAD DATASET ----------------
data = pd.read_csv("Mall_Customers.csv")

# Select features for clustering
X = data[['Annual Income (k$)', 'Spending Score (1-100)']]

# ---------------- ELBOW METHOD ----------------
wcss = []

for i in range(1,11):
    kmeans = KMeans(n_clusters=i, random_state=42)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)

plt.figure()
plt.plot(range(1,11), wcss)
plt.title("Elbow Method")
plt.xlabel("Number of Clusters")
plt.ylabel("WCSS")
plt.savefig("images/elbow_method.png")
plt.show()

# ---------------- APPLY KMEANS ----------------
kmeans = KMeans(n_clusters=5, random_state=42)
y_kmeans = kmeans.fit_predict(X)

# Add cluster numbers to dataset
data['Cluster'] = y_kmeans

# ---------------- CLUSTER INTERPRETATION ----------------
cluster_names = {
    0: "Average Customers",
    1: "High Income High Spending",
    2: "Low Income High Spending",
    3: "High Income Low Spending",
    4: "Low Income Low Spending"
}

data['Customer Type'] = data['Cluster'].map(cluster_names)

# ---------------- VISUALIZATION ----------------
plt.figure(figsize=(8,6))

plt.scatter(X[y_kmeans == 0]['Annual Income (k$)'],
            X[y_kmeans == 0]['Spending Score (1-100)'],
            s=50, label='Cluster 1')

plt.scatter(X[y_kmeans == 1]['Annual Income (k$)'],
            X[y_kmeans == 1]['Spending Score (1-100)'],
            s=50, label='Cluster 2')

plt.scatter(X[y_kmeans == 2]['Annual Income (k$)'],
            X[y_kmeans == 2]['Spending Score (1-100)'],
            s=50, label='Cluster 3')

plt.scatter(X[y_kmeans == 3]['Annual Income (k$)'],
            X[y_kmeans == 3]['Spending Score (1-100)'],
            s=50, label='Cluster 4')

plt.scatter(X[y_kmeans == 4]['Annual Income (k$)'],
            X[y_kmeans == 4]['Spending Score (1-100)'],
            s=50, label='Cluster 5')

# Plot centroids
plt.scatter(kmeans.cluster_centers_[:,0],
            kmeans.cluster_centers_[:,1],
            s=200,
            c='red',
            label='Centroids')

plt.title("Customer Segmentation using K-Means")
plt.xlabel("Annual Income (k$)")
plt.ylabel("Spending Score (1-100)")
plt.legend()

plt.savefig("images/customer_clusters.png")
plt.show()

# ---------------- SAVE RESULTS ----------------
data.to_csv("Customer_Segmentation_Result.csv", index=False)

print("\nCluster results saved to Customer_Segmentation_Result.csv")

# ---------------- CLUSTER SUMMARY ----------------
cluster_summary = data.groupby('Cluster')[['Annual Income (k$)', 'Spending Score (1-100)']].mean()

print("\nCluster Summary (Average Values):")
print(cluster_summary)