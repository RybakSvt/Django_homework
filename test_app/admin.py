from django.contrib import admin, messages
from .models import Category, Task, SubTask


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_deleted', 'deleted_at']
    list_filter = ['is_deleted']  # Добавили фильтр
    search_fields = ['name', ]
    list_per_page = 20

    actions = ['restore_selected']  # Добавили action

    # Метод для показа всех категорий в админке
    def get_queryset(self, request):
        # Используем базовый менеджер, а не наш кастомный
        return Category._base_manager.all()

    # Action для восстановления
    @admin.action(description="Восстановить выбранные категории")
    def restore_selected(self, request, queryset):
        count = queryset.filter(is_deleted=True).count()
        for category in queryset.filter(is_deleted=True):
            category.restore()
        self.message_user(
            request,
            f"Восстановлено {count} категорий",
            messages.SUCCESS
        )

    # Action для полного удаления
    @admin.action(description="Полностью удалить выбранные")
    def hard_delete_selected(self, request, queryset):
        count = queryset.count()
        for category in queryset:
            category.delete(hard=True)
        self.message_user(
            request,
            f"Полностью удалено {count} категорий из БД",
            messages.SUCCESS
        )


class SubTaskInline(admin.TabularInline):
    model =  SubTask
    extra = 1
    fields = ['title', 'description', 'status', 'deadline']
    list_display = ['title', 'status', 'deadline']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    inlines = [SubTaskInline]
    list_display = ['abb_title', 'status', 'deadline', 'created_at']
    list_filter = ['status', 'categories', 'created_at']
    search_fields = ['title', 'description']
    filter_horizontal = ['categories']
    date_hierarchy = 'created_at'
    list_per_page = 20
    ordering = ['-created_at']

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


    @admin.display(description="Наименование задачи")
    def abb_title(self, obj: Task):
        if len(obj.title) > 10:
            return f"{obj.title[:10]}..."
        return obj.title


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'task', 'status', 'deadline', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'description']
    raw_id_fields = ['task']
    date_hierarchy = 'created_at'
    list_per_page = 20
    ordering = ['-created_at']

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


    actions = ['mark_selected_as_done']


    @admin.action(description='Mark selected subtasks as Done')
    def mark_selected_as_done(self, request, queryset):
        to_update = queryset.exclude(status='done')
        updated = to_update.update(status='done')

        self.message_user(
            request,
            f'Successfully marked {updated} subtasks as Done',
            messages.SUCCESS
        )







