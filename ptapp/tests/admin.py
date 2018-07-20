from django.contrib import admin
from django import forms
import nested_admin
from .models import TestGroup, TestUnit, Question, Answer

# Register your models here.

class AnswerFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        question_count = 0
        right_count = 0
        for form in self.forms:
            data = form.cleaned_data
            if not data: continue
            if data['DELETE']: continue
            question_count+=1
            if data.get('right'):
                right_count+=1
        print(question_count, right_count)
        if question_count==0 and right_count==0:
            return
        if question_count < 2:
            raise forms.ValidationError('Число вариантов ответов должно быть больше одного.')
        if right_count==0:
            raise forms.ValidationError('У вопроса должен быть хотя бы один правильный ответ.')
        if right_count==question_count:
            raise forms.ValidationError('У вопроса теста не могут все ответы быть верными.')


class AnswerInline(nested_admin.NestedTabularInline):
    model = Answer
    formset = AnswerFormset
    extra = 4


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = "__all__"

    def clean(self):
        print(self.cleaned_data)
        if False:
            raise forms.ValidationError('Error')
        return self.cleaned_data


class QuestionAdmin(nested_admin.NestedModelAdmin):
    form = QuestionForm
    inlines = [AnswerInline]


class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    inlines = [AnswerInline]
    extra = 4


class TestUnitAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(TestUnit, TestUnitAdmin)
admin.site.register(TestGroup)