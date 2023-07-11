from Src.DSL.expr import Expression
from Src.SQLFeatures.WHERE import WHERE


# from Src.SQLFeatures.QWhere import QueryWhere


class GROUP_BY():
    order_by_query = []

    def __init__(self):

        self.where = WHERE()
        self.queries = self.where.queries
        self.output_columns_name = self.where.expression.checker.io.output_columns_name
        self.table_name = self.where.expression.checker.io.table_name
        self.different_columns = self.where.different_columns
        self.same_column = self.where.exp_check.same_column


    def group_by(self):

        if len(self.table_name) == 1:
            if len(self.different_columns) == 0:
                self.where.select()
                return self.queries

            if len(self.different_columns) > 0:
                self.where.select()
                if len(self.output_columns_name) > 0:
                    ind = len(self.queries) - 1
                    for index in range(len(self.queries)):
                        self.queries.append(
                            f"{self.queries[index][:-1]} GROUP BY {(',').join(self.output_columns_name)};")
                    while ind >= 0:
                        index = 0
                        self.queries.pop(index)
                        ind -= 1

                return self.queries

        if len(self.table_name) > 1:
            if len(self.different_columns) == 0:
                self.where.where()
                return self.queries

            if len(self.different_columns) > 0:

                self.where.where()
                ind = len(self.queries) - 1
                for index in range(len(self.queries)):
                    self.queries.append(
                        f"{self.queries[index][:-1]} GROUP BY {(',').join(self.output_columns_name)};")
                while ind >= 0:
                    index = 0
                    self.queries.pop(index)
                    ind -= 1

                return self.queries

    def orderby(self, column):

        for index in range(len(self.queries)):
            self.order_by_query.append(f"{self.queries[index][:-1]} ORDER BY {column};")


        return self.order_by_query


# i = GROUP_BY()
#
# i.group_by()
#
# print(i.queries)
