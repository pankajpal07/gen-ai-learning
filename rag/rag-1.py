from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
import os
from dotenv import load_dotenv

load_dotenv()
pdf_path = Path(__file__).parent / "Hands-On-Machine-Learning-with-Scikit-Learn-Keras-and-TensorFlow.pdf"
loader = PyPDFLoader(pdf_path)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
)

split_docs = text_splitter.split_documents(docs)

embeddings_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-exp-03-07", google_api_key=os.getenv("GEMINI_API_KEY"))

print("Injection Done")

retriever = QdrantVectorStore.from_documents(
    docs,
    embeddings_model,
    url=os.getenv("QDRANT_URL"),
    prefer_grpc=True,
    api_key=os.getenv("QDRANT_API_KEY"),
    collection_name="my_documents",
)

search_result = retriever.similarity_search(
    query="What is Learning to Optimize Rewards?"
)

print("Rerieval chunks", search_result)