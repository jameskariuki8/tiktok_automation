import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.comments_ai.services import CommentAIService
from django.contrib.auth import get_user_model

User = get_user_model()
admin_user = User.objects.filter(username='admin').first()

if not admin_user:
    print("Admin user not found. Please create one first.")
else:
    file_path = r"C:\Users\JNR Developer\Desktop\tiktok_automation\apps\comments_ai\knowledgebase.txt"
    if os.path.exists(file_path):
        service = CommentAIService(admin_user)
        print(f"Ingesting file: {file_path} for user {admin_user.username}...")
        service.ingest_file(file_path)
        print("Success! The knowledge base is now embedded and ready for RAG.")
    else:
        print(f"File not found: {file_path}")
