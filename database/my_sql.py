import mysql.connector


# Establish connection to the MySQL server
class Database:

    def __init__(self):
        self.connection = mysql.connector.connect(user='root', password='Armin(2500)',
                                                  host='127.0.0.1')
        self.cursor = self.connection.cursor()

    def remove_database(self):

        self.cursor.execute("SHOW DATABASES")
        databases = [database[0] for database in self.cursor]
        if 'synthesizer' in databases:
            self.cursor.execute("DROP DATABASE synthesizer")
            print("The 'synthesizer' database has been dropped.")

    def create_database(self):
        # Drop the 'synthesizer' database

        self.cursor.execute("SHOW DATABASES")
        databases = [database[0] for database in self.cursor]
        if 'synthesizer' in databases:
            ask = input('Synthesizer database exists, do you want to drop it? ')
            if ask == 'yes':
                self.cursor.execute("DROP DATABASE synthesizer")
                print("The 'synthesizer' database has been deleted.")

        self.cursor.execute("SHOW DATABASES")
        databases = [database[0] for database in self.cursor]
        if 'synthesizer' not in databases:
            ask = input('Do you want to create database? ')
            if ask == 'yes':
                # Create the 'synthesizer' database
                self.cursor.execute("CREATE DATABASE synthesizer")
                print("The 'synthesizer' database has been created.")
        self.cursor.execute('use synthesizer')

    # Close the cursor and connection
    def insert_tables(self, tables):
        self.cursor.execute('use synthesizer')
        try:
            for table in tables:
                table_name, columns, column_types, values = table
                column_definitions = ', '.join([f'{col} {col_type}' for col, col_type in zip(columns, column_types)])
                create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions})"
                self.cursor.execute(create_table_query)
                print(f"Table '{table_name}' inserted successfully.")

                insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"
                self.cursor.executemany(insert_query, values)
                print(f"Values inserted into table '{table_name}' successfully.")

            self.connection.commit()
        except mysql.connector.Error as err:
            print("Error inserting tables:", err)

    def check_query(self, generate_query, output_value):
        queries = generate_query
        flat_output = []
        for row in output_value:
            for r in row:
                if r.isdigit():
                    r = int(r)
                    flat_output.append([r])
                else:
                    flat_output.append([r])
        flat_output = [list(item) for item in zip(*flat_output)]
        for query in queries:
            try:
                self.cursor.execute(query)
                rows = self.cursor.fetchall()
                flat_row = []
                for row in rows:
                    for r in row:
                        flat_row.append([r])
                flat_row = [list(item) for item in zip(*flat_row)]
                if flat_row == flat_output:
                    return query

            except mysql.connector.Error as err:
                print(f"Error executing query: {query}\n{err}")
                continue
        return f'Query not found'

    def close_database(self):
        self.cursor.close()
        self.connection.close()


