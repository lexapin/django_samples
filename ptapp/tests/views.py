from django.shortcuts import get_object_or_404
from django.urls import reverse

# Представления приложения интервью
# Содержит два представления
# - TestGroupListView - Список наборов тестов
#     - отображает список наборов
# - TestUnitListView - Список тестов набора
#     - по идентификатору набора тестов выводит список тестов
# Для отображения списков используется шаблон tests/list_view.html

from .models import TestGroup, TestUnit
from django.views.generic.list import ListView


class TestGroupListView(ListView):
    """
    представление по умолчанию СПИСОК НАБОРОВ ТЕСТОВ
    """
    model = TestGroup
    template_name="tests/list_view.html"

    def get_context_data(self, **kwargs):
        """
        Модификация контекста по умолчанию для шаблона list_view.html
        """
        context = super(TestGroupListView, self).get_context_data(**kwargs)
        context.update({
            'list_name': 'Наборы тестов',
            'button_text': 'Перейти к тестам',
        })
        context['object_list'] = ((obj, reverse('test:group', args=(obj.id,))) for obj in context['object_list'])
        return context


class TestUnitListView(ListView):
    model = TestUnit
    template_name = "tests/list_view.html"

    def get_queryset(self):
        """
        Модификация запроса по умолчанию
        Учет идентификатора группы тестов group_id в запросе тестов
        """
        self.test_group = get_object_or_404(TestGroup, id=self.kwargs['group_id'])
        qs = super(TestUnitListView, self).get_queryset()
        return qs.filter(test_group = self.test_group)
    
    def get_context_data(self, **kwargs):
        """
        Модификация контекста по умолчанию для шаблона list_view.html
        """
        context = super(TestUnitListView, self).get_context_data(**kwargs)
        context.update({
            'list_name': 'Набор тестов по теме \"%s\"' % self.test_group.name,
            'button_text': 'Выполнить тест',
        })
        context['object_list'] = ((obj, reverse('interview:open', args=(obj.id,))) for obj in context['object_list'])
        return context