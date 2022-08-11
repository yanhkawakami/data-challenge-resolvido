from reader import SchemaRead


class Query:
    def __init__(self, ) -> None:
        self._path_hql = "hql/create_table_template.hql"
        schema_read = SchemaRead(schema_file_path="schema.json")
        self._table_name = schema_read.get_table_name()
        self._columns = schema_read.get_columns_properties()
        self._template_hql = self.__load_template()
        self._formatted_columns = self.__format_columns()

    def __load_template(self) -> str:
        with open(self._path_hql, "r") as template:
            template_hql = template.read()
        return template_hql

    def __format_columns(self) -> str:
        joined_columns = [k + " " + v for k, v in self._columns.items()]
        formatted_columns = ", ".join(joined_columns)
        return formatted_columns

    def build_query(self) -> str:
        built_query = self._template_hql.format(
            table_name=self._table_name,
            columns_names_type=self._formatted_columns
        )
        return built_query
