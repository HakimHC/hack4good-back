import os
from dotenv import load_dotenv
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.llms import OpenAI

load_dotenv()
embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY"))
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=30, separator="\n")

print(os.getenv('PATH_CARREFOUR'))
print(os.getenv('VEC_CARREFOUR'))
print(os.getenv('PATH_DIA'))
print(os.getenv('VEC_DIA'))
print(os.getenv('PATH_MERCADONA'))
print(os.getenv('VEC_MERCADONA'))

loader = CSVLoader(file_path=os.environ.get("PATH_CARREFOUR"))
documents = loader.load()
docs = text_splitter.split_documents(documents=documents)

vectorstore = FAISS.from_documents(docs, embeddings)
vectorstore.save_local(os.environ.get("VEC_CARREFOUR"))

loader = CSVLoader(file_path=os.environ.get("PATH_DIA"))
documents = loader.load()
docs = text_splitter.split_documents(documents=documents)

vectorstore = FAISS.from_documents(docs, embeddings)
vectorstore.save_local(os.environ.get("VEC_DIA"))

loader = CSVLoader(file_path=os.environ.get("PATH_MERCADONA"))
documents = loader.load()
docs = text_splitter.split_documents(documents=documents)

vectorstore = FAISS.from_documents(docs, embeddings)
vectorstore.save_local(os.environ.get("VEC_MERCADONA"))

# new_vectorstore = FAISS.load_local(
#     "products_database", embeddings, allow_dangerous_deserialization=True
# )
# qa = RetrievalQA.from_chain_type(
#     llm=OpenAI(
#         # engine="gpt-4-1106-preview",
#         temperature=0.0,
#         max_tokens=3100,
#         top_p=1.0,
#         frequency_penalty=0.0,
#         presence_penalty=0.0,
#     ),
#     chain_type="stuff",
#     retriever=new_vectorstore.as_retriever(),
#     verbose=True,
# )
# res = qa.run("cuanto cuesta una baguete en el carrefour")
# print(res)