from Src.DSL.expr import Expression


class SELECT():
    def __init__(self):
        self.expression = Expression()
        self.table_candidate = self.expression.checker.table_candidate
        self.exp_io = self.expression.check_io
        self.cexpr = self.expression.cexpr

    def select(self):


        if len(self.table_candidate) >= 1:
            for length in range(len(self.table_candidate) + 1):

                for num in range(length):
                    table_subset = self.table_candidate[num:length]
                    if len(table_subset) > 1:  # Select queries with more than one table
                        self.exp_io.where_queries.append(f'SELECT {self.cexpr()} FROM {",".join(table_subset)}')
                    else:
                        self.exp_io.where_queries.append(f'SELECT {self.cexpr()} FROM {",".join(table_subset)}')

# i = SELECT()
# i.select()
# print(i.expression.checker.io.queries)
