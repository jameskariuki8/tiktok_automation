import os
import django
import sys
import asyncio
import random
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Setup Django Environment
# Assuming base dir is current working directory or 2 levels up
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path: sys.path.append(BASE_DIR)

# Crucial: Add 'apps' folder to path so we can import 'accounts', 'tiktok', etc.
APPS_DIR = os.path.join(BASE_DIR, 'apps')
if APPS_DIR not in sys.path: sys.path.append(APPS_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User
from tiktok.models import TikTokAccount
from tiktok.services import TikTokApiService
from comments_ai.services import CommentAIService

# Global session storage (Simple memory-based for now)
active_sessions = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to SmartTikTok Orchestrator (Powered by OpenClaw)\n\n"
        "To pair your account, use: /pair [your_username]"
    )

async def pair(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage: /pair [username]")
        return
    
    username = context.args[0]
    try:
        user = User.objects.get(username=username)
        # Store pairing in context
        context.user_data['user_id'] = user.id
        await update.message.reply_text(f"✅ Success! Paired with account: {username}\nUse /engage 20 to start a session.")
    except User.DoesNotExist:
        await update.message.reply_text("❌ User not found.")

async def engage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = context.user_data.get('user_id')
    if not user_id:
        await update.message.reply_text("❌ Please /pair your account first.")
        return

    duration = 20 # default
    if context.args:
        try: duration = int(context.args[0])
        except: pass

    if user_id in active_sessions:
        await update.message.reply_text("⚠️ A session is already running.")
        return

    active_sessions[user_id] = True
    await update.message.reply_text(f"🚀 Starting {duration} minute Engagement Session...\nSimulating human behavior (randomized delays).")
    
    # Run the engagement loop (Async)
    asyncio.create_task(run_engagement_loop(update, user_id, duration))

async def run_engagement_loop(update, user_id, duration_mins):
    user = User.objects.get(id=user_id)
    account = TikTokAccount.objects.filter(user=user).first()
    
    if not account:
        await update.message.reply_text("❌ No TikTok account found in dashboard.")
        active_sessions.pop(user_id, None)
        return

    end_time = time.time() + (duration_mins * 60)
    count = 0
    
    while time.time() < end_time and user_id in active_sessions:
        try:
            # OpenClaw Strategy: Poll -> Analyze -> Logic -> Post
            # For brevity, we poll comments and reply to 1-2 per loop
            service = TikTokApiService(account)
            ai_service = CommentAIService(user)
            
            # 1. Fetch Comments
            # (Using first video as proxy just for demo)
            videos = service.get_video_list()
            if videos:
                vid = videos[0].get('id')
                comments = service.get_video_comments(vid)
                
                for c in comments[:2]: # Reply to max 2 per "beat"
                    if not active_sessions.get(user_id): break
                    
                    # RAG Reply
                    reply_text = ai_service.generate_reply(c.get('text'))
                    
                    # POST
                    service.post_comment_reply(vid, c.get('id'), reply_text)
                    count += 1
                    
                    # 🛡️ HUMAN SIMULATION: Randomized Delay
                    wait = random.randint(30, 90)
                    await update.message.reply_text(f"💬 Replied to @{c.get('user',{}).get('display_name')}\nNext action in {wait}s...")
                    await asyncio.sleep(wait)

            # Wait between cycles
            await asyncio.sleep(random.randint(60, 180))
            
        except Exception as e:
            print(f"Loop Error: {e}")
            await asyncio.sleep(60)

    # FINAL REPORT
    active_sessions.pop(user_id, None)
    await update.message.reply_text(
        f"🏁 Session Complete!\n"
        f"📊 Actions Taken: {count}\n"
        f"Sentiment: Positive (Simulated)\n"
        f"Recommendations: Maintain response velocity."
    )

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = context.user_data.get('user_id')
    if user_id in active_sessions:
        active_sessions.pop(user_id, None)
        await update.message.reply_text("🛑 Session stopping...")
    else:
        await update.message.reply_text("No active session.")

if __name__ == '__main__':
    print("🚀 SmartTikTok Orchestrator Bot is INITIALIZING...")
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        print("❌ CRITICAL ERROR: TELEGRAM_BOT_TOKEN is missing from environment variables!")
        sys.exit(1)
        
    try:
        app = ApplicationBuilder().token(token).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("pair", pair))
        app.add_handler(CommandHandler("engage", engage))
        app.add_handler(CommandHandler("stop", stop))
        
        print("🤖 Bot status: ONLINE. Listening for commands...")
        app.run_polling()
    except Exception as e:
        print(f"❌ BOT STARTUP FAILED: {e}")
