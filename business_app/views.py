from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Course, Subtopic, UserProgress, QuizResponse, ChatMessage
from .ai_service import AIService

def index(request):
    """Главная страница"""
    return render(request, 'index.html')

@login_required
def get_courses(request):
    """Получение данных о курсах"""
    courses = Course.objects.all()
    courses_data = []
    
    for course in courses:
        subtopics = course.subtopic_set.all()
        completed_count = UserProgress.objects.filter(
            user=request.user, 
            subtopic__in=subtopics, 
            completed=True
        ).count()
        
        progress = int((completed_count / subtopics.count()) * 100) if subtopics.count() > 0 else 0
        
        courses_data.append({
            'id': course.id,
            'title': course.title,
            'description': course.description,
            'progress': progress,
            'subtopics': [
                {
                    'id': st.id,
                    'title': st.title,
                    'completed': UserProgress.objects.filter(
                        user=request.user, 
                        subtopic=st, 
                        completed=True
                    ).exists()
                }
                for st in subtopics
            ]
        })
    
    return JsonResponse({'courses': courses_data})

@login_required
def get_subtopic_content(request, subtopic_id):
    """Получение контента подтемы"""
    try:
        subtopic = Subtopic.objects.get(id=subtopic_id)
        return JsonResponse({
            'title': subtopic.title,
            'content': subtopic.content,
            'video_url': subtopic.video_url,
            'summary': subtopic.summary
        })
    except Subtopic.DoesNotExist:
        return JsonResponse({'error': 'Subtopic not found'}, status=404)

@login_required
@csrf_exempt
def mark_completed(request):
    """Отметка подтемы как завершенной"""
    if request.method == 'POST':
        data = json.loads(request.body)
        subtopic_id = data.get('subtopic_id')
        
        try:
            subtopic = Subtopic.objects.get(id=subtopic_id)
            progress, created = UserProgress.objects.get_or_create(
                user=request.user,
                subtopic=subtopic
            )
            progress.completed = True
            progress.save()
            
            return JsonResponse({'success': True})
        except Subtopic.DoesNotExist:
            return JsonResponse({'error': 'Subtopic not found'}, status=404)
    
    return JsonResponse({'error': 'Invalid method'}, status=400)

@login_required
@csrf_exempt
def submit_quiz(request):
    """Обработка ответов конструктора"""
    if request.method == 'POST':
        data = json.loads(request.body)
        answers = data.get('answers', {})
        
        # Сохраняем ответы
        quiz_response = QuizResponse.objects.create(
            user=request.user,
            answers=answers
        )
        
        # Генерируем AI анализ
        ai_service = AIService()
        analysis = ai_service.generate_business_analysis(answers)
        
        return JsonResponse({
            'success': True,
            'analysis': analysis,
            'response_id': quiz_response.id
        })
    
    return JsonResponse({'error': 'Invalid method'}, status=400)

@login_required
@csrf_exempt
def chat_message(request):
    """Обработка сообщений в чате"""
    if request.method == 'POST':
        data = json.loads(request.body)
        chat_type = data.get('chat_type')
        message = data.get('message')
        
        # Сохраняем сообщение пользователя
        user_msg = ChatMessage.objects.create(
            user=request.user,
            chat_type=chat_type,
            message=message,
            is_user=True
        )
        
        # Получаем историю диалога
        conversation_history = list(ChatMessage.objects.filter(
            user=request.user,
            chat_type=chat_type
        ).order_by('timestamp').values('message', 'is_user'))
        
        # Генерируем ответ AI
        ai_service = AIService()
        ai_response = ai_service.get_chat_response(chat_type, message, conversation_history)
        
        # Сохраняем ответ AI
        ai_msg = ChatMessage.objects.create(
            user=request.user,
            chat_type=chat_type,
            message=ai_response,
            is_user=False
        )
        
        return JsonResponse({
            'success': True,
            'response': ai_response,
            'message_id': ai_msg.id
        })
    
    return JsonResponse({'error': 'Invalid method'}, status=400)

@login_required
def get_chat_history(request, chat_type):
    """Получение истории чата"""
    messages = ChatMessage.objects.filter(
        user=request.user,
        chat_type=chat_type
    ).order_by('timestamp')
    
    messages_data = [
        {
            'message': msg.message,
            'is_user': msg.is_user,
            'timestamp': msg.timestamp.isoformat()
        }
        for msg in messages
    ]
    
    return JsonResponse({'messages': messages_data})