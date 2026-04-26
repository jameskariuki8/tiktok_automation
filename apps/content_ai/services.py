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
        Deep-dive analysis by a professional-tier AI Social Media Manager.
        """
        from analytics.models import VideoAnalytics
        from django.db.models import Avg, Sum
        
        # 1. Fetch deep metrics
        all_stats = VideoAnalytics.objects.filter(account__user=self.user).order_by('-date')
        if not all_stats.exists():
            return "### DATA COLLECTION PHASE\nWe need at least 3-5 synced posts to generate a professional roadmap. \n\n**Action Required:** \n* Go to the Dashboard \n* Click 'Sync Engine' \n* Ensure your TikTok videos are visible in the grid."

        # 2. Pattern Recognition
        total_engagement = all_stats.aggregate(Sum('like_count'), Sum('comment_count'), Sum('share_count'))
        avg_views = all_stats.aggregate(Avg('view_count'))['view_count__avg']
        
        # 3. Create High-Context Prompt
        history = []
        for p in all_stats[:10]:
            history.append(f"Post: {p.tiktok_video_id} | Views: {p.view_count} | Likes: {p.like_count} | Comments: {p.comment_count}")
        
        context = "\n".join(history)
        
        prompt = ChatPromptTemplate.from_template("""
        You are a Senior Social Media Growth Director at a top-tier digital agency. 
        Your mission is to provide a "Virality Roadmap" for this client.
        
        DATA FEED:
        {history}
        
        Provide your analysis in THREE DISTINCT SECTIONS:
        1. THE WINNING FORMULA: Identify which specific post structure or topic is working and why (be specific about engagement patterns).
        2. GROWTH FRICTION: Identify what is holding the account back (e.g. low comment-to-view ratio, missing hooks).
        3. THE ROADMAP: Provide 3 concrete, high-impact video ideas for the next 7 days based on this data.
        
        Tone: Professional, authoritative, data-driven, and encouraging.
        """)
        
        try:
            chain = prompt | self.llm
            response = chain.invoke({"history": context})
            return response.content
        except Exception as e:
            logger.error(f"AI Analysis Failed: {e}")
            return "The AI consultant is currently in a strategy meeting. Try again in 5 minutes."

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
