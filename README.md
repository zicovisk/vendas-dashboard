# 📊 Dashboard de Vendas

Dashboard interativo de análise de vendas construído com Python, SQLite e Streamlit.

🔗 **[Ver dashboard ao vivo](https://vendas-dashboard-jsszot9bwhv7jqlsmcadlv.streamlit.app/)**

---

## 📌 Sobre o Projecto

Este projecto foi construído como parte de um plano de desenvolvimento técnico focado em dados e arquitetura de software. O objectivo foi criar uma solução real que responda a perguntas de negócio concretas a partir de dados de vendas.

**Perguntas respondidas pelo dashboard:**
- Qual é a receita e lucro total no período?
- Qual o produto mais lucrativo?
- Como evoluíram as vendas mês a mês?
- Qual a margem de lucro por produto?

---

## 🛠️ Stack Tecnológica

| Tecnologia | Função |
|------------|--------|
| Python 3.9 | Lógica, limpeza e cálculo de métricas |
| Pandas | Manipulação de dados |
| SQLite | Base de dados local |
| Plotly | Gráficos interativos |
| Streamlit | Interface do dashboard |
| Git + GitHub | Controlo de versão |

---

## 🏗️ Arquitectura do Projecto
```
vendas-dashboard/
│
├── data/
│   └── vendas.csv          ← dados de vendas
│
├── src/
│   ├── setup_db.py         ← cria a base de dados SQLite
│   ├── metrics_sql.py      ← métricas calculadas via SQL
│   └── explorar_db.py      ← queries SQL de exploração
│
├── app.py                  ← dashboard Streamlit
├── requirements.txt
└── README.md
```

O projecto segue o princípio de **separação de responsabilidades**:
- `setup_db.py` — responsável pelo INPUT e criação da base de dados
- `metrics_sql.py` — responsável pelo PROCESSAMENTO via SQL
- `app.py` — responsável pelo OUTPUT visual

---

## 📈 Funcionalidades

- **4 KPIs no topo** — receita total, lucro total, nº de transações, produto mais lucrativo
- **Filtro por período** — todos os KPIs e gráficos actualizam em tempo real
- **Gráfico de barras** — receita por produto ordenada por valor
- **Gráfico de linha** — evolução mensal de receita e lucro
- **Tabela de margens** — margem percentual por produto ordenada por rentabilidade

---

## 🚀 Como Correr Localmente
```bash
# Clonar o repositório
git clone https://github.com/zicovisk/vendas-dashboard.git
cd vendas-dashboard

# Instalar dependências
pip install -r requirements.txt

# Correr o dashboard
python3 -m streamlit run app.py
```

---

## 💡 Decisões Técnicas

**Porquê SQLite em vez de só Pandas?**
As métricas são calculadas directamente na base de dados via SQL — o mesmo padrão usado em sistemas reais em empresas. O Pandas é usado apenas para transporte de dados entre a base de dados e o Streamlit.

**Porquê módulos separados?**
Cada ficheiro tem uma responsabilidade única. Isso permite alterar a fonte de dados, os cálculos ou a interface de forma independente — sem quebrar o resto do sistema.

---

## 👤 Autor

**Lucas R. Bastos**
Estratégias Digitais | Dados | Automação com IA

🔗 [Portfolio](https://lrdigital-card.netlify.app/)