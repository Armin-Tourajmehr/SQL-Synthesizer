from Src.CheckNamecColumns.IOSubsetRelationship import Checker


class Expression():
    def __init__(self):
        self.checker = Checker()
        self.check_io = self.checker.io
        self.checker.check_columns()

    def cexpr(self):
        if self.checker.flag:
            columns = ','.join(col for col in self.checker.io.output_columns_name)
            return columns



# i = Expression()
#
# print(i.cexpr())
