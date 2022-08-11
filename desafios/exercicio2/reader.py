import json


class SchemaRead:
    '''
    Classe responsável pelas tratativas dos dados do schema,
    realizando a preparação para comparar com o evento
    :param schema_file_path: Path do schema
    '''
    def __init__(self, **kwargs) -> None:
        self._schema_file_path = kwargs.get("schema_file_path")
        self._read_schema()

    def _read_schema(self) -> None:
        '''
        Responsável por abrir o JSON do schema
        :param self.schema_file_path: Path do schema
        '''
        schema_file = open(self._schema_file_path)
        self._opened_json = json.load(schema_file)

    def get_table_name(self) -> str:
        return self._opened_json["title"]

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
                    columns_properties[column] = value["type"]
                    continue
                v_properties = value["properties"]
                for subcolumn, subvalue in v_properties.items():
                    columns_properties[subcolumn] = subvalue["type"]
            return columns_properties
        except Exception as e:
            raise RuntimeError("Impossible to extract Schema properties",
                               str(e))
