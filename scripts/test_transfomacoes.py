import unittest
from datetime import datetime

# Importa os módulos do PySpark necessários para criar DataFrames
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType, 
    StructField, 
    StringType, 
    DoubleType, 
    TimestampType
)

# Importa a função que será testada
# Nota: Certifique-se de que 'transformacoes.py' está no mesmo diretório 
# ou no caminho de importação do seu ambiente.
from transformacoes import tratamento_uniao_df 

class PySparkTestCase(unittest.TestCase):
    """
    Classe base para configurar e encerrar a SparkSession de forma eficiente 
    para todos os testes.
    """
    @classmethod
    def setUpClass(cls):
        try:
            # 1. Tenta usar a sessão global 'spark' (Databricks)
            cls.spark = spark 
        except NameError:
            # 2. Se 'spark' não estiver definido (ambiente local), cria uma nova
            from pyspark.sql import SparkSession
            cls.spark = SparkSession.builder \
                .appName("UnitTestSpark") \
                .master("local[*]") \
                .config("spark.connect.enabled", "false")\
                .getOrCreate()

    @classmethod
    def tearDownClass(cls):
        """Encerra a SparkSession depois que todos os testes terminarem."""
        cls.spark.stop()

class TestProcessamentoDeCambio(PySparkTestCase):

    def test_transformacao_completa_e_filtragem(self):
        """
        Testa a função processar_taxas_cambiais verificando:
        1. Renomeação correta de colunas.
        2. Adição correta das colunas 'base_currency' e 'timestamp'.
        3. Remoção de taxas inválidas (<= 0 ou null) e da moeda base.
        """
        
        # --- ARRANJO (Setup) ---
        
        # Definindo os parâmetros externos
        taxa_base = "BRL"
        timestamp_teste = datetime(2025, 10, 27, 10, 30, 0)
        
        # Schema de ENTRADA (Como o DataFrame raw chega)
        schema_entrada = StructType([
            StructField("currency", StringType(), True),
            StructField("value", DoubleType(), True)
        ])
        
        # Dados de ENTRADA
        dados_entrada = [
            # 1. Caso Válido (Deve ser mantido)
            ("USD", 5.02),     
            # 2. Caso de Moeda Base (Deve ser filtrado)
            ("BRL", 1.0),      
            # 3. Caso de Taxa Zero (Deve ser filtrado)
            ("EUR", 0.0),      
            # 4. Caso de Taxa Negativa (Deve ser filtrado)
            ("JPY", -0.05),    
            # 5. Caso de Taxa Nula (Deve ser filtrado)
            ("GBP", None),     
            # 6. Outro Caso Válido
            ("CAD", 3.80)      
        ]
        
        df_entrada = self.spark.createDataFrame(dados_entrada, schema_entrada)
        
        
        # --- AÇÃO (Action) ---
        df_resultado = tratamento_uniao_df(
            df_entrada, 
            taxa_base, 
            timestamp_teste
        )
        
        
        # --- ASSERÇÃO (Assertion) ---
        
        # Schema de SAÍDA ESPERADO (Verifica nomes e tipos)
        schema_esperado = StructType([
            StructField("moeda", StringType(), True),
            StructField("taxa", DoubleType(), True),
            StructField("base_currency", StringType(), True),
            StructField("timestamp", TimestampType(), True)
        ])

        # Dados de SAÍDA ESPERADOS (Apenas USD e CAD sobreviveram ao filtro)
        dados_esperados = [
            ("USD", 5.02, taxa_base, timestamp_teste),
            ("CAD", 3.80, taxa_base, timestamp_teste)
        ]
        
        df_esperado = self.spark.createDataFrame(dados_esperados, schema_esperado)
        
        
        # 1. Verifica se o número de linhas está correto
        self.assertEqual(df_resultado.count(), 2, "Contagem de linhas falhou após o filtro.")

        # 2. Verifica se as colunas estão corretas
        colunas_esperadas = ["moeda", "taxa", "base_currency", "timestamp"]
        self.assertEqual(sorted(df_resultado.columns), sorted(colunas_esperadas), "Nomes das colunas falharam na renomeação/adição.")
        
        # 3. Verifica se os dados são idênticos (coleta e comparação)
        # Deve-se ordenar para garantir a comparação correta.
        resultado_coletado = df_resultado.sort('moeda').collect()
        esperado_coletado = df_esperado.sort('moeda').collect()
        
        self.assertEqual(resultado_coletado, esperado_coletado, "O conteúdo final do DataFrame não corresponde ao esperado.")


# ----------------------------------------------------------------------
# 3. Comando para Execução do Teste
# ----------------------------------------------------------------------

# Isso permite que você execute o arquivo diretamente a partir do terminal
if __name__ == '__main__':
    # 'exit=False' é usado para que o unittest.main não feche o terminal
    # imediatamente, o que é útil em alguns IDEs ou ambientes interativos.
    unittest.main(argv=['first-arg-is-ignored'], exit=False)