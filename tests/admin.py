from django.contrib import admin
from .models import TestCategory, TestItem, TestPanel

@admin.register(TestCategory)
class TestCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class TestItemInline(admin.TabularInline):
    model = TestItem
    extra = 0

@admin.register(TestItem)
class TestItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'sample_type', 'processing_time', 'is_active')
    list_filter = ('category', 'sample_type', 'is_active')
    search_fields = ('name', 'description')

@admin.register(TestPanel)
class TestPanelAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount_percentage', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    filter_horizontal = ('tests',)