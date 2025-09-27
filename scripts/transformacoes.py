from pyspark.sql import DataFrame
from pyspark.sql import functions as F

def tratamento_uniao_df(df: DataFrame, rate: str, current_datetime: str):
  df = df.withColumn('base_currency', F.lit(rate).cast('string'))\
         .withColumn('timestamp', F.lit(current_datetime).cast('timestamp'))\
         .withColumnRenamed('currency', 'moeda')\
         .withColumnRenamed('value', 'taxa')\
         .withColumn('moeda', F.col('moeda').cast('string'))\
         .withColumn('taxa', F.col('taxa').cast('double'))\
         .filter(F.col('moeda') != rate)\
         .filter((F.col('taxa') > 0) & (F.col('taxa').isNotNull()))
  return df