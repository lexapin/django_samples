from django.contrib import admin
import nested_admin
from .models import TestGroup, TestUnit, Question, Answer

# Register your models here.


class AnswerInline(nested_admin.NestedTabularInline):
    model = Answer
    extra = 4


class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    inlines = [AnswerInline]
    extra = 4


class TestUnitAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInline]


admin.site.register(TestUnit, TestUnitAdmin)
admin.site.register(TestGroup)