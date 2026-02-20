"""
Vector store implementation using ChromaDB for semantic search

Provides semantic memory capabilities for B.A.D.I.
"""

import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional, Any
from datetime import datetime
import hashlib

from badi.config import get_config


class VectorStore:
    """
    Vector store for semantic search using ChromaDB
    
    Manages collections for conversations and documents with
    automatic embedding generation.
    """
    
    def __init__(self, persist_directory: Optional[str] = None):
        """
        Initialize ChromaDB client
        
        Args:
            persist_directory: Directory to persist the vector database
        """
        config = get_config()
        
        if persist_directory is None:
            persist_directory = str(config.vector_dir)
        
        # Initialize ChromaDB client with persistence
        self.client = chromadb.Client(Settings(
            persist_directory=persist_directory,
            anonymized_telemetry=False
        ))
        
        # Initialize collections
        self.conversations = self._get_or_create_collection("conversations")
        self.documents = self._get_or_create_collection("documents")
        self.memories = self._get_or_create_collection("memories")
    
    def _get_or_create_collection(self, name: str):
        """Get or create a ChromaDB collection"""
        try:
            return self.client.get_collection(name=name)
        except ValueError:
            return self.client.create_collection(
                name=name,
                metadata={"hnsw:space": "cosine"}
            )
    
    def _generate_id(self, text: str, metadata: dict) -> str:
        """Generate a unique ID for a document"""
        # Combine text and key metadata to create unique hash
        data = f"{text}_{metadata.get('user_id', '')}_{metadata.get('timestamp', '')}"
        return hashlib.md5(data.encode()).hexdigest()
    
    def add_memory(
        self,
        text: str,
        metadata: Optional[Dict[str, Any]] = None,
        collection: str = "conversations"
    ) -> str:
        """
        Add a text entry to the vector store
        
        Args:
            text: The text content to store
            metadata: Additional metadata (user_id, timestamp, task_id, etc.)
            collection: Which collection to add to
            
        Returns:
            Document ID
        """
        if metadata is None:
            metadata = {}
        
        # Add timestamp if not present
        if "timestamp" not in metadata:
            metadata["timestamp"] = datetime.utcnow().isoformat()
        
        # Generate unique ID
        doc_id = self._generate_id(text, metadata)
        
        # Select collection
        coll = self._get_collection(collection)
        
        # Add to vector store (ChromaDB handles embedding automatically)
        coll.add(
            documents=[text],
            metadatas=[metadata],
            ids=[doc_id]
        )
        
        return doc_id
    
    def search(
        self,
        query: str,
        collection: str = "conversations",
        top_k: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Semantic search in the vector store
        
        Args:
            query: Search query text
            collection: Which collection to search
            top_k: Number of results to return
            filter_metadata: Metadata filters (e.g., {"user_id": 1})
            
        Returns:
            List of results with documents, metadata, and distances
        """
        config = get_config()
        top_k = min(top_k, config.vector_search_top_k * 2)  # Safety limit
        
        coll = self._get_collection(collection)
        
        # Perform query
        results = coll.query(
            query_texts=[query],
            n_results=top_k,
            where=filter_metadata
        )
        
        # Format results
        formatted_results = []
        if results and results["documents"] and results["documents"][0]:
            for i in range(len(results["documents"][0])):
                formatted_results.append({
                    "document": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "distance": results["distances"][0][i] if results["distances"] else None,
                    "id": results["ids"][0][i] if results["ids"] else None
                })
        
        return formatted_results
    
    def delete_by_id(self, doc_id: str, collection: str = "conversations"):
        """Delete a document by ID"""
        coll = self._get_collection(collection)
        coll.delete(ids=[doc_id])
    
    def delete_by_metadata(
        self,
        filter_metadata: Dict[str, Any],
        collection: str = "conversations"
    ):
        """Delete documents matching metadata filter"""
        coll = self._get_collection(collection)
        coll.delete(where=filter_metadata)
    
    def update_metadata(
        self,
        doc_id: str,
        metadata: Dict[str, Any],
        collection: str = "conversations"
    ):
        """Update metadata for a document"""
        coll = self._get_collection(collection)
        coll.update(
            ids=[doc_id],
            metadatas=[metadata]
        )
    
    def get_by_id(self, doc_id: str, collection: str = "conversations") -> Optional[Dict[str, Any]]:
        """Get a document by ID"""
        coll = self._get_collection(collection)
        result = coll.get(ids=[doc_id])
        
        if result and result["documents"]:
            return {
                "document": result["documents"][0],
                "metadata": result["metadatas"][0] if result["metadatas"] else {},
                "id": result["ids"][0] if result["ids"] else None
            }
        return None
    
    def count(self, collection: str = "conversations") -> int:
        """Get count of documents in collection"""
        coll = self._get_collection(collection)
        return coll.count()
    
    def _get_collection(self, name: str):
        """Get collection by name"""
        if name == "conversations":
            return self.conversations
        elif name == "documents":
            return self.documents
        elif name == "memories":
            return self.memories
        else:
            raise ValueError(f"Unknown collection: {name}")
    
    def clear_collection(self, collection: str):
        """Clear all entries from a collection"""
        # Delete and recreate collection
        self.client.delete_collection(name=collection)
        
        if collection == "conversations":
            self.conversations = self._get_or_create_collection("conversations")
        elif collection == "documents":
            self.documents = self._get_or_create_collection("documents")
        elif collection == "memories":
            self.memories = self._get_or_create_collection("memories")


# Global vector store instance
_vector_store: Optional[VectorStore] = None


def get_vector_store() -> VectorStore:
    """Get or create the global vector store instance"""
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore()
    return _vector_store


def reload_vector_store() -> VectorStore:
    """Reload vector store (useful after config changes)"""
    global _vector_store
    _vector_store = VectorStore()
    return _vector_store
