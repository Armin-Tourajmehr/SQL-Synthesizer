from Src.DSL.expr import Expression
from Src.CheckNamecColumns.IOSubsetRelationship import Checker


class Aggregation():

    def __init__(self):
        self.checker = Checker()
        self.different_columns = self.checker.different_columns
        self.integer_columns = self.checker.integer_columns
        self.agg_queries = self.checker.io.agg_queries

    def min(self, col):
        return f' MIN({col}) AS {self.different_columns[0]}'

    def max(self, col):
        return f' MAX({col}) AS {self.different_columns[0]}'

    def avg(self, col):
        return f' AVG({col}) AS {self.different_columns[0]}'

    def sum(self, col):
        return f' SUM({col}) AS {self.different_columns[0]}'

    def count(self, col):
        return f' COUNT({col}) AS {self.different_columns[0]}'



    def generate_agg(self):
        for col in self.integer_columns:
            self.agg_queries.append(self.min(col))
            self.agg_queries.append(self.max(col))
            self.agg_queries.append(self.avg(col))
            self.agg_queries.append(self.sum(col))
            self.agg_queries.append(self.count(col))
        self.agg_queries.append(self.count('*'))
        return self.agg_queries

# i = Aggregation()
#
# i.generate_agg()
# print(i.integer_columns)
# print(i.different_columns)
# print(i.agg_queries)
