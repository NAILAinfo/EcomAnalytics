import pandas as pd
from sqlalchemy import create_engine
import dash
from dash import dcc, html
import plotly.express as px
from dash.dependencies import Input, Output

# Créez une connexion à la base de données MySQL
engine = create_engine("mysql+mysqlconnector://root:@localhost/table2 ecommerce client bhaviour")  # Adapté à votre configuration

# Récupérer les données depuis la base de données
query = "SELECT * FROM `table 2`"  
df = pd.read_sql(query, engine)

# Créez l'application Dash
app = dash.Dash(__name__)

# Graphique 1 : Répartition des clients par genre
gender_fig = px.pie(df, names='Gender', title="Répartition des clients par genre")

# Graphique 2 : Dépenses totales des clients par ville
spend_by_city_fig = px.bar(df, x='City', y='Total Spend', title="Dépenses totales par ville")

# Graphique 3 : Moyenne des évaluations des clients
avg_rating_fig = px.histogram(df, x='Average Rating', title="Distribution des évaluations moyennes")

# Graphique 4 : Répartition des types de membres
membership_fig = px.pie(df, names='Membership Type', title="Répartition des types de membres")

# Graphique 5 : Niveau de satisfaction des clients
satisfaction_fig = px.bar(df, x='Satisfaction Level', y='Total Spend', title="Relation entre satisfaction et dépenses")

# Définir la mise en page du dashboard
app.layout = html.Div([
    html.H1("Dashboard des Comportements des Clients"),
    
    html.Div([
        html.Div([dcc.Graph(figure=gender_fig)], className="six columns"),
        html.Div([dcc.Graph(figure=spend_by_city_fig)], className="six columns")
    ], className="row"),

    html.Div([
        html.Div([dcc.Graph(figure=avg_rating_fig)], className="six columns"),
        html.Div([dcc.Graph(figure=membership_fig)], className="six columns")
    ], className="row"),

    html.Div([dcc.Graph(figure=satisfaction_fig)], className="row")
])

# Exécuter le serveur Dash
if __name__ == '__main__':
    app.run_server(debug=True)