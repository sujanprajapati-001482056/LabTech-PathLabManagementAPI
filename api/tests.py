from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from patients.models import Patient
from tests.models import TestCategory, TestItem
from reports.models import TestOrder
import datetime

class UserTests(APITestCase):
    def setUp(self):
        # Create admin user
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpassword'
        )
        
        # Create regular user
        self.user = User.objects.create_user(
            email='user@example.com',
            password='userpassword',
            role='lab_technician'
        )
    
    def test_create_user(self):
        """
        Ensure we can create a new user object.
        """
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('user-list')
        data = {
            'email': 'newuser@example.com',
            'password': 'newuserpassword',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'receptionist'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(User.objects.get(email='newuser@example.com').role, 'receptionist')

class PatientTests(APITestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_user(
            email='user@example.com',
            password='userpassword'
        )
        
        # Create patient
        self.patient = Patient.objects.create(
            first_name='John',
            last_name='Doe',
            date_of_birth=datetime.date(1990, 1, 1),
            gender='male',
            phone_number='1234567890',
            address='123 Main St'
        )
    
    def test_get_patients(self):
        """
        Ensure we can retrieve patients.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('patient-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_create_patient(self):
        """
        Ensure we can create a new patient.
        """
        self.client.force_authenticate(user=self.user)
        url = reverse('patient-list')
        data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'date_of_birth': '1995-05-15',
            'gender': 'female',
            'phone_number': '9876543210',
            'address': '456 Oak St'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patient.objects.count(), 2)

class TestItemTests(APITestCase):
    def setUp(self):
        # Create admin user
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpassword'
        )
        
        # Create test category
        self.category = TestCategory.objects.create(
            name='Blood Tests',
            description='Tests related to blood analysis'
        )
    
    def test_create_test_item(self):
        """
        Ensure we can create a new test item.
        """
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('testitem-list')
        data = {
            'name': 'Complete Blood Count',
            'category': self.category.id,
            'description': 'Measures several components of blood',
            'price': '50.00',
            'sample_type': 'Blood',
            'processing_time': 2
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TestItem.objects.count(), 1)