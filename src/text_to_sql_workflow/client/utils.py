from dataclasses import dataclass
from typing import Any

@dataclass
class ConnectionDetails:
    host: str
    port: int
    user: str
    database: str
    password: str

@dataclass
class ColumnSchema:
    column_name: str
    data_type: str
    character_maximum_length: Any
    is_nullable: bool
    column_default: Any


def uri_to_connection_details(uri: str) -> ConnectionDetails:
    """
    Convert Postgres connection URI to connection details (host, port, user, database, password)

    Args:
        uri (str): Postgres connection URI
    
    Returns:
        ConnectionDetails
    """
    try:
        base_uri = uri.split("://")[1]
        database = base_uri.split("/")[1]
        user_psw, host_port = base_uri.split("@")[0], base_uri.split("@")[1]
        user, psw = user_psw.split(":")[0], user_psw.split(":")[1]
        host, port = host_port.split(":")[0], int(host_port.split(":")[1].split("/")[0])
    except Exception as e:
        raise ValueError(f"It was not possible to parse the provided URI due to the following error: {e}")
    else:
        return ConnectionDetails(database=database, port=port, user=user, host=host, password=psw)