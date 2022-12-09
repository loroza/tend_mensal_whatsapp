class PostgreSQL():

    pd = __import__('pandas')

    #Read PostgreSQL
    def read_postgres(name_table:str=None,
                      schema:str=None,
                      query:str='',
                      full_query:str='') -> pd.DataFrame:


        import psycopg2
        from psycopg2 import Error
        import pandas as pd

        import json

        with open('headers.json', encoding='utf-8') as meu_json:
            headers = json.load(meu_json)

        if len(full_query) >= 1:
            query_execute = full_query
        elif len(query) >= 1:
            query_execute = f'SELECT * FROM "{schema}".{name_table.upper()} {query}'
        else:
            query_execute = f'SELECT * FROM "{schema}".{name_table.upper()}'

        try:
            connection = psycopg2.connect(user=headers['user'],
                                          password=headers['password'],
                                          host=headers['host'],
                                          port=headers['port'],
                                          database=headers['database'])

            cursor = connection.cursor()

            cursor.execute(query_execute)

            result_query = cursor.fetchall()
            columns = [desc[0].upper() for desc in cursor.description]
            dataframe = pd.DataFrame(result_query, columns=columns)

        except (Exception, Error) as error:
            print('Error', error)

        finally:
            if (connection):
                cursor.close()
                connection.close()
        
        return dataframe