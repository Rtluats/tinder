import uuid

import pytest
import datetime
from rest_framework.reverse import reverse

from user_app.models import User


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def test_password():
   return 'strong-test-pass'


@pytest.fixture
def create_user(db, django_user_model, test_password):
   def make_user(**kwargs):
       date = datetime.date.today()
       kwargs['password'] = test_password
       kwargs['name'] = 'John'
       kwargs['birth_date'] = date.replace(year=2002)
       if 'email' not in kwargs:
           kwargs['email'] = str(uuid.uuid4()) + '@gmail.com'
       return django_user_model.objects.create_user(**kwargs)
   return make_user


@pytest.mark.django_db
def test_user_create(create_user):
    date = datetime.date.today()
    create_user()
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_view_non_auth(client):
    url = reverse('user-list')
    response = client.get(url)
    assert response.status_code == 200


# @pytest.mark.django_db
# def test_view_auth(client):
#     date = datetime.date.today()
#     user = User.objects.create(name='John', email='user@email.com', password='password', birth_date=date.replace(year=2002))
#     User.objects.create(name='John2', email='user2@email.com', password='password2', birth_date=date.replace(year=2001)).save()
#     User.objects.create(name='John3', email='user3@email.com', password='password3', birth_date=date.replace(year=2000)).save()
#     user.save()
#     url = "/auth/"
#     client.force_login(user)
#
#     response = client.get(reverse('user-list'))
#
#     assert response.status_code == 200
