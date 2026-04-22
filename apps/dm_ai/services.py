import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import logging

logger = logging.getLogger(__name__)

class DMAIService:
    def __init__(self, user):
        self.user = user
        self.api_key = os.getenv('GOOGLE_API_KEY')
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=self.api_key)

    def generate_dm_reply(self, message_text):
        """
        Generate a reply for a direct message.
        Always polite and helpful.
        """
        prompt = ChatPromptTemplate.from_template(
            "You are a professional social media assistant. Respond to this TikTok DM: '{message}'"
        )
        chain = prompt | self.llm
        response = chain.invoke({"message": message_text})
        return response.content
