from django.contrib import admin
from .models import Category, MenuItem, Report



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'reporter_name', 'grade_section', 'stall', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'grade_section', 'stall')
    search_fields = ('user__username', 'reporter_name', 'concern_text', 'id')
    actions = ['mark_as_resolved', 'mark_as_closed']

    @admin.action(description='Mark selected reports as Resolved')
    def mark_as_resolved(self, request, queryset):
        queryset.update(status='Resolved')

    @admin.action(description='Mark selected reports as Closed')
    def mark_as_closed(self, request, queryset):
        queryset.update(status='Closed')
