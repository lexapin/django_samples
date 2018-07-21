from django.test import TestCase

# Create your tests here.
# Тестирование представлений
# - все представления требуют login_required (тестирование с анонимным пользователем и аутентифицированным)
#   - представление interview/test/<test_id>
#   - представление interview/<interview_id>/question
#   - представление interview/<interview_id>/report
# - представление interview/test/<test_id>
#   - если тест не задан в базе данных -> 404
#   - если тест завершен -> redirect(report)
#   - если тест не завершен -> redirect(question)
# - представление interview/<interview_id>/question
#   - интервью отсутствует в базе данных
#   - интервью есть в базе данных - получениие вопроса
#   - интервью - после последнего вопроса (опрос завершен) перенаправление на report
# - представление interview/<interview_id>/report
#   - если интервью не закончено -> redirect(question)
#   - если интервью закончено - отображение результатов
#   - если интервью отсутствует в базе данных -> 404