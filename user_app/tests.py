import uuid

import pytest
import datetime

from rest_framework.reverse import reverse

from user_app.models import User, UserGroup
from like_app.models import Like, Dislike


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


@pytest.fixture
def create_groups(db, django_user_model):
    def make_groups(**kwargs):
        default_group = UserGroup.objects.create(
            number_of_allowed_swipes=20,
            allowed_distance=10_000,
            group_name="стандартная"
        )
        vip_group = UserGroup.objects.create(
            number_of_allowed_swipes=100,
            allowed_distance=25_000,
            group_name="вип"
        )
        premium_group = UserGroup.objects.create(
            number_of_allowed_swipes=-1,
            allowed_distance=-1,
            group_name="премиум"
        )
        return [default_group, vip_group, premium_group]

    return make_groups


@pytest.mark.django_db
def test_user_create(create_user):
    create_user()
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_view(client):
    url = reverse('user-list')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_view_get_list(client, create_user):
    user = create_user()
    create_user()
    create_user()

    client.force_login(user)

    response = client.get(reverse('user-list'))

    assert len(response.data['results']) == 3


@pytest.mark.django_db
def test_view_get_by_distance(api_client, create_user, create_groups):
    groups = create_groups()
    user1 = create_user()
    user2 = create_user()
    user3 = create_user()
    user1.group = groups[0]
    user2.group = groups[1]
    user3.group = groups[2]
    user3.distance_look = -1
    user1.save()
    user2.save()
    user3.save()

    api_client.force_login(user3)

    url = reverse('user-list')

    data = {
        'pk': user3.pk,
        'get_by_distance': True
    }

    response = api_client.get(url, data=data)

    assert len(response.data) == 2


@pytest.mark.django_db
def test_view_get_users_for_chat(api_client, create_user, create_groups):
    user1 = create_user()
    user2 = create_user()
    user3 = create_user()

    Like.objects.create(user1_like_key=user1, user2_like_key=user3, user1_like=True, user2_like=True)
    Dislike.objects.create(user1_dislike_key=user2, user2_like_key=user3)

    api_client.force_login(user3)

    url = reverse('user-list')

    data = {
        'pk': user3.pk,
        'get_users_for_chat': True
    }

    response = api_client.get(url, data=data)

    assert len(response.data) == 1
