from django.contrib import admin

from .models import Interview, Reply, UserAnswer

# Register your models here.

admin.site.register(Interview)
admin.site.register(Reply)
admin.site.register(UserAnswer)