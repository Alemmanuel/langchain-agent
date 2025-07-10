import os
from dotenv import load_dotenv

from langchain.agents import initialize_agent, AgentType
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

from tools import tools

# ---------------------- Cargar variables de entorno ----------------------
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise ValueError("❌ Falta GOOGLE_API_KEY en el archivo .env")

# ---------------------- Configurar paths absolutos ----------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VECTORSTORE_PATH = os.path.join(BASE_DIR, "vectorstore_index")
SQLITE_PATH = f"sqlite:///{os.path.join(BASE_DIR, 'demo.db')}"

# ---------------------- Modelo Gemini ----------------------
llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-flash",
    google_api_key=google_api_key,
    temperature=0.3
)

# ---------------------- Vectorstore: FAISS ----------------------
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.load_local(
    VECTORSTORE_PATH,
    embedding_model,
    allow_dangerous_deserialization=True
)
retriever = vectorstore.as_retriever()
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

@tool
def ask_vectorstore(query: str) -> str:
    """Consulta información semántica en la base vectorial."""
    return qa_chain.invoke(query)

# ---------------------- Base de datos SQL ----------------------
db = SQLDatabase.from_uri(SQLITE_PATH)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# ---------------------- Inicializar agente multifuente ----------------------
agent = initialize_agent(
    tools=tools + [ask_vectorstore] + toolkit.get_tools(),
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)

# ---------------------- Interfaz CLI ----------------------
if __name__ == "__main__":
    print("🤖 Agente con Gemini listo. Escribe tu pregunta. Escribe 'salir' para terminar.")
    while True:
        user_input = input("👉 Tú: ")
        if user_input.lower() in ["salir", "exit", "quit"]:
            print("👋 Hasta luego, The Special One.")
            break
        try:
            response = agent.invoke({"input": user_input})
            print("🤖 Agente:", response["output"])
        except Exception as e:
            print("❌ Error:", str(e))
