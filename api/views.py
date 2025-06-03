from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from accounts.models import User
from patients.models import Patient, MedicalHistory
from tests.models import TestCategory, TestItem, TestPanel
from reports.models import TestOrder, TestResult, Report
from .serializers import (
    UserSerializer, UserCreateSerializer,
    PatientSerializer, MedicalHistorySerializer,
    TestCategorySerializer, TestItemSerializer, TestPanelSerializer,
    TestOrderSerializer, TestResultSerializer, ReportSerializer
)
from .permissions import IsAdminOrReadOnly, IsAdminOrLabTechnician

# User ViewSets
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['email', 'first_name', 'last_name']
    filterset_fields = ['role', 'is_active']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

# Patient ViewSets
class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['first_name', 'last_name', 'phone_number', 'email']
    filterset_fields = ['gender', 'blood_group']
    
    @action(detail=True, methods=['get'])
    def medical_history(self, request, pk=None):
        patient = self.get_object()
        medical_histories = patient.medical_histories.all()
        serializer = MedicalHistorySerializer(medical_histories, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def test_orders(self, request, pk=None):
        patient = self.get_object()
        test_orders = patient.test_orders.all()
        serializer = TestOrderSerializer(test_orders, many=True)
        return Response(serializer.data)

class MedicalHistoryViewSet(viewsets.ModelViewSet):
    queryset = MedicalHistory.objects.all()
    serializer_class = MedicalHistorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['patient', 'date']

# Test ViewSets
class TestCategoryViewSet(viewsets.ModelViewSet):
    queryset = TestCategory.objects.all()
    serializer_class = TestCategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    
    @action(detail=True, methods=['get'])
    def test_items(self, request, pk=None):
        category = self.get_object()
        test_items = category.test_items.all()
        serializer = TestItemSerializer(test_items, many=True)
        return Response(serializer.data)

class TestItemViewSet(viewsets.ModelViewSet):
    queryset = TestItem.objects.all()
    serializer_class = TestItemSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'description']
    filterset_fields = ['category', 'sample_type', 'is_active']

class TestPanelViewSet(viewsets.ModelViewSet):
    queryset = TestPanel.objects.all()
    serializer_class = TestPanelSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'description']
    filterset_fields = ['is_active']

# Report ViewSets
class TestOrderViewSet(viewsets.ModelViewSet):
    queryset = TestOrder.objects.all()
    serializer_class = TestOrderSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['order_number', 'patient__first_name', 'patient__last_name']
    filterset_fields = ['status', 'payment_status']
    
    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        test_order = self.get_object()
        results = test_order.results.all()
        serializer = TestResultSerializer(results, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_result(self, request, pk=None):
        test_order = self.get_object()
        serializer = TestResultSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(test_order=test_order, processed_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TestResultViewSet(viewsets.ModelViewSet):
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer
    permission_classes = [IsAdminOrLabTechnician]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['test_order', 'is_normal', 'is_verified']
    
    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        test_result = self.get_object()
        test_result.is_verified = True
        test_result.verified_by = request.user
        test_result.save()
        serializer = self.get_serializer(test_result)
        return Response(serializer.data)

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['report_number', 'test_order__order_number']
    filterset_fields = ['status']
    
    @action(detail=True, methods=['post'])
    def finalize(self, request, pk=None):
        report = self.get_object()
        report.status = Report.FINALIZED
        report.finalized_by = request.user
        report.save()
        serializer = self.get_serializer(report)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def deliver(self, request, pk=None):
        report = self.get_object()
        report.status = Report.DELIVERED
        report.save()
        serializer = self.get_serializer(report)
        return Response(serializer.data)