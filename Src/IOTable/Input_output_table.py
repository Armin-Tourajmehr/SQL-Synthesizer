from database.my_sql import Database
class IO:
    table_name = []
    size = 0
    out_col_extra = []
    output_name = ''
    output_columns_name = []
    user_hint = ''
    output_values = []
    table_columns_name = []
    values = []
    select_query = []
    type_columns = []
    output_type_column = []
    queries = []
    zip_info = []
    agg_queries = []

    def __init__(self):
        self.database = Database()

    def get_table(self):
        self.database.create_database()
        self.size = int(input(f'How many tables do you want? '))
        for num in range(self.size):
            self.table_name.append(input('Enter your table name: '))

            print('Enter column like this: age,name,id_number,....')
            print(f'Enter {self.table_name[num]} table columns:')
            self.table_columns_name.append(input('columns name: ').replace(" ", "").split(','))
            print("Enter type column, note that if your type is string, write 'varchar(15), for integer write 'int'")
            self.type_columns.append(input('Enter type of your columns: ').replace(" ", "").split(','))
            num_records = int(input(f'How many records do you want to add for {self.table_name[num]} table: '))
            temp = []
            print(f'Enter your values like these: david,25,male,...')
            for num in range(num_records):
                temp.append(input('Enter your values: ').replace(" ", "").split(','))

            self.values.append(temp)

            info = [(table, col, typ, val)for table, col, typ, val in zip(self.table_name, self.table_columns_name,  self.type_columns,  self.values)]
            self.zip_info = info
        print("Input 'yes' if you want to add hint")
        ask = input('any hint? ')
        if ask == 'yes':
            print("If there is any hint to help synthesizer,"
                  " add like this: table.columns(>,<,=,<=,>=,<>)value, separate by comma:"
                  "e.g ---> table.column>value or table.column='string'")
            hint = input('Hint: ').replace(" ", "").split(',')
            self.user_hint = hint


        self.get_output()

    def get_output(self):

        self.output_name = self.table_name.pop()

        self.output_columns_name = self.table_columns_name.pop()

        self.output_values = self.values.pop()

        self.output_type_column = self.type_columns.pop()
        self.zip_info.pop()

        self.size -= 1

# i = IO()
# i.get_table()
# print(i.zip_info)