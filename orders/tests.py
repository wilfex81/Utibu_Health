from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Medication, Order, Customer, Statement


class UserRegistrationLoginTestCase(APITestCase):
    def setUp(self):
        self.user_data = {
            'username': 'test_user',
            'email': 'test@example.com',
            'password': 'test_password'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_user_registration(self):
        new_user_data = {
            'username': 'new_test_user',
            'email': 'new_test@example.com',
            'password': 'new_test_password'
        }
        response = self.client.post('/api/v1/register/', new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(username='new_test_user').username, 'new_test_user')

    def test_user_login(self):
        data = {
            'username': 'test_user',
            'password': 'test_password'
        }
        response = self.client.post('/api/v1/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('message' in response.data)
        self.assertEqual(response.data['message'], 'Login successful')

    def test_user_logout(self):
        self.client.login(username='test_user', password='test_password')
        response = self.client.post('/api/v1/logout/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class OrderAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='test_password')
        self.customer = Customer.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_order_creation_and_retrieval(self):
        medication = Medication.objects.create(name='Test Med', quantity=5, price=10.00)
        data = {
            'customer': self.customer.id,
            'medications': medication.id,
            'quantity': 1
        }
        response = self.client.post('/api/v1/orders/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_order_update(self):
        medication = Medication.objects.create(name='Test Med', quantity=5, price=10.00)
        order = Order.objects.create(customer=self.customer, medications=medication, quantity=1)
        updated_medication = Medication.objects.create(name='Updated Med', quantity=10, price=20.00)
        data = {
            'customer': self.customer.id,
            'medications': updated_medication.id,
            'quantity': 2
        }
        response = self.client.put(f'/api/v1/orders/{order.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)




    def test_order_deletion(self):
        medication = Medication.objects.create(name='Test Med', quantity=5, price=10.00)
        order = Order.objects.create(customer=self.customer, medications=medication)
        response = self.client.delete(f'/api/v1/orders/{order.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)



class MedicationListCreateAPIViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='test_password')
        self.client.force_authenticate(user=self.user)

    def test_medication_list(self):
        response = self.client.get('/api/v1/medications/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_medication(self):
        data = {'name': 'Test Med', 'quantity': 5, 'price': 10.00, 'description': 'test meds description'}
        response = self.client.post('/api/v1/medications/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Medication.objects.count(), 1)


class MedicationDetailAPIViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='test_password')
        self.medication = Medication.objects.create(name='Test Med', quantity=5, price=10.00, description = 'test meds description')


    def test_get_medication_detail(self):
        response = self.client.get(f'/api/v1/medications/{self.medication.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_medication(self):
        data = {'name': 'Updated Med', 'quantity': 8, 'price': 15.00, 'description': 'update test meds description' }
        response = self.client.put(f'/api/v1/medications/{self.medication.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.medication.refresh_from_db()
        self.assertEqual(self.medication.name, 'Updated Med')
        self.assertEqual(self.medication.quantity, 8)
        self.assertEqual(self.medication.price, 15.00)

    def test_delete_medication(self):
        response = self.client.delete(f'/api/v1/medications/{self.medication.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Medication.objects.filter(id=self.medication.id).exists())


class StatementDetailAPIViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='test_password')
        self.customer = Customer.objects.create(user=self.user)
        self.statement = Statement.objects.create(customer=self.customer, amount_due=100)

    def test_get_statement_detail(self):
        response = self.client.get(f'/api/v1/statement/{self.statement.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
