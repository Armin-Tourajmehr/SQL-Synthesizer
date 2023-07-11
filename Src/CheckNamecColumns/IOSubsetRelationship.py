from Src.IOTable.Input_output_table import IO


class Checker():
    same_column = ''
    table_candidate = []
    integer_columns = []
    different_columns = []
    flag = True

    def __init__(self):
        self.io = IO()
        self.out_col_extra = self.io.out_col_extra

    def check_columns(self):

        self.io.get_table()

        all_columns = []
        for colName in self.io.table_columns_name:
            for col in colName:
                all_columns.append(col)

        for col in all_columns:
            if all_columns.count(col) == 2:
                self.same_column = col

        for outputname in self.io.output_columns_name:
            for tableName, columnName in list(zip(self.io.table_name, self.io.table_columns_name)):
                if outputname in columnName and tableName not in self.table_candidate:
                    self.table_candidate.append(tableName)

            if outputname not in all_columns:
                self.different_columns.append(outputname)
                index = self.io.output_columns_name.index(outputname)
                self.io.output_columns_name.pop(index)

        for columnName, typeName in list(zip(self.io.table_columns_name, self.io.type_columns)):
            for col, typ in list(zip(columnName, typeName)):
                if col == self.same_column:
                    continue
                else:
                    if typ == 'int':
                        if col not in self.integer_columns and col not in self.io.output_columns_name:
                            self.integer_columns.append(col)


#
# i = Checker()
#
# i.check_columns()
# print(i.io.table_name)
# print(i.table_candidate)
# print(i.integer_columns)
# print(i.different_columns)
# print(i.same_column)
