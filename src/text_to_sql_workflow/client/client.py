import pgsql

from dataclasses import asdict
from .utils import uri_to_connection_details, ConnectionDetails, ColumnSchema

class PostgresClient:
    def __init__(self, uri: str, enable_tls: bool = False):
        self.connection_details: ConnectionDetails = uri_to_connection_details(uri)
        self.tls = enable_tls

    def _get_db_connection(self):
        return pgsql.Connection(address=(self.connection_details.host, self.connection_details.port), user=self.connection_details.user, password=self.connection_details.password, database=self.connection_details.database, tls=self.tls)
    
    def get_tables(self) -> list:
        public_tables = []
        with self._get_db_connection() as db:
            tables = db.prepare("""SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND table_type = 'BASE TABLE'
ORDER BY table_name;""")
            for table in tables(): # type: ignore
                public_tables.append(table.table_name)
            tables.close()  
        return public_tables

    def get_table_schema(self, table_name: str) -> list[dict]:
        column_schemas = []
        with self._get_db_connection() as db:
            columns = db.prepare("""SELECT 
    column_name,
    data_type,
    character_maximum_length,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_schema = 'public' 
  AND table_name = $1
ORDER BY ordinal_position;""")
            for column in columns(table_name): # type: ignore
                column_schemas.append(asdict(ColumnSchema(column.column_name, column.data_type, column.character_maximum_length, column.is_nullable, column.column_default)))
            columns.close()
        return column_schemas

    def select(self, statement: str) -> list[dict]:
        if not statement.lower().startswith("select"):
            raise ValueError("A select statement must start with `select`")
        selected = []
        with self._get_db_connection() as db:
            selected_items = db.prepare(statement=statement)
            for item in selected_items(): # type: ignore
                selected.append(asdict(item))
        return selected
    

        