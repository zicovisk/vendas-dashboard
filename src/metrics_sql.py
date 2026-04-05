import sqlite3
import pandas as pd


def query(db_path: str, sql: str) -> pd.DataFrame:
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df


def receita_total(db_path: str) -> float:
    df = query(db_path, "SELECT ROUND(SUM(receita), 2) AS total FROM vendas")
    return df["total"].iloc[0]


def lucro_total(db_path: str) -> float:
    df = query(db_path, "SELECT ROUND(SUM(lucro), 2) AS total FROM vendas")
    return df["total"].iloc[0]


def total_transacoes(db_path: str) -> int:
    df = query(db_path, "SELECT COUNT(*) AS total FROM vendas")
    return int(df["total"].iloc[0])


def produto_mais_vendido(db_path: str) -> str:
    df = query(db_path, """
        SELECT produto
        FROM vendas
        GROUP BY produto
        ORDER BY SUM(quantidade) DESC
        LIMIT 1
    """)
    return df["produto"].iloc[0]


def vendas_por_produto(db_path: str) -> pd.DataFrame:
    return query(db_path, """
        SELECT
            produto,
            ROUND(SUM(receita), 2)   AS receita_total,
            ROUND(SUM(lucro), 2)     AS lucro_total,
            SUM(quantidade)          AS quantidade_total
        FROM vendas
        GROUP BY produto
        ORDER BY receita_total DESC
    """)


def vendas_por_periodo(db_path: str) -> pd.DataFrame:
    return query(db_path, """
        SELECT
            SUBSTR(data, 1, 7)       AS mes,
            ROUND(SUM(receita), 2)   AS receita,
            ROUND(SUM(lucro), 2)     AS lucro
        FROM vendas
        GROUP BY mes
        ORDER BY mes
    """)


def margem_por_produto(db_path: str) -> pd.DataFrame:
    return query(db_path, """
        SELECT
            produto,
            ROUND(SUM(receita), 2)                          AS receita_total,
            ROUND(SUM(lucro), 2)                            AS lucro_total,
            ROUND(SUM(lucro) * 100.0 / SUM(receita), 1)    AS margem_pct
        FROM vendas
        GROUP BY produto
        ORDER BY margem_pct DESC
    """)


def vendas_filtradas(db_path: str, data_inicio: str, data_fim: str) -> pd.DataFrame:
    return query(db_path, f"""
        SELECT *
        FROM vendas
        WHERE data >= '{data_inicio}'
          AND data <= '{data_fim}'
    """)