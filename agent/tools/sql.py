import sqlite3
from langchain.tools import Tool

conn=sqlite3.connect("db.sqlite")

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

run_query_tool=Tool.from_function(
    name="run_sqlite_query",
    description="Run a sqlite query",
    func=run_sqlite_query
)