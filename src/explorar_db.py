import sqlite3

def executar_query(db_path: str, query: str):
    """Executa uma query SQL e mostra os resultados."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(query)
    colunas = [desc[0] for desc in cursor.description]
    resultados = cursor.fetchall()
    conn.close()
    return colunas, resultados

def mostrar(colunas, resultados):
    """Mostra os resultados de forma legível."""
    print(" | ".join(colunas))
    print("-" * 60)
    for linha in resultados:
        print(" | ".join(str(v) for v in linha))
    print()


db = "data/vendas.db"

# QUERY 1 — SELECT básico
print("📋 QUERY 1: Ver todas as vendas")
cols, rows = executar_query(db, """
    SELECT data, produto, quantidade, receita, lucro
    FROM vendas
""")
mostrar(cols, rows)

# QUERY 2 — WHERE
print("🔍 QUERY 2: Vendas com lucro acima de €50")
cols, rows = executar_query(db, """
    SELECT produto, quantidade, receita, lucro
    FROM vendas
    WHERE lucro > 50
""")
mostrar(cols, rows)

# QUERY 3 — GROUP BY + SUM
print("📦 QUERY 3: Receita total por produto")
cols, rows = executar_query(db, """
    SELECT produto, 
           SUM(quantidade) AS total_unidades,
           ROUND(SUM(receita), 2) AS receita_total,
           ROUND(SUM(lucro), 2) AS lucro_total
    FROM vendas
    GROUP BY produto
    ORDER BY receita_total DESC
""")
mostrar(cols, rows)

# QUERY 4 — GROUP BY por mês
print("📅 QUERY 4: Receita por mês")
cols, rows = executar_query(db, """
    SELECT SUBSTR(data, 1, 7) AS mes,
           ROUND(SUM(receita), 2) AS receita,
           ROUND(SUM(lucro), 2) AS lucro
    FROM vendas
    GROUP BY mes
    ORDER BY mes
""")
mostrar(cols, rows)