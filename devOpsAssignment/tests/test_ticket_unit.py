import pytest
from model_bakery import baker

from users.models import User


@pytest.fixture
def luser(db):
    return baker.make('users.User', role=User.Role.USER)

@pytest.fixture
def muser(db):
    return baker.make('users.User', role=User.Role.MANAGER)

@pytest.fixture
def uticket(luser):
    return baker.make('tickets.Ticket', submitted_by=luser)

@pytest.fixture
def mticket(muser):
    return baker.make('tickets.Ticket', submitted_by=muser)

@pytest.fixture
def auth_client(client, luser):
    client.force_login(luser)
    return client

@pytest.fixture
def mauth_client(client, muser):
    client.force_login(muser)
    return client

@pytest.mark.django_db
def test_user_cannot_access_manager_ticket(auth_client, mticket):
    response = auth_client.get(f'/tickets/{mticket.pk}/')
    assert response.status_code == 404

@pytest.mark.django_db
def test_muser_can_access_manager_ticket(mauth_client, uticket):
    response = mauth_client.get(f'/tickets/{uticket.pk}/')
    print(response.status_code)
    assert response.status_code == 200

