import pytest
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.urls import reverse

from task_manager.tasks.models import Task
from .models import Status

User = get_user_model()


@pytest.mark.django_db
class TestStatusCRUD:
    @pytest.fixture
    def logged_client(self, client):
        User.objects.create_user(username='user1', password='testpass123')
        client.login(username='user1', password='testpass123')
        return client

    # ---------- CREATE ----------
    def test_create_status_get_requires_login(self, client):
        url = reverse('status_create')
        response = client.get(url)
        assert response.status_code == 302
        assert reverse('login') in response.url

    def test_create_status_get(self, logged_client):
        url = reverse('status_create')
        response = logged_client.get(url)
        assert response.status_code == 200
        assert "Создать статус" in response.content.decode()

    def test_create_status_post(self, logged_client):
        url = reverse('status_create')
        response = logged_client.post(url, {'name': 'Новый'})
        assert response.status_code == 302
        assert Status.objects.filter(name='Новый').exists()

    # ---------- UPDATE ----------
    def test_update_status_get(self, logged_client):
        status = Status.objects.create(name='Старый')
        url = reverse('status_update', args=[status.pk])
        response = logged_client.get(url)
        assert response.status_code == 200
        assert "Редактировать статус" in response.content.decode()

    def test_update_status_post(self, logged_client):
        status = Status.objects.create(name='Старый')
        url = reverse('status_update', args=[status.pk])
        response = logged_client.post(url, {'name': 'Обновленный'})
        assert response.status_code == 302
        status.refresh_from_db()
        assert status.name == 'Обновленный'

    # ---------- DELETE ----------
    def test_delete_status_get(self, logged_client):
        status = Status.objects.create(name='Удалить')
        url = reverse('status_delete', args=[status.pk])
        response = logged_client.get(url)
        assert response.status_code == 200
        assert "Удалить статус" in response.content.decode()

    def test_delete_status_post(self, logged_client):
        status = Status.objects.create(name='Удалить')
        url = reverse('status_delete', args=[status.pk])
        response = logged_client.post(url)
        assert response.status_code == 302
        assert not Status.objects.filter(pk=status.pk).exists()

    def test_cannot_delete_status_in_use(self, logged_client):
        status = Status.objects.create(name='В работе')
        author = User.objects.get(username='user1')
        Task.objects.create(
            name='Test task',
            status=status,
            author=author
        )

        url = reverse('status_delete', args=[status.pk])
        response = logged_client.post(url)

        # статус не удаляется
        assert Status.objects.filter(pk=status.pk).exists()

        # и есть флеш-сообщение
        messages = list(get_messages(response.wsgi_request))
        assert any("невозможно удалить" in str(m) for m in messages)

    # ---------- LIST ----------
    def test_status_list_requires_login(self, client):
        url = reverse('statuses_index')
        response = client.get(url)
        assert response.status_code == 302

    def test_status_list_get(self, logged_client):
        Status.objects.create(name='Открыт')
        url = reverse('statuses_index')
        response = logged_client.get(url)
        assert response.status_code == 200
        assert "Открыт" in response.content.decode()