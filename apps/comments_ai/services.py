import os
from django.conf import settings
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
import logging

logger = logging.getLogger(__name__)

class CommentAIService:
    def __init__(self, user):
        self.user = user
        self.api_key = os.getenv('GOOGLE_API_KEY')
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", google_api_key=self.api_key)
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=self.api_key)
        self.vector_db_path = os.path.join(settings.BASE_DIR, 'vector_stores', f'user_{user.id}_comments')

    def ingest_knowledge(self, texts):
        """
        Ingest user-provided strings into the vector store.
        """
        docs = [Document(page_content=t) for t in texts]
        self._add_to_vector_db(docs)
        return True

    def ingest_file(self, file_path):
        """
        Ingest a text file into the vector store.
        """
        from langchain_community.document_loaders import TextLoader
        from langchain_text_splitters import CharacterTextSplitter
        
        loader = TextLoader(file_path, encoding='utf-8')
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)
        
        self._add_to_vector_db(docs)
        return True

    def _add_to_vector_db(self, docs):
        """
        Common embedding and storage logic.
        """
        if os.path.exists(self.vector_db_path):
            vector_db = FAISS.load_local(self.vector_db_path, self.embeddings, allow_dangerous_deserialization=True)
            vector_db.add_documents(docs)
        else:
            vector_db = FAISS.from_documents(docs, self.embeddings)
        
        os.makedirs(os.path.dirname(self.vector_db_path), exist_ok=True)
        vector_db.save_local(self.vector_db_path)

    def _direct_llm_reply(self, text):
        """
        Backup reply logic if RAG fails or no knowledge base is present.
        """
        prompt = ChatPromptTemplate.from_template("""
        You are a helpful TikTok assistant. Answer in a friendly, engaging, and professional way.
        Keep it short (max 2 sentences).
        Message: {text}
        Reply:""")
        try:
            chain = prompt | self.llm
            response = chain.invoke({"text": text})
            return response.content
        except:
            return "Thanks for the comment! Stay tuned for more! 🚀"

    def generate_reply(self, comment_text):
        """
        Use RAG to generate a reply to a comment.
        """
        # Auto-Sync: If no vector DB exists, try to ingest from local file first
        if not os.path.exists(self.vector_db_path):
            self.ingest_local_kb()
            
        if not os.path.exists(self.vector_db_path):
            return self._direct_llm_reply(comment_text)
            
        try:
            vector_db = FAISS.load_local(self.vector_db_path, self.embeddings, allow_dangerous_deserialization=True)
            docs = vector_db.similarity_search(comment_text, k=3)
            context = "\n".join([doc.page_content for doc in docs])
            
            prompt = ChatPromptTemplate.from_template("""
            You are a helpful TikTok assistant for a creator. Answer friendly.
            Context: {context}
            Comment: {comment}
            Reply:""")
            
            chain = prompt | self.llm
            response = chain.invoke({"context": context, "comment": comment_text})
            return response.content
        except:
            return self._direct_llm_reply(comment_text)

    def generate_dm_reply(self, message_text):
        """
        Generate a RAG-based reply for a Direct Message.
        """
        if not os.path.exists(self.vector_db_path):
            return self._direct_llm_reply(message_text)

        try:
            vector_db = FAISS.load_local(self.vector_db_path, self.embeddings, allow_dangerous_deserialization=True)
            docs = vector_db.similarity_search(message_text, k=3)
            context = "\n".join([doc.page_content for doc in docs])
            
            prompt = ChatPromptTemplate.from_template("""
            You are a professional assistant handling Direct Messages.
            Use the context below to answer the user's question accurately.
            Context: {context}
            Message: {message}
            Assistant Reply:""")
            
            chain = prompt | self.llm
            response = chain.invoke({"context": context, "message": message_text})
            return response.content
        except:
            return self._direct_llm_reply(message_text)

    def ingest_local_kb(self):
        """
        Ingest the bundled knowledgebase.txt into the vector store.
        """
        kb_path = os.path.join(settings.BASE_DIR, 'apps', 'comments_ai', 'knowledgebase.txt')
        if os.path.exists(kb_path):
            return self.ingest_file(kb_path)
        return False
