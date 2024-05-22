from django.test import TestCase ,Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Record
from .forms import CreateUserForm, LoginForm, AddRecord, UpdateRecord

class HomeViewTests(TestCase):
    def test_home_view_status_code(self):
        response = self.client.get(reverse(''))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'webapp/index.html')


class RegisterViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')

    def test_register_view_status_code(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'webapp/register.html')

    def test_register_form_submission(self):
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'password1': 'Testpass123',
            'password2': 'Testpass123',
            'email': 'testuser@example.com'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(get_user_model().objects.filter(username='testuser').exists())


class CustomLoginViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='Testpass123',
            email='testuser@example.com'
        )

    def test_login_view_status_code(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'webapp/login.html')

    def test_login_form_submission(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'Testpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))


class DashboardViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.dashboard_url = reverse('dashboard')
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='Testpass123',
            email='testuser@example.com'
        )
        self.client.login(username='testuser', password='Testpass123')

    def test_dashboard_view_status_code(self):
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'webapp/dashboard.html')

    def test_dashboard_view_context_data(self):
        Record.objects.create(
            created_by=self.user, 
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone='1234567890',
            address='123 Main St',
            city='Anytown',
            province='Anystate',
            country='Anycountry'
            )
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['records']), 1)
        self.assertEqual(response.context['records'][0].first_name, 'John')
        self.assertEqual(response.context['records'][0].last_name, 'Doe')


class RecordCreateViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.create_record_url = reverse('create_record')
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='Testpass123',
            email='testuser@example.com'
        )
        self.client.login(username='testuser', password='Testpass123')

    def test_create_record_view_status_code(self):
        response = self.client.get(self.create_record_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'webapp/create_record.html')

    def test_create_record_form_submission(self):
        response = self.client.post(self.create_record_url, {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '1234567890',
            'address': '123 Main St',
            'city': 'Anytown',
            'province': 'Anyprovince',
            'country': 'Anyland'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))
        self.assertTrue(Record.objects.filter(first_name='John', last_name='Doe').exists())


class RecordUpdateViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='Testpass123',
            email='testuser@example.com'
        )
        self.client.login(username='testuser', password='Testpass123')
        self.record = Record.objects.create(
            created_by=self.user,
            first_name='Old',
            last_name='Record',
            email='old@example.com',
            phone='1234567890',
            address='Old Address',
            city='Old City',
            province='Old Province',
            country='Old Country'
        )
        self.update_record_url = reverse('update_record', args=[self.record.id])

    def test_update_record_view_status_code(self):
        response = self.client.get(self.update_record_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'webapp/update_record.html')

    def test_update_record_form_submission(self):
        response = self.client.post(self.update_record_url, {
            'first_name': 'Updated',
            'last_name': 'Record',
            'email': 'updated@example.com',
            'phone': '0987654321',
            'address': 'Updated Address',
            'city': 'Updated City',
            'province': 'Updated Province',
            'country': 'Updated Country'
        })
        self.assertEqual(response.status_code, 302)  
        self.assertRedirects(response, reverse('dashboard'))
        self.record.refresh_from_db()
        self.assertEqual(self.record.first_name, 'Updated')
        self.assertEqual(self.record.last_name, 'Record')
        self.assertEqual(self.record.email, 'updated@example.com')
        self.assertEqual(self.record.phone, '0987654321')
        self.assertEqual(self.record.address, 'Updated Address')
        self.assertEqual(self.record.city, 'Updated City')
        self.assertEqual(self.record.province, 'Updated Province')
        self.assertEqual(self.record.country, 'Updated Country')

class DeleteRecordViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='Testpass123',
            email='testuser@example.com'
        )
        self.client.login(username='testuser', password='Testpass123')
        self.record = Record.objects.create(
            created_by=self.user,
            first_name='Test',
            last_name='Record',
            email='test@example.com',
            phone='1234567890',
            address='Test Address',
            city='Test City',
            province='Test Province',
            country='Test Country'
        )
        self.delete_record_url = reverse('delete_record', args=[self.record.id])

    def test_delete_record_view(self):
        response = self.client.post(self.delete_record_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))
        self.assertFalse(Record.objects.filter(id=self.record.id).exists())
