from django.db import models
from django.utils.translation import gettext_lazy as _

class TestCategory(models.Model):
    """Model for test categories."""
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Test categories'

class TestItem(models.Model):
    """Model for individual test items."""
    
    name = models.CharField(max_length=200)
    category = models.ForeignKey(TestCategory, on_delete=models.CASCADE, related_name='test_items')
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Reference ranges
    normal_range = models.CharField(max_length=100, blank=True, null=True)
    unit = models.CharField(max_length=20, blank=True, null=True)
    
    # Processing information
    sample_type = models.CharField(max_length=100)  # e.g., Blood, Urine, etc.
    processing_time = models.IntegerField(help_text="Processing time in hours")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class TestPanel(models.Model):
    """Model for test panels (groups of tests)."""
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    tests = models.ManyToManyField(TestItem, related_name='panels')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Discount compared to individual tests
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name