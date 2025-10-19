"""
DAG: Primeira Pipeline
Descrição: Pipeline simples com 3 tarefas sequenciais
Autor: Andre Luiz
Data: 2025-10-19
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator


# ============================================
# FUNÇÕES DAS TAREFAS
# ============================================

def primeira_atividade():
    """Primeira atividade da pipeline"""
    print("=" * 50)
    print("Esta é a primeira atividade.")
    print("Executando processamento inicial...")
    print("=" * 50)


def segunda_atividade():
    """Segunda atividade da pipeline"""
    print("=" * 50)
    print("Esta é a segunda atividade.")
    print("Executando processamento intermediário...")
    print("=" * 50)


def terceira_atividade():
    """Terceira atividade da pipeline"""
    print("=" * 50)
    print("Esta é a terceira atividade.")
    print("Executando processamento final...")
    print("=" * 50)


# ============================================
# CONFIGURAÇÕES PADRÃO DA DAG
# ============================================

default_args = {
    'owner': 'andre_luiz',
    'depends_on_past': False,
    'email': ['admin@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2025, 10, 19),
}


# ============================================
# DEFINIÇÃO DA DAG
# ============================================

with DAG(
    dag_id='primeira_pipeline',
    default_args=default_args,
    description='Pipeline simples com 3 tarefas sequenciais',
    schedule_interval='@daily',  # Executa diariamente
    catchup=False,
    tags=['exemplo', 'tutorial', 'python'],
) as dag:

    # ============================================
    # DEFINIÇÃO DAS TAREFAS
    # ============================================

    task_1 = PythonOperator(
        task_id='primeira_atividade',
        python_callable=primeira_atividade,
        doc_md="""
        ### Primeira Atividade
        Esta tarefa executa o processamento inicial da pipeline.
        """,
    )

    task_2 = PythonOperator(
        task_id='segunda_atividade',
        python_callable=segunda_atividade,
        doc_md="""
        ### Segunda Atividade
        Esta tarefa executa o processamento intermediário da pipeline.
        """,
    )

    task_3 = PythonOperator(
        task_id='terceira_atividade',
        python_callable=terceira_atividade,
        doc_md="""
        ### Terceira Atividade
        Esta tarefa executa o processamento final da pipeline.
        """,
    )

    # ============================================
    # DEPENDÊNCIAS (ORDEM DE EXECUÇÃO)
    # ============================================

    task_1 >> task_2 >> task_3