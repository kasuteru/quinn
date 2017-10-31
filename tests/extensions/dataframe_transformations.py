from pyspark.sql.functions import lit

def with_greeting(df):
    return df.withColumn("greeting", lit("hi"))

def with_something(df, something):
    return df.withColumn("something", lit(something))

def with_funny(word):
    def inner(df):
        return df.withColumn("funny", lit(word))
    return inner