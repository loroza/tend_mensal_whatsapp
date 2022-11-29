class PostgreSQL():

    pd = __import__('pandas')

    #Read PostgreSQL
    def read_postgres(name_table:str=None,
                      schema:str=None,
                      database:str='postgres',
                      user:str='pecista',
                      password:str='bueno123',
                      host:str='10.4.1.96',
                      port:str='5432',
                      query:str='',
                      full_query:str='') -> pd.DataFrame:


        import psycopg2
        from psycopg2 import Error
        import pandas as pd

        if len(full_query) >= 1:
            query_execute = full_query
        elif len(query) >= 1:
            query_execute = f'SELECT * FROM "{schema}".{name_table.upper()} {query}'
        else:
            query_execute = f'SELECT * FROM "{schema}".{name_table.upper()}'

        try:
            connection = psycopg2.connect(user=user,
                                          password=password,
                                          host=host,
                                          port=port,
                                          database=database)

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