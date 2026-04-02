import pandas as pd


def receita_total(df: pd.DataFrame) -> float:
    """Retorna a receita total de todas as vendas."""
    return df["receita"].sum()


def lucro_total(df: pd.DataFrame) -> float:
    """Retorna o lucro total de todas as vendas."""
    return df["lucro"].sum()


def total_transacoes(df: pd.DataFrame) -> int:
    """Retorna o número total de transações."""
    return len(df)


def produto_mais_vendido(df: pd.DataFrame) -> str:
    """Retorna o nome do produto com maior quantidade vendida."""
    return (
        df.groupby("produto")["quantidade"]
        .sum()
        .idxmax()
    )


def vendas_por_produto(df: pd.DataFrame) -> pd.DataFrame:
    """
    Retorna um resumo de receita e lucro por produto,
    ordenado por receita decrescente.
    """
    return (
        df.groupby("produto")
        .agg(
            receita_total=("receita", "sum"),
            lucro_total=("lucro", "sum"),
            quantidade_total=("quantidade", "sum")
        )
        .sort_values("receita_total", ascending=False)
        .reset_index()
    )


def vendas_por_periodo(df: pd.DataFrame) -> pd.DataFrame:
    """
    Retorna receita e lucro agrupados por mês.
    """
    df = df.copy()
    df["mes"] = df["data"].dt.to_period("M").astype(str)
    return (
        df.groupby("mes")
        .agg(
            receita=("receita", "sum"),
            lucro=("lucro", "sum")
        )
        .reset_index()
    )


def margem_por_produto(df: pd.DataFrame) -> pd.DataFrame:
    """
    Retorna a margem de lucro percentual por produto.
    Margem = lucro / receita * 100
    """
    resumo = vendas_por_produto(df)
    resumo["margem_pct"] = (
        resumo["lucro_total"] / resumo["receita_total"] * 100
    ).round(1)
    return resumo[["produto", "receita_total", "lucro_total", "margem_pct"]]


if __name__ == "__main__":
    # Teste direto
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from src.load_data import load_vendas

    df = load_vendas("data/vendas.csv")

    print(f"💰 Receita total:       €{receita_total(df):.2f}")
    print(f"📈 Lucro total:         €{lucro_total(df):.2f}")
    print(f"🧾 Total transações:    {total_transacoes(df)}")
    print(f"🏆 Produto mais vendido: {produto_mais_vendido(df)}")
    print()
    print("📦 Vendas por produto:")
    print(vendas_por_produto(df).to_string(index=False))
    print()
    print("📅 Vendas por período:")
    print(vendas_por_periodo(df).to_string(index=False))
    print()
    print("📊 Margem por produto:")
    print(margem_por_produto(df).to_string(index=False))