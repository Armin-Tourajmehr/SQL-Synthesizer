from Src.SQLFeatures.GROUP_BY import GROUP_BY
from database.my_sql import Database

class Synthesizer:
    database = Database()
    result = ''
    def __init__(self):
        # Instance

        self.groupby = GROUP_BY()

        # Variable
        self.queries = self.groupby.where.exp_io.queries

    def run(self):

        self.groupby.group_by()
        self.zip_info = self.groupby.where.exp_io.zip_info
        self.output_value = self.groupby.where.exp_io.output_values

        order = input('Do you want to sort your column: ')
        if order == 'yes':
            column = input('which column? ')
            self.orderby_query = self.groupby.orderby(column)
            self.queries = self.orderby_query

        self.database.insert_tables(self.zip_info)

        self.result = self.database.check_query(self.queries,self.output_value)
    def close(self):
        ask = input('Do you want to remove synthesizer database? ')
        if ask == 'yes':
            self.database.remove_database()

        try:
            self.database.close_database()
        except:
            print('There is not any connection')


synthesizer = Synthesizer()
synthesizer.run()
print(synthesizer.queries)
print(synthesizer.result)
synthesizer.close()