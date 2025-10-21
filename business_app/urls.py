from django.urls import path
from . import views

urlpatterns = [
    path('api/courses/', views.get_courses, name='get_courses'),
    path('api/subtopic/<int:subtopic_id>/', views.get_subtopic_content, name='get_subtopic_content'),
    path('api/mark-completed/', views.mark_completed, name='mark_completed'),
    path('api/submit-quiz/', views.submit_quiz, name='submit_quiz'),
    path('api/chat/', views.chat_message, name='chat_message'),
    path('api/chat-history/<str:chat_type>/', views.get_chat_history, name='get_chat_history'),
]