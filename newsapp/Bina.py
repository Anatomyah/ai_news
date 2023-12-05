from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents.agent_types import AgentType

# Create an instance of SQLDatabase to interact with the SQLite database.
db = SQLDatabase.from_uri(r"sqlite:///C:\Users\User\PycharmProjects\news\db.sqlite3")

# Initialize the SQLDatabaseToolkit with the database and a configured OpenAI LLM instance.
toolkit = SQLDatabaseToolkit(db=db, llm=OpenAI(temperature=0))

# Create an SQL Agent using the Langchain library.
agent_executor = create_sql_agent(
    llm=OpenAI(temperature=0),
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
)

# Execute the agent to perform a task – in this case, summarizing the latest article in the economics category.
result = agent_executor.run("give me a summary of the body of the latest article in the economics category")

# The result variable holds the output from the agent's execution.
