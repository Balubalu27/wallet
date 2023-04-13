import pytest
from django.urls import reverse

from crypto.models import Wallet


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


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
@pytest.mark.parametrize(
    'send_from, to, currency, amount, status_code', [
        ('0x4728B952eD162b1DB5efc44fd34f6b78741e9D17', '0x5C7Be6Da7eAd1801CE4Ab8A837499E444f53640a', 'eth', '10', 200),
        ('0x5C7Be6Da7eAd1801CE4Ab8A837499E444f53640a', '0x7c528d80c6C3700EaCAfad5302b42D07eeFa07A7', 'eth', '101', 400),
        ('0x7c528d80c6C3700EaCAfad5302b42D07eeFa07A7', '0x4728B952eD162b1DB5efc44fd34f6b78741e9D17', 'eth', '', 400),
    ]
)
def test_create_transaction(mocker, send_from, to, currency, amount, status_code, wallets, api_client):
    mock_get_account_balance = mocker.patch(
        'crypto.accounts.get_account_balance',
        return_value=100
    )
    data = {
        'send_from': send_from,
        'to': to,
        'currency': currency,
        'amount': amount,
    }
    url = reverse('transactions')
    response = api_client.post(url, data=data)
    assert response.status_code == status_code

    if response.status_code == 200:
        assert "hash" in response.json()
