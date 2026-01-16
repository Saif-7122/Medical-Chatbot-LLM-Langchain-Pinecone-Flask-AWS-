from dotenv import load_dotenv
import os
from pinecone import Pinecone
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()

PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
index_name = "medical-chatbot"

print(f"Checking index: {index_name}")

if not PINECONE_API_KEY:
    print("Error: PINECONE_API_KEY not found in env.")
    exit(1)

try:
    pc = Pinecone(api_key=PINECONE_API_KEY)
    
    # List indexes
    indexes = pc.list_indexes()
    print(f"Available indexes: {indexes.names()}")
    
    if index_name not in indexes.names():
        print(f"Index {index_name} does not exist!")
    else:
        index = pc.Index(index_name)
        stats = index.describe_index_stats()
        print(f"Index stats: {stats}")
        
        if stats.total_vector_count == 0:
            print("Index is empty!")
        else:
            print("Index has vectors. Testing retrieval...")
            embeddings = download_hugging_face_embeddings()
            docsearch = PineconeVectorStore.from_existing_index(
                index_name=index_name,
                embedding=embeddings
            )
            # Try a simple similarity search
            docs = docsearch.similarity_search("fever", k=3)
            print(f"Retrieved {len(docs)} documents.")
            for doc in docs:
                print(f"- {doc.page_content[:100]}...")

except Exception as e:
    print(f"An error occurred: {e}")
