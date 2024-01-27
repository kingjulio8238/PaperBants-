#Langchain integrations
from langchain.embeddings.huggingface import HuggingFaceBgeEmbeddings
from llama_index import ServiceContext

embed_model = HuggingFaceBgeEmbeddings(model_name="BAAI/bge-base-en")

service_context = ServiceContext.from_defaults(embed_model=embed_model)

