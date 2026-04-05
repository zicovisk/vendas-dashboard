import sqlite3
import pandas as pd 
import os 

def criar_base_de_dados(csv_path: str, db_path: str):
    """
    Lê o CSV de vendas e cria uma base de dados SQLite.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Ficheiro não encontrado: {csv_path}")

    # Carregar o CSV
    df = pd.read_csv(csv_path)

    # Calcular colunas derivadas
    df["receita"] = df["quantidade"] * df["preco_unitario"]
    df["custo_total"] = df["quantidade"] * df["custo_unitario"]
    df["lucro"] = df["receita"] - df["custo_total"]

    # Criar a base de dados e inserir os dados
    conn = sqlite3.connect(db_path)
    df.to_sql("vendas", conn, if_exists="replace", index=False)
    conn.close()

    print(f"✅ Base de dados criada em: {db_path}")
    print(f"   Registos inseridos: {len(df)}")


if __name__ == "__main__":
    criar_base_de_dados("data/vendas.csv", "data/vendas.db")

