from django.contrib import admin
from .models import TestOrder, TestResult, Report

class TestResultInline(admin.TabularInline):
    model = TestResult
    extra = 0

@admin.register(TestOrder)
class TestOrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'patient', 'status', 'payment_status', 'total_amount', 'created_at')
    list_filter = ('status', 'payment_status', 'created_at')
    search_fields = ('order_number', 'patient__first_name', 'patient__last_name')
    date_hierarchy = 'created_at'
    inlines = [TestResultInline]
    filter_horizontal = ('test_items', 'test_panels')

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('test_order', 'test_item', 'result_value', 'is_normal', 'is_verified')
    list_filter = ('is_normal', 'is_verified', 'processed_at')
    search_fields = ('test_order__order_number', 'test_item__name')

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_number', 'test_order', 'status', 'generated_at')
    list_filter = ('status', 'generated_at')
    search_fields = ('report_number', 'test_order__order_number', 'test_order__patient__first_name', 'test_order__patient__last_name')
    date_hierarchy = 'generated_at'