from workflows.events import Event, StartEvent, StopEvent
from pydantic import Field

class InputEvent(StartEvent):
    message: str
    db_uri: str
    enable_tls: bool

class SelectTable(Event):
    pass

class TableSelection(Event):
    pass

class BuildQuery(Event):
    statement: str

class HandleQuery(Event):
    pass

class OutputEvent(StopEvent):
    explained_result: str