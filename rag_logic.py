from llama_index.core import SimpleDirectoryReader, Settings, VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.core.vector_stores import SimpleVectorStore
from llama_index.core.storage.index_store import SimpleIndexStore
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.core.memory import ChatMemoryBuffer
import os

Settings.llm = Ollama(
    model='wizardlm2:latest',
    temperature=0,
    context_window=1024,
    request_timeout=960
)

Settings.embed_model = OllamaEmbedding(
    model_name='nomic-embed-text:v1.5',
    embed_batch_size=10,
)


# uri = r"mongodb+srv://blackops:lcQkXpbr7NYpXHix@blackops.buygd3m.mongodb.net/?retryWrites=true&w=majority&appName=blackops"

# mongodb_client = pymongo.MongoClient(uri , server_api = ServerApi('1'))
# db = mongodb_client.get_database('PDFindexing')

# def ReadAndStore():

#     documents = SimpleDirectoryReader('data').load_data()
#     storage = StorageContext.from_defaults( vector_store= MongoDBAtlasVectorSearch(mongodb_client=mongodb_client , collection_name='PDFindex' , db_name='PDFindexing'))
#     index = VectorStoreIndex.from_documents(documents=documents , show_progress=True , storage_context = storage)


# def initializeDB():
#     print(db.list_collection_names())

#     if 'PDFindex' in db.list_collection_names():
#         print('exist')
#         return
#     else :
#         db.create_collection('PDFindex')
#         ReadAndStore()
#         print('Success')


# initializeDB()

# index = VectorStoreIndex.from_vector_store(vector_store= MongoDBAtlasVectorSearch(mongodb_client=mongodb_client , collection_name='PDFindex' , db_name='PDFindexing'))
# query = index.as_query_engine()

# while True:
#     prompt = input('you :')
#     print(query.query(prompt))

class RAG():
    def __init__(self, filename, file_path) -> None:
        super().__init__()

        self.file_path = file_path
        self.filename = filename
        self.embedding_path = f"./storage/{self.filename}_embedding"
        self.chat_store = SimpleChatStore()
        self.chat_memory = ChatMemoryBuffer.from_defaults(
            token_limit=3000,
            chat_store=self.chat_store,
            chat_store_key=filename,
        )
        # self.chat_store.persist(persist_path=f'history/{self.filename}.json')
        self._ReadAndStore()

    def _ReadAndStore(self):

        # Check if path exist
        if os.path.exists(self.embedding_path):
            print('File exist')
            return

        else:
            # Read documents from path
            documents = SimpleDirectoryReader(
                input_files=[self.file_path], errors='ignore').load_data()

            # init storage with one of vector stores
            storage_context = StorageContext.from_defaults(
                vector_store=SimpleVectorStore()
            )

            # Create and build index
            index = VectorStoreIndex.from_documents(
                documents=documents, show_progress=True, storage_context=storage_context)

            # Save index to persist , default (./storage)
            index.storage_context.persist(persist_dir=self.embedding_path)

            print('Embedding success ...')

    def _LoadEmbedding(self):

        # Setup storage to load from it
        storage_context = StorageContext.from_defaults(
            persist_dir=self.embedding_path)

        # Load index from storage
        loaded_index = load_index_from_storage(storage_context=storage_context)

        return loaded_index

    def QueryCreator(self):

        # load the saved embedding
        loaded_index = self._LoadEmbedding()

        # Make loaded index act as query agent with as_query_engine method
        query = loaded_index.as_chat_engine(
            streaming=True ,
            memory= self.chat_memory ,
            chat_mode='context'
            )
        
        
        
        return query

    def Act(self, prompt):

        agent = self.QueryCreator().stream_chat(prompt)
        
        return agent
