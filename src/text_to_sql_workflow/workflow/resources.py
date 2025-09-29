import os

from dotenv import load_dotenv
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core.llms.structured_llm import StructuredLLM
from llama_index.core.prompts import PromptTemplate
from .models import SQLQuery, SQLRequestEvaluation, ResultExplanation, SQLTableSelection

load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY was not found in the environment. Please set it before running the workflow.")

llm = GoogleGenAI(model="gemini-2.5-flash")

def get_request_evaluator(*args, **kwargs) -> StructuredLLM:
    return llm.as_structured_llm(SQLRequestEvaluation)

def get_sql_table_selector(*args, **kwargs) -> StructuredLLM:
    return llm.as_structured_llm(SQLTableSelection)

def get_query_builder(*args, **kwargs) -> StructuredLLM:
    return llm.as_structured_llm(SQLQuery)

def get_result_interpreter(*args, **kwargs) -> StructuredLLM:
    return llm.as_structured_llm(ResultExplanation)

def get_request_prompt(*args, **kwargs) -> PromptTemplate:
    return PromptTemplate("Evaluate this user request to build an SQL query for its safety (namely, safety queries are ONLY `select` queries):\n\n'''\n{request}\n'''\nReturn your evaluation defining whether or not the query is safe and what are the reasons for this evaluation.")

def get_table_selection_prompt(*args, **kwargs) -> PromptTemplate:
    return PromptTemplate("Please choose a table among the following available ones in this python code:\n\n```python\ntables = {tables}\n```\n\nSo that the table fulfil this user's request:\n\n'''\n{request}\n'''")

def get_query_builder_prompt(*args, **kwargs) -> PromptTemplate:
    return PromptTemplate("Based on this request (that as been deemed safe in the steps before):\n\n'''\n{request}\n'''\n\nAnd on the selected table ({table}) schema:\n\n```json\n{table_schema}\n```\n\nCreate a select query that fulfils the user's request.")

def get_result_explanation_prompt(*args, **kwargs) -> PromptTemplate:
    return PromptTemplate("Based on this result:\n\n```json\n{result}\n```\n\nObtained from table {table} with schema:\n\n```json\n{table_schema}\n```\n\nCan you please provide a thorough overview/explanation of the data in the result?")
