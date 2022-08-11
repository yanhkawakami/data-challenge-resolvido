from reader import SchemaRead


class CompareEventSchema:
    '''
    Classe responsável pelas comparações do evento com o schema
    :param schema_file_path: Path do schema
    '''
    def __init__(self, **kwargs) -> None:
        schema_file_path = kwargs.get("schema_file_path")
        schema_reader = SchemaRead(schema_file_path=schema_file_path)
        self._schema = schema_reader.get_columns_properties()

    def compare_size(self, event) -> bool:
        '''
        Responsável por comparar o tamanho do evento e do schema
        :param event:  Colunas e tipos do evento
        :param self._schema: Colunas e tipos do schema
        :return <boolean>
        '''
        return len(self._schema) == len(event)

    def compare_columns_properties(self, event) -> bool:
        '''
        Responsável por comparar a estrutura do evento e do schema,
        sendo colunas e tipos. Caso não sejam idênticas, retorna
        False
        :param event:  Colunas e tipos do evento
        :param self._schema: Colunas e tipos do schema
        :return <boolean>
        '''
        if self._schema == event:
            return True
        return False
