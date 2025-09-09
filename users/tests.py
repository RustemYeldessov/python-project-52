from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()


class UsersAuthCrudTests(TestCase):
    def setUp(self):
        self.user_password = 'pass12345!'
        self.user = User.objects.create_user(username='john', password=self.user_password)

    def test_users_list_accessible_without_login(self):
        response = self.client.get(reverse('users:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Пользователи')

    def test_register_redirects_to_login(self):
        response = self.client.post(reverse('users:create'), {
            'username': 'mary',
            'password1': 'newstrongpass123',
            'password2': 'newstrongpass123',
        })
        self.assertRedirects(response, reverse('login'))

    def test_login_redirects_to_home(self):
        response = self.client.post(reverse('login'), {
            'username': 'john',
            'password': self.user_password,
        })
        self.assertRedirects(response, reverse('home'))

    def test_update_self_only(self):
        self.client.login(username='john', password=self.user_password)
        response = self.client.post(reverse('users:update', args=[self.user.pk]), {
            'username': 'johnny',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
        })
        self.assertRedirects(response, reverse('users:list'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'johnny')

    def test_delete_self_only(self):
        self.client.login(username='john', password=self.user_password)
        response = self.client.post(reverse('users:delete', args=[self.user.pk]))
        self.assertRedirects(response, reverse('users:list'))
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())


