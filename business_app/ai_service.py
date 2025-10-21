import openai
import os
from django.conf import settings
import json

class AIService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def generate_business_analysis(self, quiz_answers):
        """Генерация анализа бизнеса на основе ответов в конструкторе"""
        
        prompt = f"""
        Проанализируй бизнес-профиль на основе следующих ответов:
        
        Этап бизнеса: {quiz_answers.get('stage', 'Не указано')}
        Основная цель: {quiz_answers.get('goal', 'Не указано')}
        Количество сотрудников: {quiz_answers.get('team_size', 'Не указано')}
        Ежемесячный оборот: {quiz_answers.get('turnover', 'Не указано')}
        Сфера бизнеса: {quiz_answers.get('field', 'Не указано')}
        Основной канал привлечения клиентов: {quiz_answers.get('channel', 'Не указано')}
        Основная проблема: {quiz_answers.get('problem', 'Не указано')}
        
        Предоставь детальный анализ в формате JSON с следующими разделами:
        1. Финансовые рекомендации (рекомендации, продукты, обоснование)
        2. Маркетинговые стратегии (рекомендации, каналы, бюджет)
        3. Операционные улучшения (процессы, автоматизация, оптимизация)
        4. Оценка рисков (ключевые риски, mitigation strategies)
        5. План развития (краткосрочные и долгосрочные цели)
        
        Верни только JSON без дополнительного текста.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Ты бизнес-консультант Альфа-Банка с опытом 15 лет. Анализируй бизнес и давай конкретные рекомендации."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            analysis = response.choices[0].message.content
            return json.loads(analysis)
            
        except Exception as e:
            # Fallback анализ если AI недоступен
            return self.get_fallback_analysis(quiz_answers)
    
    def get_chat_response(self, chat_type, user_message, conversation_history):
        """Генерация ответа в чате"""
        
        system_prompts = {
            'ai-analysis': "Ты ИИ-аналитик Альфа-Банка. Ты проводишь глубокий анализ бизнеса, оцениваешь риски и даешь прогнозы. Будь профессиональным и точным.",
            'manager': "Ты менеджер по проектам Альфа-Банка. Помогаешь с проработкой бизнес-проектов, составлением планов и решением организационных вопросов.",
            'ai-assistant': "Ты ИИ-помощник по организационным вопросам бизнеса. Помогаешь с налогами, отчетностью, наймом и другими операционными вопросами.",
            'accountant': "Ты бухгалтер Альфа-Банка. Специализируешься на налоговой отчетности, финансовом учете и оптимизации налоговой нагрузки."
        }
        
        system_prompt = system_prompts.get(chat_type, "Ты полезный помощник Альфа-Банка.")
        
        # Формируем историю диалога
        messages = [{"role": "system", "content": system_prompt}]
        
        for msg in conversation_history[-6:]:  # Берем последние 6 сообщений
            role = "user" if msg['is_user'] else "assistant"
            messages.append({"role": role, "content": msg['message']})
        
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return "В настоящее время сервис временно недоступен. Пожалуйста, попробуйте позже."
    
    def get_fallback_analysis(self, quiz_answers):
        """Резервный анализ если AI недоступен"""
        return {
            "financial_recommendations": {
                "recommendations": ["Оптимизация налоговой нагрузки", "Создание финансовой подушки"],
                "products": ["Кредитная линия 'Бизнес-Старт'", "Инвестиционный продукт 'Рост'"],
                "reasoning": "На основе вашего этапа бизнеса рекомендуем данные продукты"
            },
            "marketing_strategies": {
                "recommendations": ["Усиление онлайн-присутствия", "Развитие партнерских программ"],
                "channels": ["Социальные сети", "Контекстная реклама"],
                "budget": "15-20% от оборота"
            },
            "operational_improvements": {
                "recommendations": ["Автоматизация рутинных процессов", "Внедрение CRM-системы"],
                "automation": ["Электронный документооборот", "Автоматизация отчетности"],
                "optimization": "Сокращение операционных расходов на 10-15%"
            },
            "risk_assessment": {
                "key_risks": ["Валютные колебания", "Изменения в законодательстве"],
                "mitigation": ["Диверсификация поставщиков", "Создание резервного фонда"]
            },
            "development_plan": {
                "short_term": ["Увеличение клиентской базы на 20%", "Оптимизация процессов"],
                "long_term": ["Выход на новые рынки", "Масштабирование бизнеса"]
            }
        }