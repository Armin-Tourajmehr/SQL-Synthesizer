from Src.DSL.expr import Expression
from Src.SQLFeatures.Aggregation import Aggregation
import itertools


class WHERE():
    conditions = []

    def __init__(self):
        self.expression = Expression()
        self.exp_check = self.expression.checker
        self.exp_io = self.expression.check_io
        self.table_candidate = self.expression.checker.table_candidate

        self.table_name = self.expression.check_io.table_name
        self.table_columns_name = self.expression.check_io.table_columns_name
        self.type_columns = self.expression.check_io.type_columns
        self.output_columns_name = self.expression.check_io.output_columns_name
        self.user_hint = self.expression.check_io.user_hint
        self.different_columns = self.exp_check.different_columns
        self.queries = self.exp_io.queries

        self.cexpr = self.expression.cexpr

        self.aggregation = Aggregation()

    def where(self):
        for table1 in self.table_name:
            for table2 in self.table_name:
                if table1 != table2:
                    for column1 in self.table_columns_name[self.table_name.index(table1)]:
                        for column2 in self.table_columns_name[self.table_name.index(table2)]:
                            if column1 == column2 and self.type_columns[self.table_name.index(table1)][
                                self.table_columns_name[self.table_name.index(table1)].index(column1)] == \
                                    self.type_columns[self.table_name.index(table2)][
                                        self.table_columns_name[self.table_name.index(table2)].index(column2)] and \
                                    self.type_columns[self.table_name.index(table1)][
                                        self.table_columns_name[self.table_name.index(table1)].index(
                                            column1)] == 'varchar(15)' and self.type_columns[self.table_name.index(table2)][
                                self.table_columns_name[self.table_name.index(table2)].index(column2)] == 'varchar(15)':
                                self.conditions.append(f"{table1}.{column1}={table2}.{column2}")

                            if column1 == column2 and self.type_columns[self.table_name.index(table1)][
                                self.table_columns_name[self.table_name.index(table1)].index(column1)] == \
                                    self.type_columns[self.table_name.index(table2)][
                                        self.table_columns_name[self.table_name.index(table2)].index(column2)] and \
                                    self.type_columns[self.table_name.index(table1)][
                                        self.table_columns_name[self.table_name.index(table1)].index(
                                            column1)] == 'int' and self.type_columns[self.table_name.index(table2)][
                                self.table_columns_name[self.table_name.index(table2)].index(column2)] == 'int':
                                self.conditions.append(f"{table1}.{column1}={table2}.{column2}")
                                self.conditions.append(f"{table1}.{column1}>{table2}.{column2}")
                                self.conditions.append(f"{table1}.{column1}<{table2}.{column2}")
                                self.conditions.append(f"{table1}.{column1} >= {table2}.{column2}")
                                self.conditions.append(f"{table1}.{column1} => {table2}.{column2}")
                                self.conditions.append(f"{table1}.{column1} <> {table2}.{column2}")

        index = int(len(self.conditions) / 2)
        self.conditions = self.conditions[:index]

        if len(self.different_columns) == 0:
            if len(self.user_hint) == 0:
                for cond in self.conditions:
                    self.queries.append(
                        f"SELECT {self.cexpr()} FROM {','.join(self.table_candidate)} WHERE {cond};")
                    self.queries.append(
                        f"SELECT DISTINCT {self.cexpr()} FROM {','.join(self.table_candidate)} WHERE {cond};")

            if len(self.user_hint) > 0:
                for cond in self.conditions:
                    for hint_comb in itertools.product(["AND", "OR"], repeat=len(self.user_hint)):
                        hint_condition = " ".join(
                            f"{hint} ({hint_val})" for hint, hint_val in zip(hint_comb, self.user_hint))
                        query = f"SELECT {self.cexpr()} FROM {','.join(self.table_name)} WHERE {cond} {hint_condition};"
                        query_distinct = f"SELECT DISTINCT {self.cexpr()} FROM {','.join(self.table_name)} WHERE {cond} {hint_condition};"
                        self.queries.append(query)
                        self.queries.append(query_distinct)

        if len(self.different_columns) > 0:
            self.generate_agg = self.aggregation.generate_agg()

            if len(self.user_hint) > 0:
                for cond in self.conditions:
                    for agg in self.generate_agg:
                        for hint_comb in itertools.product(["AND", "OR"], repeat=len(self.user_hint)):
                            hint_condition = " ".join(
                                f"{hint} ({hint_val})" for hint, hint_val in zip(hint_comb, self.user_hint))
                            query = f"SELECT {self.cexpr()},{agg} FROM {','.join(self.table_name)} WHERE {cond} {hint_condition};"
                            query_distinct = f"SELECT DISTINCT {self.cexpr()},{agg} FROM {','.join(self.table_name)} WHERE {cond} {hint_condition};"
                            self.queries.append(query)
                            self.queries.append(query_distinct)

            if len(self.user_hint) == 0:
                for cond in self.conditions:
                    for agg in self.generate_agg:
                        self.queries.append(
                            f"SELECT {self.cexpr()},{agg} FROM {','.join(self.table_candidate)} WHERE {cond};")
                        self.queries.append(
                            f"SELECT DISTINCT {self.cexpr()},{agg} FROM {','.join(self.table_candidate)} WHERE {cond};")

    def select(self):
        if len(self.different_columns) == 0:
            if len(self.user_hint) == 0:
                self.queries.append(f"SELECT {self.cexpr()} FROM {self.table_name[0]};")
                self.queries.append(f"SELECT DISTINCT {self.cexpr()} FROM {self.table_name[0]};")

            if len(self.user_hint) == 1:
                # for hint_comb in itertools.product(["","AND", "OR"], repeat=len(self.user_hint)):
                #     hint_condition = " ".join(
                #         f"{hint} ({hint_val})" for hint, hint_val in zip(hint_comb, self.user_hint))
                query = f"SELECT {self.cexpr()} FROM {self.table_name[0]} WHERE {self.user_hint[0]};"
                query_distinct = f"SELECT DISTINCT {self.cexpr()} FROM {self.table_name[0]} WHERE {self.user_hint[0]};"
                self.queries.append(query)
                self.queries.append(query_distinct)

            if len(self.user_hint) > 1:
                operators = ["AND", "OR"]

                for i in range(2 ** (len(self.user_hint) - 1)):
                    operator_comb = [operators[(i >> j) & 1] for j in range(len(self.user_hint) - 1)]
                    condition_comb = []
                    for j in range(len(self.user_hint)):
                        condition_comb.append(self.user_hint[j])
                        if j < len(operator_comb):
                            condition_comb.append(operator_comb[j])
                    query = f"SELECT {self.cexpr()} FROM {self.table_name[0]} WHERE {' '.join(condition_comb)};"
                    query_distinct = f"SELECT DISTINCT {self.cexpr()} FROM {self.table_name[0]} WHERE {' '.join(condition_comb)};"
                    self.queries.append(query)
                    self.queries.append(query_distinct)



        if len(self.different_columns) > 0:
            self.generate_agg = self.aggregation.generate_agg()
            if len(self.user_hint) == 0:
                for agg in self.generate_agg:
                    if len(self.output_columns_name) == 0:
                        self.queries.append(
                            f"SELECT {agg} FROM {self.table_name[0]};")
                    if len(self.output_columns_name) > 0:
                        self.queries.append(
                            f"SELECT {self.cexpr()},{agg} FROM {self.table_name[0]};")
                        self.queries.append(
                            f"SELECT DISTINCT {self.cexpr()},{agg} FROM {self.table_name[0]};")

            if len(self.user_hint) > 0:
                for agg in self.generate_agg:
                    operators = ["AND", "OR"]

                    for i in range(2 ** (len(self.user_hint) - 1)):
                        operator_comb = [operators[(i >> j) & 1] for j in range(len(self.user_hint) - 1)]
                        condition_comb = []
                        for j in range(len(self.user_hint)):
                            condition_comb.append(self.user_hint[j])
                            if j < len(operator_comb):
                                condition_comb.append(operator_comb[j])
                        if len(self.output_columns_name) == 0:
                            query = f"SELECT {agg} FROM {self.table_name[0]} WHERE {' '.join(condition_comb)};"
                            query_distinct = f"SELECT DISTINCT {agg} FROM {self.table_name[0]} WHERE {' '.join(condition_comb)};"
                            self.queries.append(query)
                            self.queries.append(query_distinct)
                        if len(self.output_columns_name) > 0:
                            query = f"SELECT {self.cexpr()},{agg} FROM {self.table_name[0]} WHERE {' '.join(condition_comb)};"
                            query_distinct = f"SELECT DISTINCT {self.cexpr()},{agg} FROM {self.table_name[0]} WHERE {' '.join(condition_comb)};"
                            self.queries.append(query)
                            self.queries.append(query_distinct)


# i = WHERE()
# i.where()
# print(i.queries)
