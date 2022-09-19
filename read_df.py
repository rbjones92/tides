# Robert Jones
# 9.18.22
# Read and Transform tides_df

from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import from_unixtime, unix_timestamp, col
from pyspark.sql.functions import concat_ws
from pyspark.sql.functions import to_timestamp
from pyspark.sql.functions import regexp_extract
from pyspark.sql import functions as F


spark = SparkSession.builder.getOrCreate()


schema = StructType([ 
    StructField("index", IntegerType(), True), \
    StructField("date", StringType(), True), \
    StructField("dotw", StringType(), True), \
    StructField("time", StringType(), True), \
    StructField("predicted(ft)", FloatType(), True), \
    StructField("hi_low", StringType(), True), \
])



def transpose_df():

    # Read dataframe
    df = spark.read.csv('C:/Users/Bob/Desktop/SpringBoard/Python_Projects/Tides/tide_df/tide_df.csv',schema=schema)
    # Convert 12 hour time to 24 hour time
    df = df.withColumn('time24',from_unixtime(unix_timestamp(col(('time')), "hh:mm aa"), "HH:mm"))
    # Combine date and time
    df = df.select(concat_ws(' ',df.date,df.time24).alias('datetime'),"index","dotw","predicted(ft)","hi_low")
    # Convert date and time to timestamp
    ts = to_timestamp('datetime',"yyyy/MM/dd HH:mm")
    df = df.withColumn('timestamp',ts)
    # Extract just time to query on it later
    df = df.withColumn('time',regexp_extract('datetime','\d{2}:\d{2}',0))
    # drop unncessary datetime
    df = df.drop('datetime')
    # drop duplicates
    df = df.drop_duplicates()

    return df


def query_dates():


    df = transpose_df()
    df = df.createOrReplaceTempView('tides')

    # No Weekends
    sql_statement = 'SELECT * FROM tides WHERE dotw != "Sat" AND dotw != "Sun"'
    df = spark.sql(sql_statement)

    # Low tide between 7am and 9am
    df = df.filter(F.col('time').between('07:00','09:00') & (df.hi_low == "L"))

    df = df.withColumn('date',df.timestamp.substr(1,10))

    df = df.select(df.dotw,df.date,'predicted(ft)')

    df = df.orderBy(df.date)

    df.coalesce(1).write.csv('C:/Users/Bob/Desktop/SpringBoard/Python_Projects/Tides/tide_df/tide_df.transform')

    df.show()




query_dates()