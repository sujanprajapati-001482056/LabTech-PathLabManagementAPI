from rest_framework import serializers
from accounts.models import User
from patients.models import Patient, MedicalHistory
from tests.models import TestCategory, TestItem, TestPanel
from reports.models import TestOrder, TestResult, Report

# User Serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'role', 'profile_picture']
        read_only_fields = ['id']

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'role', 'password', 'profile_picture']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

# Patient Serializers
class MedicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistory
        fields = ['id', 'diagnosis', 'treatment', 'date', 'doctor', 'notes']
        read_only_fields = ['id']

class PatientSerializer(serializers.ModelSerializer):
    medical_histories = MedicalHistorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Patient
        fields = [
            'id', 'first_name', 'last_name', 'date_of_birth', 'gender', 
            'email', 'phone_number', 'address', 'blood_group', 'allergies',
            'emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship',
            'registration_date', 'medical_histories'
        ]
        read_only_fields = ['id', 'registration_date']

# Test Serializers
class TestCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCategory
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']

class TestItemSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    
    class Meta:
        model = TestItem
        fields = [
            'id', 'name', 'category', 'category_name', 'description', 'price',
            'normal_range', 'unit', 'sample_type', 'processing_time', 'is_active'
        ]
        read_only_fields = ['id']

class TestPanelSerializer(serializers.ModelSerializer):
    tests = TestItemSerializer(many=True, read_only=True)
    test_ids = serializers.PrimaryKeyRelatedField(
        queryset=TestItem.objects.all(),
        many=True,
        write_only=True,
        source='tests'
    )
    
    class Meta:
        model = TestPanel
        fields = [
            'id', 'name', 'description', 'tests', 'test_ids',
            'price', 'discount_percentage', 'is_active'
        ]
        read_only_fields = ['id']

# Report Serializers
class TestResultSerializer(serializers.ModelSerializer):
    test_name = serializers.ReadOnlyField(source='test_item.name')
    normal_range = serializers.ReadOnlyField(source='test_item.normal_range')
    unit = serializers.ReadOnlyField(source='test_item.unit')
    
    class Meta:
        model = TestResult
        fields = [
            'id', 'test_item', 'test_name', 'result_value', 'is_normal',
            'normal_range', 'unit', 'notes', 'is_verified'
        ]
        read_only_fields = ['id']

class TestOrderSerializer(serializers.ModelSerializer):
    patient_name = serializers.ReadOnlyField(source='patient.__str__')
    test_items_details = TestItemSerializer(source='test_items', many=True, read_only=True)
    test_panels_details = TestPanelSerializer(source='test_panels', many=True, read_only=True)
    
    class Meta:
        model = TestOrder
        fields = [
            'id', 'order_number', 'patient', 'patient_name', 
            'test_items', 'test_items_details',
            'test_panels', 'test_panels_details',
            'status', 'payment_status', 'total_amount', 'discount', 'paid_amount',
            'created_at', 'expected_completion_date', 'notes'
        ]
        read_only_fields = ['id', 'order_number', 'created_at']

class ReportSerializer(serializers.ModelSerializer):
    patient_name = serializers.ReadOnlyField(source='test_order.patient.__str__')
    results = TestResultSerializer(source='test_order.results', many=True, read_only=True)
    
    class Meta:
        model = Report
        fields = [
            'id', 'report_number', 'test_order', 'patient_name',
            'status', 'generated_at', 'finalized_at', 'delivered_at',
            'delivery_method', 'pdf_report', 'notes', 'results'
        ]
        read_only_fields = ['id', 'report_number', 'generated_at']