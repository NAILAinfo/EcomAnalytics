import pandas as pd
from sqlalchemy import create_engine
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from mlxtend.frequent_patterns import apriori, association_rules

# --- Configuration MySQL ---
engine = create_engine("mysql+mysqlconnector://root:@localhost/table2 ecommerce client bhaviour")

# --- SEGMENTATION DES CLIENTS AVEC K-MEANS ---
# Charger les données depuis la table
query = """
SELECT CustomerID, SUM(TotalSales) AS TotalSpending, COUNT(InvoiceID) AS TransactionCount
FROM fact_sales
GROUP BY CustomerID
"""
customer_data = pd.read_sql(query, engine)

# Normaliser les données pour K-Means
scaler = StandardScaler()
data_scaled = scaler.fit_transform(customer_data[['TotalSpending', 'TransactionCount']])

# Appliquer l'algorithme K-Means
kmeans = KMeans(n_clusters=3, random_state=42)
customer_data['Cluster'] = kmeans.fit_predict(data_scaled)

# Visualisation des clusters
plt.figure(figsize=(8, 6))
plt.scatter(
    customer_data['TotalSpending'], 
    customer_data['TransactionCount'], 
    c=customer_data['Cluster'], cmap='viridis'
)
plt.title("Segmentation des Clients")
plt.xlabel("Dépenses Totales (TotalSpending)")
plt.ylabel("Nombre de Transactions (TransactionCount)")
plt.colorbar(label="Cluster")
plt.show()

# Exporter les résultats dans une nouvelle table SQL
customer_data.to_sql("customer_segmentation", con=engine, if_exists='replace', index=False)
print("Segmentation des clients enregistrée dans la table 'customer_segmentation'.")

# --- RÈGLES D'ASSOCIATION AVEC APRIORI ---
# Charger les données transactionnelles
query = "SELECT InvoiceID, StockCode FROM fact_sales"
transaction_data = pd.read_sql(query, engine)

# Transformer les données en format binaire pour Apriori
basket = transaction_data.pivot_table(
    index='InvoiceID', columns='StockCode', aggfunc=lambda x: 1, fill_value=0
)

# Appliquer l'algorithme Apriori
frequent_itemsets = apriori(basket, min_support=0.05, use_colnames=True)

# Générer les règles d'association
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)

# Afficher les règles
print("\n--- Règles d'Association ---")
print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']])

# Exporter les règles dans une table SQL
rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].to_sql(
    "association_rules", con=engine, if_exists='replace', index=False
)
print("Règles d'association enregistrées dans la table 'association_rules'.")