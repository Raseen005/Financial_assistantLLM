import chromadb
from sentence_transformers import SentenceTransformer  
from typing import List, Dict
import os

class Vectorstore:
    
    def __init__(self, persist_directory: str = './chroma_db'):
        
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(
            name='financial_documents',  
            metadata={'description': "Documents for financial information"}
        )
        
        if not os.path.exists('./models/all-MiniLM-L6-v2'):
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            self.embedding_model.save('./models/all-MiniLM-L6-v2')
        else:
            self.embedding_model = SentenceTransformer('./models/all-MiniLM-L6-v2')

        
        print("Initialization Successful")
        
    def chunk_text(self, text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
        chunks = []  
        start = 0
        while start < len(text):
            end = start + chunk_size 
            temp = text[start:end]
            chunks.append(temp)  
            start += chunk_size - chunk_overlap
            
        return chunks
    
    def process_tables(self, tables: List) -> str:
        
        table_content = []
        
        for table in tables:
            if table['is_financial']:
                table_str = f"\n--Financial information (page number {table['page_num']})--\n"
                table_str += table['data'].to_string(index=False)  
                table_content.append(table_str)
                
        return '\n'.join(table_content)
    
    def add_documents(self, documents_data: Dict, document_name: str):
        
        text_content = documents_data['text']
        table_content = self.process_tables(documents_data['tables'])
        
        full_content = text_content + '\n\n' + table_content
        
        chunks = self.chunk_text(full_content)
        embeddings = self.embedding_model.encode(chunks).tolist()  
        
        chunk_ids = [f"{document_name}_chunk_{i}" for i in range(len(chunks))]
        
        metadatas = [{'document_name': document_name, 'chunk_id': i} for i in range(len(chunks))]
        
        self.collection.add(
            embeddings=embeddings,
            documents=chunks,
            metadatas=metadatas,
            ids=chunk_ids
        )
        
        
    def search_query(self, query: str, n_inputs: int = 5):
        query_embedding = self.embedding_model.encode([query]).tolist() 
        
        results = self.collection.query(
            query_embeddings=query_embedding,  
            n_results=n_inputs,
            include=['documents', 'metadatas', 'distances']
        )
        
        return results
    
    def get_information(self):
        return self.collection.count()
    
    def delete_information(self):
        """Delete all documents from the collection"""
        try:
            # Try multiple approaches to clear the database
            count_before = self.collection.count()
            
            # Approach 1: Modern ChromaDB
            self.collection.delete(where={})
            
            # Approach 2: If that fails, try alternative
        except ValueError:
            try:
                self.collection.delete(where={"document_name": {"$ne": ""}})
            except:
                # Approach 3: Get all IDs and delete them individually
                results = self.collection.get()
                if results['ids']:
                    self.collection.delete(ids=results['ids'])
        
            
