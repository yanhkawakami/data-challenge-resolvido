from query import Query


_ATHENA_CLIENT = None


def create_hive_table_with_athena(query):
    '''
    Função necessária para criação da tabela HIVE na AWS
    :param query: Script SQL de Create Table (str)
    :return: None
    '''
    print(f"Query: {query}")
    response = _ATHENA_CLIENT.start_query_execution(
        QueryString=query,
        ResultConfiguration={
            'OutputLocation': 's3://iti-query-results/'
        }
    )

    print(_ATHENA_CLIENT.get_query_execution(
        QueryExecutionId=response["QueryExecutionId"]
    ))


def handler():
    '''
    #  Função principal
    Aqui você deve começar a implementar o seu código
    Você pode criar funções/classes à vontade
    Utilize a função create_hive_table_with_athena para te auxiliar
        na criação da tabela HIVE, não é necessário alterá-la
    '''
    query = Query()
    built_query = query.build_query()
    create_hive_table_with_athena(built_query)
