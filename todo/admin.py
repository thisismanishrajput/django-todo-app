from django.contrib import admin
from .models import TodoModel

# Register your models here.

@admin.register(TodoModel)
class ModelTodo(admin.ModelAdmin):
    list_display = ['id','title', 'desc','created_by']
