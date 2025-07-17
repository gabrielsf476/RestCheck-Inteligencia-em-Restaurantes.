from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
from joblib import dump, load
import pandas as pd

def treinar(df, caminho_modelo="modelo.pkl"):
    df_treino = pd.get_dummies(df.copy(), columns=['prato'])
    X = df_treino.drop(columns=['quantidade', 'data'], errors='ignore').select_dtypes(include=[np.number]).fillna(0)
    y = df_treino['quantidade']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    modelo = RandomForestRegressor(random_state=42)
    modelo.fit(X_train, y_train)
    dump(modelo, caminho_modelo)
    rmse = np.sqrt(mean_squared_error(y_test, modelo.predict(X_test)))
    r2 = r2_score(y_test, modelo.predict(X_test))
    return modelo, rmse, r2

def prever(df, modelo_path="modelo.pkl"):
    modelo = load(modelo_path)
    df_encoded = pd.get_dummies(df.copy(), columns=['prato'])
    for col in modelo.feature_names_in_:
        if col not in df_encoded.columns:
            df_encoded[col] = 0
    X_pred = df_encoded.drop(columns=['quantidade', 'data'], errors='ignore').select_dtypes(include=[np.number]).fillna(0)
    X_pred = X_pred.reindex(columns=modelo.feature_names_in_, fill_value=0)
    y_pred = modelo.predict(X_pred)
    return pd.Series(y_pred.astype(int), name="quantidade_prevista")

