import json
from workflows import Workflow, Context, step
from workflows.resource import Resource
from llama_index.core.llms.structured_llm import StructuredLLM
from llama_index.core.prompts import PromptTemplate
from typing import Annotated, Union

from text_to_sql_workflow.client import PostgresClient
from .models import WorkflowState, SQLRequestEvaluation, SQLTableSelection, SQLQuery, ResultExplanation
from .events import InputEvent, TableSelection, BuildQuery, HandleQuery, OutputEvent, SelectTable
from .resources import get_query_builder, get_query_builder_prompt, get_request_evaluator, get_request_prompt, get_result_interpreter, get_result_explanation_prompt, get_sql_table_selector, get_table_selection_prompt

class TextToSQLWorkflow(Workflow):
    @step
    async def evaluate_user_request(self, ev: InputEvent, ctx: Context[WorkflowState], request_evaluator: Annotated[StructuredLLM, Resource(get_request_evaluator)], request_prompt: Annotated[PromptTemplate, Resource(get_request_prompt)]) -> Union[SelectTable, OutputEvent]:
        ctx.write_event_to_stream(ev)
        async with ctx.store.edit_state() as state:
            state.pg_client = PostgresClient(ev.db_uri, ev.enable_tls)
            state.input_request = ev.message
        res = await request_evaluator.achat(messages=request_prompt.format_messages(request=ev.message))
        if res.message.content:
            evaluation = SQLRequestEvaluation.model_validate_json(res.message.content)
        else:
            evaluation = SQLRequestEvaluation(is_safe=False, reasons="It was not possible to evaluate the query for safety at this time")
        if not evaluation.is_safe:
            return OutputEvent(explained_result=evaluation.reasons)
        else:
            return SelectTable()
    @step
    async def select_postgres_table(self, ev: SelectTable, ctx: Context[WorkflowState], table_selector: Annotated[StructuredLLM, Resource(get_sql_table_selector)], table_selection_prompt: Annotated[PromptTemplate, Resource(get_table_selection_prompt)]) -> Union[OutputEvent, TableSelection]:
        ctx.write_event_to_stream(ev)
        state = await ctx.store.get_state()
        if state.pg_client is not None:
            tables = state.pg_client.get_tables()
            res = await table_selector.achat(table_selection_prompt.format_messages(tables=tables, request=state.input_request))
            if res.message.content:
                selection = SQLTableSelection.model_validate_json(res.message.content)
            else:
                selection = SQLTableSelection(table_name="")
            if selection.table_name != "":
                async with ctx.store.edit_state() as state:
                    state.table_name = selection.table_name
                return TableSelection()
            else:
                return OutputEvent(explained_result="It was not possible to select a table to fulfil your query at this time")
        else:
            return OutputEvent(explained_result="It was not possible to select a table to fulfil your query at this time")
    
    @step
    async def build_query(self, ev: TableSelection, ctx: Context[WorkflowState], query_builder: Annotated[StructuredLLM, Resource(get_query_builder)], query_builder_prompt: Annotated[PromptTemplate, Resource(get_query_builder_prompt)]) -> Union[OutputEvent, BuildQuery]:
        ctx.write_event_to_stream(ev)
        state = await ctx.store.get_state()
        if state.pg_client is not None:
            table_schema = state.pg_client.get_table_schema(state.table_name)
            async with ctx.store.edit_state() as edit_state:
                edit_state.table_schema = json.dumps(table_schema, indent=4)
            res = await query_builder.achat(query_builder_prompt.format_messages(table=state.table_name, table_schema=json.dumps(table_schema, indent=4), request=state.input_request))
            if res.message.content:
                query = SQLQuery.model_validate_json(res.message.content)
            else:
                query = SQLQuery(statement="", explanation="It was not possible to generate an SQL query at this time")
            if query.statement != "":
                return BuildQuery(statement=query.statement)
            else:
                return OutputEvent(explained_result=query.explanation)
        else:
            return OutputEvent(explained_result="It was not possible to generate an SQL query at this time")
    
    @step
    async def handle_query(self, ev: BuildQuery, ctx: Context[WorkflowState]) -> Union[HandleQuery, OutputEvent]:
        ctx.write_event_to_stream(ev)
        state = await ctx.store.get_state()
        if state.pg_client is not None:
            result = state.pg_client.select(ev.statement)
            if len(result) > 0:
                async with ctx.store.edit_state() as edit_state:
                    edit_state.result = json.dumps(result, indent=4)
                return HandleQuery()
            else:
                return OutputEvent(explained_result="It was not possible to retrieve results for your query at this time")
        else:
            return OutputEvent(explained_result="It was not possible to retrieve results for your query at this time")

    @step
    async def explain_result(self, ev: HandleQuery, ctx: Context[WorkflowState], result_interpreter: Annotated[StructuredLLM, Resource(get_result_interpreter)], result_explanation_promt: Annotated[PromptTemplate, Resource(get_result_explanation_prompt)]) -> OutputEvent:
        ctx.write_event_to_stream(ev)
        state = await ctx.store.get_state()
        res = await result_interpreter.achat(result_explanation_promt.format_messages(result=state.result, table_schema=state.table_schema, table=state.table_name))
        if res.message.content:
            explanation = ResultExplanation.model_validate_json(res.message.content)
        else:
            explanation = ResultExplanation(explanation=f"It was not possible to explain the result at the moment.\n\nThe final result was:\n\n```json\n{state.result}\n```\n\n")
        return OutputEvent(explained_result=explanation.explanation)

            



