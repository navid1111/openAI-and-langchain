import sqlite3
from langchain.tools import Tool
from pydantic.v1 import BaseModel
from typing import List

conn=sqlite3.connect("db.sqlite")

def list_tables():
    c=conn.cursor()
    c.execute("SELECT name from sqlite_master WHERE type='table';")
    rows = c.fetchall()
    return rows  # Just return the rows, formatting will be done where it's used

def run_sqlite_query(query):
    try:
        c = conn.cursor()
        c.execute(query)
        results = c.fetchall()
        c.close()
        return results
    except sqlite3.Error as e:
        return f"Database error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"
class RunQueryArgsSchema(BaseModel):
    query:str

run_query_tool=Tool.from_function(
    name="run_sqlite_query",
    description="Run a sqlite query",
    func=run_sqlite_query,
    args_schema=RunQueryArgsSchema
)
def describe_table(table_name):
    c=conn.cursor()
    tables=', '.join("'" +table+"'" for table in table_name)
    rows = c.execute(f"SELECT sql from sqlite_master WHERE type='table' and name IN ({tables});")
    return '\n'.join(row[0] for row in rows if row[0] is not None)
class DescribeTableArgsSchema(BaseModel):
    table_names:List[str]

describe_table_tool=Tool.from_function(
    name="describe_table",
    description="Given a list of table names ,return the schema of the table",
    func=describe_table,
    args_schema=DescribeTableArgsSchema
)