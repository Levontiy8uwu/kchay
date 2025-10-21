from django.contrib import admin
from .models import Course, Subtopic, UserProgress, QuizResponse, ChatMessage

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']
    search_fields = ['title']

@admin.register(Subtopic)
class SubtopicAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']
    list_filter = ['course']
    search_fields = ['title']
    ordering = ['course', 'order']

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'subtopic', 'completed', 'completed_at']
    list_filter = ['completed', 'subtopic__course']
    search_fields = ['user__username', 'subtopic__title']
    readonly_fields = ['completed_at']

@admin.register(QuizResponse)
class QuizResponseAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at']

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'chat_type', 'is_user', 'timestamp']
    list_filter = ['chat_type', 'is_user', 'timestamp']
    search_fields = ['user__username', 'message']
    readonly_fields = ['timestamp']

# Функция для создания начальных данных
def create_initial_data():
    # Создаем курсы если их нет
    if not Course.objects.exists():
        print("Creating initial data...")
        
        # Курс 1: Основы предпринимательства
        basics_course = Course.objects.create(
            title="Основы предпринимательства",
            description="Фундаментальные знания для начала и развития бизнеса"
        )
        
        Subtopic.objects.create(
            course=basics_course,
            title="Генерация бизнес-идеи",
            content="""
            <div class="learning-objectives">
                <h4><i class="fas fa-bullseye"></i> Цели обучения</h4>
                <ul class="task-list">
                    <li class="task-item">Освоить 5 методов генерации бизнес-идей</li>
                    <li class="task-item">Научиться оценивать потенциал идей по 4 критериям</li>
                    <li class="task-item">Разработать собственную бизнес-идею с учетом рыночных потребностей</li>
                </ul>
            </div>
            
            <div class="case-study">
                <h4>Кейс: Успешная бизнес-идея "Кофе с собой"</h4>
                <p>Рассмотрим историю создания сети кофеен "Кофе с собой". Идея появилась в 2010 году...</p>
            </div>
            """,
            summary="Генерация бизнес-идеи - это первый и один из самых важных этапов создания собственного дела. Успешная идея должна решать конкретную проблему или удовлетворять потребность целевой аудитории.",
            order=1
        )
        
        Subtopic.objects.create(
            course=basics_course,
            title="Разработка бизнес-плана",
            content="""
            <div class="learning-objectives">
                <h4><i class="fas fa-bullseye"></i> Цели обучения</h4>
                <ul class="task-list">
                    <li class="task-item">Освоить структуру бизнес-плана</li>
                    <li class="task-item">Научиться проводить анализ рынка</li>
                    <li class="task-item">Составить финансовый прогноз на 3 года</li>
                </ul>
            </div>
            """,
            summary="Бизнес-план - это документ, который описывает все аспекты будущего предприятия, анализирует проблемы и определяет способы их решения.",
            order=2
        )
        
        # Курс 2: Финансы для бизнеса
        finance_course = Course.objects.create(
            title="Финансы для бизнеса",
            description="Управление финансами, налоговая оптимизация, финансовое планирование"
        )
        
        Subtopic.objects.create(
            course=finance_course,
            title="Основы финансового учета",
            content="<p>Финансовый учет - это система сбора, регистрации и обобщения информации о деятельности организации в денежном выражении.</p>",
            summary="Финансовый учет позволяет отслеживать финансовое состояние бизнеса и принимать обоснованные решения.",
            order=1
        )
        
        # Курс 3: Маркетинг и продажи
        marketing_course = Course.objects.create(
            title="Маркетинг и продажи",
            description="Цифровой маркетинг, стратегии продаж, привлечение клиентов"
        )
        
        Subtopic.objects.create(
            course=marketing_course,
            title="Основы цифрового маркетинга",
            content="<p>Цифровой маркетинг - это продвижение товаров и услуг с использованием цифровых каналов и технологий.</p>",
            summary="Цифровой маркетинг позволяет эффективно привлекать клиентов в современном мире.",
            order=1
        )
        
        print("Initial data created successfully!")

# Вызываем создание начальных данных при загрузке админки
try:
    create_initial_data()
except Exception as e:
    print(f"Error creating initial data: {e}")