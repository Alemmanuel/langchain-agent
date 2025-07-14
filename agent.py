import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.chains import RetrievalQA, create_sql_query_chain
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.utilities import SQLDatabase

from tools import rick_and_morty_tool, saludar

# 1. Cargar credenciales
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# 2. LLM
llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-flash",
    temperature=0.3,
    google_api_key=GOOGLE_API_KEY,
)

# 3. Embeddings y Vectorstore
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.load_local("vectorstore_index", embedding_model, allow_dangerous_deserialization=True)
retriever = vectorstore.as_retriever()
vector_qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# 4. SQL
db = SQLDatabase.from_uri("sqlite:///demo.db")
sql_chain = create_sql_query_chain(llm, db)

# 5. Herramientas
tools = [
    Tool(
        name="vector_qa",
        description="Busca información en la base vectorial.",
        func=lambda q: vector_qa.invoke({"query": q})
    ),
    Tool(
        name="sql_chain",
        description="Realiza consultas SQL sobre empleados.",
        func=lambda q: sql_chain.invoke({"question": q})
    ),
    Tool(
        name="rick_and_morty_tool",
        description="Devuelve los datos de un personaje de Rick and Morty por ID.",
        func=rick_and_morty_tool
    ),
    Tool(
        name="saludar",
        description="Saluda a una persona por su nombre.",
        func=saludar
    )
]

# 6. Agente
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

agent.llm = llm  # Aseguramos que el agente use el LLM configurado
agent.vectorstore = vectorstore  # Añadimos el vectorstore al agente
agent.sql_chain = sql_chain  # Añadimos la cadena SQL al agente