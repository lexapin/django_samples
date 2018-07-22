from django.contrib import admin
from django import forms
import nested_admin
from .models import TestGroup, TestUnit, Question, Answer

# Register your models here.
# Модификация и регистрация форм для административного интерфейса
# - Форма ввода группы для тестов
# - Форма ввода теста с верификацией вариантов ответов

class AnswerFormset(forms.models.BaseInlineFormSet):
    """
    Форма для ввода нескольких вариантов ответов сразу
    Реализация формы стандартная
    Остается только проверка заполненных данных
    """
    def clean(self):
        """
        Проверяет введенные варианты ответов
        Для этого использует два счетчика:
        - question qount - общее число вариантов ответов на вопрос
        - right_count - число правильных ответов на вопрос
        Игнорируются удаляемые записи и вопросы без вариантов ответов
        Генерируются исключения если:
        - число вариантов ответов меньше двух
        - нет правильных ответов
        - все варианты ответов верные
        """
        question_count = 0
        right_count = 0
        for form in self.forms:
            data = form.cleaned_data
            if not data or data.get('DELETE'): continue
            question_count+=1
            if data.get('right'):
                right_count+=1
        if question_count==0 and right_count==0:
            raise forms.ValidationError('Вопрос должен содержать ответы.')
        if question_count < 2:
            raise forms.ValidationError('Число вариантов ответов должно быть больше одного.')
        if right_count==0:
            raise forms.ValidationError('У вопроса должен быть хотя бы один правильный ответ.')
        if right_count==question_count:
            raise forms.ValidationError('У вопроса теста не могут все ответы быть верными.')


class AnswerInline(nested_admin.NestedTabularInline):
    """
    Модель подформы ОТВЕТ
    """
    model = Answer
    formset = AnswerFormset
    extra = 0


class QuestionForm(forms.ModelForm):
    """
    Модель формы для модели ВОПРОС
    """
    class Meta:
        model = Question
        fields = "__all__"


class QuestionAdmin(nested_admin.NestedModelAdmin):
    """
    Административная форма модели ВОПРОС
    """
    form = QuestionForm
    inlines = [AnswerInline]


class QuestionInline(nested_admin.NestedStackedInline):
    """
    Вложенная форма ВОПРОС для формы TestUnit
    """
    model = Question
    inlines = [AnswerInline]
    extra = 0


class TestUnitAdmin(nested_admin.NestedModelAdmin):
    """
    Административная форма модели ТЕСТ
    """
    inlines = [QuestionInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(TestUnit, TestUnitAdmin)
admin.site.register(TestGroup)