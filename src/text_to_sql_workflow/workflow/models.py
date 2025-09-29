from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

from text_to_sql_workflow.client import PostgresClient

class SQLRequestEvaluation(BaseModel):
    is_safe: bool = Field(description="Is the SQL query safe? An SQL query is deemed safe if it is composed by only one SELECT statement")
    reasons: str = Field(description="Brief reasons why the query is or is not safe")

class SQLTableSelection(BaseModel):
    table_name: str = Field(description="Selected table among the available ones to fulfil the user's request.")

class SQLQuery(BaseModel):
    statement: str = Field(description="SQL select statement that fulfils the user's request")
    explanation: str = Field(description="Explanation of the statement")

class ResultExplanation(BaseModel):
    explanation: str = Field(description="Explanation of the result from an SQL select query")

class WorkflowState(BaseModel):
    input_request: str = Field(default_factory=str)
    pg_client: Optional[PostgresClient] = Field(default=None)
    table_name: str = Field(default_factory=str)
    table_schema: str = Field(default_factory=str)
    statement: str = Field(default_factory=str)
    result: str = Field(default_factory=str)
    model_config = ConfigDict(arbitrary_types_allowed=True)