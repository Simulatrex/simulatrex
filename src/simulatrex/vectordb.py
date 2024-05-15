"""
Author: Dominik Scherm (dom@simulatrex.ai)

File: vectordb.py
Description: Defines the vectordb class, which is a wrapper around ChromaDB

"""

import os
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

load_dotenv()

from simulatrex.utils.log import SingletonLogger

_logger = SingletonLogger


class VectorDB:
    def __init__(self, collection_name: str):
        api_key = os.getenv("OPENAI_API_KEY")

        if api_key is None:
            raise Exception(
                "No OpenAI API key found. Please set OPENAI_API_KEY as environment variable."
            )

        if collection_name is None:
            raise Exception("No collection name provided.")

        self.collection_name = collection_name
        self.api_key = api_key
        self.init_chroma()

    def init_chroma(self):
        try:
            # Embed using openai, TODO: replace with abstract embedding
            openai_embed_function = embedding_functions.OpenAIEmbeddingFunction(
                api_key=self.api_key,
                # TODO: replace with abstract model name
                model_name="text-embedding-ada-002",
            )

            current_dir = os.path.dirname(os.path.abspath(__file__))
            chroma_db_path = os.path.join(current_dir, "chromadb")

            self.client = chromadb.PersistentClient(path=chroma_db_path)

            self.collection = self.client.create_collection(
                name=self.collection_name,
                embedding_function=openai_embed_function,
                get_or_create=True,
            )

        except Exception as e:
            _logger.error(e)
            raise Exception("Failed to initialize ChromaDB collection.")

    def add_memory(self, content: str, metadatas=None, ids=None):
        """
        Add memory which will be vectorized

        Parameters:
        - content: content string
        - metadatas (list, optional): List of metadata dictionaries for each document. Defaults to None.
        - ids (list, optional): List of unique IDs for each document. Defaults to None.
        """

        self.collection.add(
            documents=[content],
            metadatas=metadatas or [{}],  # Empty metadata if not provided
            ids=ids,
        )

    def query_memory(
        self, query_text, n_results=5, where_metadata=None, where_document=None
    ):
        """
        Query the ChromaDB collection for semantically similar documents.

        Parameters:
        - query_text (str): The text to query against the stored documents.
        - n_results (int, optional): Number of results to return. Defaults to 5.
        - where_metadata (dict, optional): Filters based on metadata fields. Defaults to None.
        - where_document (dict, optional): Filters based on document content. Defaults to None.

        Returns:
        - list: List of query results.
        """
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where=where_metadata,
            where_document=where_document,
        )
        return results

    def delete_memory(self, memory_id: str):
        """
        Delete a memory by id

        Parameters:
        - id (str): The id of the memory to delete
        """
        self.collection.delete([memory_id])

    def get_collection(self, collection_id: str):
        """
        Get a collection by id

        Parameters:
        - id (str): The id of the memory to get
        """
        return self.client.get_collection(collection_id)

    def delete_collection(self, collection_id: str):
        """
        Delete a collection by id

        Parameters:
        - id (str): The id of the memory to delete
        """
        self.client.delete_collection(collection_id)
