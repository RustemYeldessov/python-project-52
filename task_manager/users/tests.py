import pytest
from django.contrib.messages import get_messages
from django.urls import reverse

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


@pytest.fixture
def users(db, django_user_model):
    users = []
    for i in range(1, 4):
        user = django_user_model.objects.create_user(
            username=f"user{i}",
            password="testpass123",
            first_name=f"First{i}",
            last_name=f"Last{i}",
        )
        users.append(user)
    return users


def test_user_registration(client, django_user_model):
    initial_users = django_user_model.objects.count()

    url = reverse("users_create")
    data = {
        "username": "newuser",
        "password1": "newpass123",
        "password2": "newpass123",
        "first_name": "New",
        "last_name": "User",
    }
    response = client.post(url, data)

    assert response.status_code == 302
    assert django_user_model.objects.count() == initial_users + 1
    assert django_user_model.objects.filter(username="newuser").exists()

    messages = [str(m).lower() for m in get_messages(response.wsgi_request)]
    assert any("успешно" in m for m in messages)


def test_user_update_authenticated(client, users):
    user1 = users[0]
    client.login(username="user1", password="testpass123")

    url = reverse("users_update", kwargs={"pk": user1.pk})
    response = client.post(
        url,
        {
            "username": "user1",
            "first_name": "Updated",
            "last_name": "User",
            "password1": "newpass123",
            "password2": "newpass123",
        },
    )

    assert response.status_code == 302
    user1.refresh_from_db()
    assert user1.first_name == "Updated"
    assert user1.check_password("newpass123")


def test_user_update_unauthenticated(client, users):
    user1 = users[0]
    url = reverse("users_update", kwargs={"pk": user1.pk})
    response = client.post(url)

    login_url = reverse("login")
    expected_redirect = f"{login_url}?next={url}"
    assert response.url == expected_redirect

    messages = [str(m).lower() for m in get_messages(response.wsgi_request)]
    assert any("не авторизованы" in m for m in messages)


def test_cannot_update_other_user(client, users):
    user1, user2, _ = users
    client.login(username="user2", password="testpass123")

    url = reverse("users_update", kwargs={"pk": user1.pk})
    response = client.post(url, {"username": "hacker"})

    assert response.status_code == 302
    user1.refresh_from_db()
    assert user1.username != "hacker"


def test_cannot_delete_user_with_tasks(client, users):
    user1 = users[0]
    status = Status.objects.create(name="В работе")
    Task.objects.create(name="Test task", status=status, author=user1)

    client.login(username="user1", password="testpass123")
    client.post(reverse("users_delete", args=[user1.pk]))

    assert user1.__class__.objects.filter(pk=user1.pk).exists()


def test_can_delete_user_without_tasks(client, users):
    user2 = users[1]
    client.login(username="user2", password="testpass123")

    response = client.post(reverse("users_delete", args=[user2.pk]))
    assert response.status_code == 302
    assert not user2.__class__.objects.filter(pk=user2.pk).exists()