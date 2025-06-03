from django.db import models
from django.utils.translation import gettext_lazy as _
from patients.models import Patient
from tests.models import TestItem, TestPanel
from accounts.models import User
import uuid

class TestOrder(models.Model):
    """Model for test orders."""
    
    # Order information
    order_number = models.CharField(max_length=20, unique=True, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='test_orders')
    ordered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='ordered_tests')
    
    # Test items and panels
    test_items = models.ManyToManyField(TestItem, blank=True, related_name='orders')
    test_panels = models.ManyToManyField(TestPanel, blank=True, related_name='orders')
    
    # Order status
    PENDING = 'pending'
    PROCESSING = 'processing'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    
    # Payment status
    UNPAID = 'unpaid'
    PARTIALLY_PAID = 'partially_paid'
    PAID = 'paid'
    
    PAYMENT_STATUS_CHOICES = [
        (UNPAID, 'Unpaid'),
        (PARTIALLY_PAID, 'Partially Paid'),
        (PAID, 'Paid'),
    ]
    
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default=UNPAID)
    
    # Financial information
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Expected completion date
    expected_completion_date = models.DateTimeField(blank=True, null=True)
    
    # Notes
    notes = models.TextField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.order_number} - {self.patient}"
    
    class Meta:
        ordering = ['-created_at']

class TestResult(models.Model):
    """Model for test results."""
    
    test_order = models.ForeignKey(TestOrder, on_delete=models.CASCADE, related_name='results')
    test_item = models.ForeignKey(TestItem, on_delete=models.CASCADE)
    
    # Result information
    result_value = models.CharField(max_length=100)
    is_normal = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)
    
    # Processing information
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='processed_results')
    processed_at = models.DateTimeField(auto_now_add=True)
    
    # Verification
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_results')
    verified_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.test_order.order_number} - {self.test_item.name}"

class Report(models.Model):
    """Model for test reports."""
    
    test_order = models.OneToOneField(TestOrder, on_delete=models.CASCADE, related_name='report')
    report_number = models.CharField(max_length=20, unique=True, editable=False)
    
    # Report status
    DRAFT = 'draft'
    FINALIZED = 'finalized'
    DELIVERED = 'delivered'
    
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (FINALIZED, 'Finalized'),
        (DELIVERED, 'Delivered'),
    ]
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=DRAFT)
    
    # Report generation
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='generated_reports')
    generated_at = models.DateTimeField(auto_now_add=True)
    
    # Report finalization
    finalized_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='finalized_reports')
    finalized_at = models.DateTimeField(null=True, blank=True)
    
    # Report delivery
    delivered_at = models.DateTimeField(null=True, blank=True)
    delivery_method = models.CharField(max_length=50, blank=True, null=True)  # e.g., Email, Physical copy, etc.
    
    # PDF report
    pdf_report = models.FileField(upload_to='reports/', blank=True, null=True)
    
    # Additional notes
    notes = models.TextField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.report_number:
            self.report_number = f"REP-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.report_number} - {self.test_order.patient}"
    
    class Meta:
        ordering = ['-generated_at']