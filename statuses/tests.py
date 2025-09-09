from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Status


User = get_user_model()


class StatusesCrudTests(TestCase):
    def setUp(self):
        self.password = 'pass12345!'
        self.user = User.objects.create_user(username='user', password=self.password)

    def test_requires_login(self):
        # list
        self.assertEqual(self.client.get(reverse('statuses:list')).status_code, 302)
        # create page
        self.assertEqual(self.client.get(reverse('statuses:create')).status_code, 302)

    def test_crud_flow(self):
        self.client.login(username='user', password=self.password)
        # create
        response = self.client.post(reverse('statuses:create'), {'name': 'Новый'})
        self.assertRedirects(response, reverse('statuses:list'))
        status = Status.objects.get(name='Новый')
        # update
        response = self.client.post(reverse('statuses:update', args=[status.pk]), {'name': 'В работе'})
        self.assertRedirects(response, reverse('statuses:list'))
        status.refresh_from_db()
        self.assertEqual(status.name, 'В работе')
        # delete
        response = self.client.post(reverse('statuses:delete', args=[status.pk]))
        self.assertRedirects(response, reverse('statuses:list'))
        self.assertFalse(Status.objects.filter(pk=status.pk).exists())

