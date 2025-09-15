import pytest
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task

User = get_user_model()


@pytest.mark.django_db
class TestTaskCRUD:
    def setup_method(self):
        self.user1 = User.objects.create_user(
            username='user1', password='pass123'
        )
        self.user2 = User.objects.create_user(
            username='user2', password='pass123'
        )
        self.status = Status.objects.create(name='Новый')

    # ---------- CREATE ----------
    def test_create_task_get_requires_login(self, client):
        url = reverse('task_create')
        response = client.get(url)
        assert response.status_code == 302
        assert reverse('login') in response.url

    def test_create_task_get_authorized(self, client):
        client.login(username='user1', password='pass123')
        url = reverse('task_create')
        response = client.get(url)
        assert response.status_code == 200
        assert "Создать задачу" in response.content.decode()

    def test_create_task_post(self, client):
        client.login(username='user1', password='pass123')
        url = reverse('task_create')
        data = {
            'name': 'Test Task',
            'description': 'Some description',
            'status': self.status.id,
            'executor': self.user2.id,
        }
        response = client.post(url, data)
        assert response.status_code == 302
        assert response.url == reverse('tasks_index')
        task = Task.objects.get()
        assert task.author == self.user1
        assert task.executor == self.user2

    # ---------- UPDATE ----------
    def test_update_task_get(self, client):
        task = Task.objects.create(
            name='Old Task', status=self.status, author=self.user1
        )
        client.login(username='user1', password='pass123')
        url = reverse('task_update', kwargs={'pk': task.id})
        response = client.get(url)
        assert response.status_code == 200
        assert "Редактировать задачу" in response.content.decode()

    def test_update_task_post(self, client):
        task = Task.objects.create(
            name='Old Task', status=self.status, author=self.user1
        )
        client.login(username='user1', password='pass123')
        url = reverse('task_update', kwargs={'pk': task.id})
        response = client.post(url, {
            'name': 'Updated Task',
            'description': 'new desc',
            'status': self.status.id,
            'executor': self.user2.id,
        })
        assert response.status_code == 302
        task.refresh_from_db()
        assert task.name == 'Updated Task'
        assert task.description == 'new desc'

    # ---------- DELETE ----------
    def test_delete_task_by_author(self, client):
        task = Task.objects.create(
            name='Task', status=self.status, author=self.user1
        )
        client.login(username='user1', password='pass123')
        url = reverse('task_delete', kwargs={'pk': task.id})
        response = client.post(url)
        assert response.status_code == 302
        assert Task.objects.count() == 0

    def test_delete_task_by_non_author(self, client):
        task = Task.objects.create(
            name='Task', status=self.status, author=self.user1
        )
        client.login(username='user2', password='pass123')
        url = reverse('task_delete', kwargs={'pk': task.id})
        response = client.post(url)
        assert Task.objects.count() == 1
        messages = list(get_messages(response.wsgi_request))
        assert any("может удалить только её автор" in str(m) for m in messages)

    def test_delete_task_requires_login(self, client):
        task = Task.objects.create(
            name='Task', status=self.status, author=self.user1
        )
        url = reverse('task_delete', kwargs={'pk': task.id})
        response = client.post(url)
        assert response.status_code == 302
        assert reverse('login') in response.url
        assert Task.objects.count() == 1