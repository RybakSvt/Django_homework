from django.contrib import admin
from .models import Category, Task, SubTask


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_per_page = 20


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'deadline', 'created_at']
    list_filter = ['status', 'categories', 'created_at']
    search_fields = ['title', 'description']
    filter_horizontal = ['categories']
    date_hierarchy = 'created_at'
    list_per_page = 20

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'status')
        }),
        ('Категории', {
            'fields': ('categories',)
        }),
        ('Даты', {
            'fields': ('deadline', 'created_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ['created_at']


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'task', 'status', 'deadline', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'description']
    raw_id_fields = ['task']
    date_hierarchy = 'created_at'
    list_per_page = 20

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'task', 'status')
        }),
        ('Даты', {
            'fields': ('deadline', 'created_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ['created_at']



