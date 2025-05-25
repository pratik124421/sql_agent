


import os
from langchain.chat_models import AzureChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from operator import itemgetter
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# ----------------------------
# Azure OpenAI Configuration
# ----------------------------
os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("api_key")
os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("api_url")
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_VERSION"] = "2025-01-01-preview"

deployment_name = "gpt-4o"

# ----------------------------
# Set up Azure OpenAI LLM
# ----------------------------
llm = AzureChatOpenAI(
    deployment_name=deployment_name,
    temperature=0,
    model_name="gpt-4o"
)

# ----------------------------
# Connect to SQLite DB
# ----------------------------
db = SQLDatabase.from_uri("sqlite:///restaurant.db")
print("::::> Available tables:", db.get_usable_table_names())

# Get schema for prompt context
schema = db.get_table_info()

# ----------------------------
# SQL Cleanup Utility
# ----------------------------
def clean_sql(query: str) -> str:
    return query.strip().replace("```sql", "").replace("```", "").strip()

clean_query = RunnableLambda(lambda x: {"query": clean_sql(x)})
execute_query = clean_query | QuerySQLDataBaseTool(db=db)

# ----------------------------
# SQL Generation Prompt with Schema
# ----------------------------
sql_generation_prompt = PromptTemplate.from_template(f"""
You are an expert SQL developer.

Given the database schema:
{schema}

Only write a valid SQL query that answers the user's question.
Do not include explanations or markdown.

Question: {{question}}
SQL Query:
""")

write_query = sql_generation_prompt | llm | StrOutputParser()

# ----------------------------
# Answer Generation Prompt
# ----------------------------
answer_prompt = PromptTemplate.from_template("""
Given the following user question, SQL query, and SQL result, answer the user question.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer:
""")

answer = answer_prompt | llm | StrOutputParser()

# ----------------------------
# Final Chain
# ----------------------------
chain = (
    RunnablePassthrough.assign(query=write_query)
    .assign(result=itemgetter("query") | execute_query)
    | answer
)


def run_chain(q: str):
    response = chain.invoke({"question": q})
    # sql = write_query.invoke({"question": user_question})
    # return sql.strip(), db.run(sql.strip()), result.strip()
    return response