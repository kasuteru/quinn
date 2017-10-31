import pytest

from quinn.spark import *
from quinn.extensions import *
from .dataframe_transformations import *

from pyspark.sql.functions import col

class TestDataFrameExt(object):

    def test_transform_with_lambda(self):
        data = [("jose", 1), ("li", 2), ("luisa", 3)]
        source_df = spark.createDataFrame(data, ["name", "age"])

        actual_df = source_df.transform(lambda df: df.withColumn("age_times_two", col("age") * 2))

        expected_data = [("jose", 1, 2), ("li", 2, 4), ("luisa", 3, 6)]
        expected_df = spark.createDataFrame(expected_data, ["name", "age", "age_times_two"])

        assert(expected_df.collect() == actual_df.collect())

    def test_transform_with_no_arg_fun(self):
        data = [("jose", 1), ("li", 2), ("luisa", 3)]
        source_df = spark.createDataFrame(data, ["name", "age"])

        actual_df = source_df.transform(lambda df: with_greeting(df))

        expected_data = [("jose", 1, "hi"), ("li", 2, "hi"), ("luisa", 3, "hi")]
        expected_df = spark.createDataFrame(expected_data, ["name", "age", "greeting"])

        assert(expected_df.collect() == actual_df.collect())

    def test_transform_with_one_arg_fun(self):
        data = [("jose", 1), ("li", 2), ("luisa", 3)]
        source_df = spark.createDataFrame(data, ["name", "age"])

        actual_df = source_df.transform(lambda df: with_something(df, "crazy"))

        expected_data = [("jose", 1, "crazy"), ("li", 2, "crazy"), ("luisa", 3, "crazy")]
        expected_df = spark.createDataFrame(expected_data, ["name", "age", "something"])

        assert(expected_df.collect() == actual_df.collect())

    def test_chain_transforms(self):
        data = [("jose", 1), ("li", 2), ("luisa", 3)]
        source_df = spark.createDataFrame(data, ["name", "age"])

        actual_df = source_df\
            .transform(lambda df: with_greeting(df))\
            .transform(lambda df: with_something(df, "crazy"))

        expected_data = [("jose", 1, "hi", "crazy"), ("li", 2, "hi", "crazy"), ("luisa", 3, "hi", "crazy")]
        expected_df = spark.createDataFrame(expected_data, ["name", "age", "greeting", "something"])
        assert(expected_df.collect() == actual_df.collect())

    def test_transform_with_closure(self):
        data = [("jose", 1), ("li", 2), ("luisa", 3)]
        source_df = spark.createDataFrame(data, ["name", "age"])

        actual_df = (source_df
             .transform(with_greeting)  # no lambda required
             .transform(with_funny("haha")))

        expected_data = [
            ("jose", 1, "hi", "haha"),
            ("li", 2, "hi", "haha"),
            ("luisa", 3, "hi", "haha")
        ]
        expected_df = spark.createDataFrame(expected_data, ["name", "age", "greeting", "funny"])
        assert(expected_df.collect() == actual_df.collect())