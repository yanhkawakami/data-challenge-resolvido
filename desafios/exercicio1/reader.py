import json


class SchemaRead:
    '''
    Classe responsável pelas tratativas dos dados do schema,
    realizando a preparação para comparar com o evento
    :param schema_file_path: Path do schema
    '''
    def __init__(self, **kwargs) -> None:
        self._schema_file_path = kwargs.get("schema_file_path")
        self.__read_schema()

    def __read_schema(self) -> None:
        '''
        Responsável por abrir o JSON do schema
        :param self.schema_file_path: Path do schema
        '''
        schema_file = open(self._schema_file_path)
        self._opened_json = json.load(schema_file)

    def get_sorted_columns_properties(self, columns_properties) -> dict:
        '''
        Responsável por ordenar as colunas do schema
        :param columns_properties: Colunas e tipos do schema
        :return <dict>
        '''
        sorted_dict = dict(sorted(columns_properties.items()))
        return sorted_dict

    def get_columns_properties(self) -> dict:
        '''
        Responsável extrair colunas e seus tipos a partir do schema
        :param self._opened_json: JSON aberto para leitura
        :return <dict>
        '''
        try:
            schema_properties = self._opened_json["properties"]
            columns_properties = {}
            for column, value in schema_properties.items():
                if column != "address":
                    columns_properties[column] = type(value["examples"][0])
                    continue
                v_properties = value["properties"]
                for subcolumn, subvalue in v_properties.items():
                    columns_properties[subcolumn] = type(
                        subvalue["examples"][0])
            sorted_columns_properties = \
                self.get_sorted_columns_properties(columns_properties)
            return sorted_columns_properties
        except Exception as e:
            raise RuntimeError("Impossible to extract Schema properties",
                               str(e))


class EventRead:
    '''
    Classe responsável pelas tratativas dos dados do evento,
    realizando a preparação para comparar com o schema
    '''
    def get_sorted_event_columns(self, event_columns_properties) -> dict:
        '''
        Responsável por ordenar as colunas do evento
        :param columns_properties: Colunas e tipos do evento
        :return <dict>
        '''
        sorted_dict = dict(sorted(event_columns_properties.items()))
        return sorted_dict

    def get_event_columns_properties(self, event) -> dict:
        '''
        Responsável extrair colunas e seus tipos a partir do evento
        :param event: evento recebido da fila
        :return <dict>
        '''
        try:
            event_columns_properties = {}
            for column, value in event.items():
                if column != "address":
                    event_columns_properties[column] = type(value)
                    continue
                for subcolumn, subvalue in value.items():
                    event_columns_properties[subcolumn] = type(subvalue)
            sorted_columns_properties = \
                self.get_sorted_event_columns(event_columns_properties)
            return sorted_columns_properties
        except Exception as e:
            raise RuntimeError("Impossible to extract Schema properties",
                               str(e))
