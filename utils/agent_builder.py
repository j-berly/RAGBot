from pydantic import BaseModel, Field
from typing import Optional
from llama_index.chat_engine import CondensePlusContextChatEngine
from llama_index import ServiceContext, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from utils.doc_parser import load_data
from prompts import GEN_SYS_PROMPT_STR


class RAGParams(BaseModel):
    top_k: int = Field(
        default=2, description="Number of documents to retrieve from vector store."
    )
    chunk_size: int = Field(default=1024, description="Chunk size for vector store.")
    embed_model: str = Field(default="BAAI/bge-small-zh", description="Embedding model to use (default is OpenAI)")


class RAGAgent:
    """
    RAG Agent: load data, create agent,  (add web tool later)
    """

    def __init__(self, llm, params: Optional[RAGParams] = None):
        self.docs = None
        self.rag = None
        self.system_prompt = GEN_SYS_PROMPT_STR
        self._params = params
        self._llm = llm

    def load_data(self, filename):
        """Load data for a given task.

        Only filename should be specified, and must be existed.

        Args:
            filename (str): a filename or a set of filenames concatenated with ";"

        """
        self.docs = load_data(filename)

    def add_web_tool(self):
        """ TODO """

    def create_agent(self):
        """Create retrieval augmented generation agent for a given task.

        There are no parameters for this function because all the
        functions should have already been called to set up the agent.

        """

        embed_model = HuggingFaceEmbedding(model_name=self._params.model_name, tokenizer_name=self._params.model_name)

        # index data
        service_context = ServiceContext.from_defaults(
            llm=self._llm,
            chunk_size=self._params.chunk_size,
            embed_model=embed_model,
            system_prompt=self.system_prompt
        )
        vector_index = VectorStoreIndex.from_documents(documents=self.docs, service_context=service_context)

        self.rag = CondensePlusContextChatEngine.from_defaults(
            vector_index.as_retriever(similarity_top_k=self._params.top_k),
            service_context=service_context, system_prompt=self.system_prompt)
