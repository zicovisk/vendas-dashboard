import pandas as pd
import os

def load_vendas(filepath: str) -> pd.DataFrame:
    """
    Carrega e limpa os dados de vendas a partir de um ficheiro CSV.
    
    Parâmetros:
        filepath: caminho para o ficheiro CSV
    
    Retorna:
        DataFrame limpo e pronto para análise
    """
    # Verificar se o ficheiro existe
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Ficheiro não encontrado: {filepath}")
    
    # Carregar o CSV
    df = pd.read_csv(filepath)
    
    # Converter a coluna de data para formato datetime
    df["data"] = pd.to_datetime(df["data"], format="%Y-%m-%d")
    
    # Remover linhas com valores nulos
    df = df.dropna()
    
    # Calcular colunas derivadas
    df["receita"] = df["quantidade"] * df["preco_unitario"]
    df["custo_total"] = df["quantidade"] * df["custo_unitario"]
    df["lucro"] = df["receita"] - df["custo_total"]
    
    return df


if __name__ == "__main__":
    # Teste direto: correr este ficheiro sozinho para verificar que funciona
    df = load_vendas("data/vendas.csv")
    print("✅ Dados carregados com sucesso!")
    print(f"   Linhas: {len(df)}")
    print(f"   Colunas: {list(df.columns)}")
    print(f"\nPrimeiras linhas:")
    print(df.head())
    print(f"\nReceita total: €{df['receita'].sum():.2f}")
    print(f"Lucro total:   €{df['lucro'].sum():.2f}")