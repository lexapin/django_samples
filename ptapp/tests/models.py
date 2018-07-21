from django.db import models
from django.conf import settings


# Модели приложения Тесты


class TestGroup(models.Model):
    """
    Модель ГРУППА ТЕСТОВ для объединения тестов в наборы
    - name - название группы
    - description - описание группы тестов
    """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return "{name} ({description})".format(name=self.name, description=self.description)


class TestUnit(models.Model):
    """
    Модель ТЕСТ
    name - имя теста
    description - описание теста
    owner - создатель теста (не используется)
    test_group - к какой группе относится тест
    created_at - когда создан тест (не используется)
    updated_at - когда изменялся тест (не использется)
    """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    test_group = models.ForeignKey(TestGroup, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{name} ({description})".format(name=self.name, description=self.description)


class Question(models.Model):
    """
    Модель ВОПРОС
    - text - текст вопроса
    - test_unit - к какому тесту принадлежит
    """
    text = models.TextField(blank=True)
    test_unit = models.ForeignKey(TestUnit, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    @property
    def right_answers(self):
        """
        Возвращает число правильных ответов вопроса
        """
        return [answer for answer in self.answer_set.filter(right=True)]


class Answer(models.Model):
    """
    Модель ОТВЕТ на вопрос
    - name - текст ответа
    - description - комментарий к ответу
    - right - правильный ответ или нет
    - question - к какому вопросу теста принадлжеит
    """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True)
    right = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return "Answer {name} is {right} for {question} ".format(
                        name=self.name,
                        question=self.question,
                        right = 'right' if self.right else 'wrong',
        )
