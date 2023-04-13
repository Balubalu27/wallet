import pytest
from django.urls import reverse

from crypto.models import Wallet


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def wallets():
    return Wallet.objects.bulk_create(
        (
            Wallet(currency='eth', public_key='0x4728B952eD162b1DB5efc44fd34f6b78741e9D17', private_key='x'),
            Wallet(currency='eth', public_key='0x5C7Be6Da7eAd1801CE4Ab8A837499E444f53640a', private_key='y'),
            Wallet(currency='eth', public_key='0x7c528d80c6C3700EaCAfad5302b42D07eeFa07A7', private_key='z'),
        )
    )


@pytest.mark.django_db
def test_get_wallets(mocker, wallets, api_client):
    mock_get_account_balance = mocker.patch(
        'crypto.accounts.get_account_balance',
        return_value=0
    )
    url = reverse('wallets')
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == len(wallets)


@pytest.mark.django_db
@pytest.mark.parametrize(
    'currency, status_code', [
        ('eth', 201),
        ('rub', 400),
        (1, 400),
        ('', 400),
    ]
)
def test_create_wallet(currency, status_code, api_client):
    url = reverse('wallets')
    data = {
       'currency': currency,
    }
    response = api_client.post(url, data=data)
    assert response.status_code == status_code
