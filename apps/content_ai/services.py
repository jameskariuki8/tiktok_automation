import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from .models import ContentIdea
import logging

logger = logging.getLogger(__name__)

class ContentAIService:
    def __init__(self, user):
        self.user = user
        self.api_key = os.getenv('GOOGLE_API_KEY')
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=self.api_key)

    def generate_content_strategy(self, niche_input):
        """
        Gemini-powered strategy generation.
        """
        prompt = ChatPromptTemplate.from_template("""
        You are a TikTok Content Strategist. Based on the niche: '{niche}', 
        generate a high-performing video idea.
        
        Provide the response in the following format:
        Topic: [Idea title]
        Hook: [First 3 seconds script]
        Script: [Rest of the video script]
        Audience: [Who is this for]
        Hashtags: [#tag1, #tag2...]
        """)
        
        chain = prompt | self.llm
        response = chain.invoke({"niche": niche_input})
        
        # In a production app, we'd parse the structured response (e.g. using Pydantic)
        # For now, we store the raw output or simplified parsing
        lines = response.content.split('\n')
        topic = str(lines[0]) if len(lines) > 0 else niche_input
        
        idea = ContentIdea.objects.create(
            user=self.user,
            topic=topic,
            hook=response.content[:200], # Simplified
            suggested_script=response.content,
            target_audience="General " + niche_input
        )
        return idea

    def analyze_performance_and_advise(self):
        """
        Compare top-performing vs low-performing posts and provide growth advice.
        """
        from analytics.models import VideoAnalytics
        from django.db.models import Avg
        
        # 1. Fetch metrics
        all_stats = VideoAnalytics.objects.filter(account__user=self.user)
        if not all_stats.exists():
            return "No data yet. Post more videos to get AI advice!"

        # 2. Identify patterns (simplified logic)
        avg_likes = all_stats.aggregate(Avg('like_count'))['like_count__avg']
        top_posts = all_stats.filter(like_count__gt=avg_likes).order_by('-like_count')[:3]
        
        # 3. Generate Advice via Gemini
        context = "\n".join([f"Post Caption: {p.caption}, Likes: {p.like_count}, Views: {p.view_count}" for p in all_stats[:5]])
        
        prompt = ChatPromptTemplate.from_template("""
        You are a TikTok Growth Analyst. Here is the performance data for the last few posts:
        {history}
        
        Analyze which type of content is working best and provide 3 actionable tips for improvement.
        Focus on: Hook quality, Topic engagement, and Call to action.
        """)
        
        chain = prompt | self.llm
        response = chain.invoke({"history": context})
        return response.content

    def generate_caption_for_video(self, video_topic):
        """
        Generate a viral TikTok caption and 5 hashtags for a given topic.
        """
        prompt = ChatPromptTemplate.from_template("""
        You are a TikTok Viral Content Creator. 
        Topic: {topic}
        
        Write a short, punchy TikTok caption (under 150 characters) and include 5 trending hashtags.
        Use emojis and make it engaging.
        """)
        
        chain = prompt | self.llm
        response = chain.invoke({"topic": video_topic})
        return response.content
