import pytest
import datetime
from rest_framework.reverse import reverse

from user_app.models import User


@pytest.mark.django_db
def test_user_create():
    date = datetime.date.today()
    User.objects.create(name='John', email='user@email.com', password='password', birth_date=date.replace(year=2002))
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_view_non_auth(client):
    url = reverse('user-list')
    response = client.get(url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_view_auth(client):
    date = datetime.date.today()
    User.objects.create(name='John', email='user@email.com', password='password', birth_date=date.replace(year=2002))
    url = '/auth/'
    client.login(
        username='user@email.com', passwd='password'
    )
    response = client.get(url)
    assert response.status_code == 200