from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
import os

# Cargar documentos de ejemplo
loader = TextLoader("documento.txt", encoding="utf-8")  # Asegúrate de tener este archivo
documents = loader.load()

# Dividir texto
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

# Embeddings
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Crear y guardar el índice
vectorstore = FAISS.from_documents(docs, embedding_model)
vectorstore.save_local("vectorstore_index")
print("✅ Vectorstore generada y guardada en vectorstore_index/")
