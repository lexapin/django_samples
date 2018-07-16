from django.contrib import admin
from .models import TestGroup, TestUnit, Question, Answer

# Register your models here.

admin.site.register(TestGroup)
admin.site.register(TestUnit)
admin.site.register(Question)
admin.site.register(Answer)