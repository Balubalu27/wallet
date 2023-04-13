import pytest

from crypto.serializers import TransactionSerializer, WalletSerializer


@pytest.fixture()
def without_get_account_balance(mocker):
    patcher = mocker.patch('crypto.accounts.get_account_balance', return_value=0)
    patcher.start()
    yield patcher
    patcher.stop()


class TestWalletSerializer:
    def test_valid_serializer(self, without_get_account_balance):
        serializer = WalletSerializer(data={'currency': 'eth'})
        assert serializer.is_valid()
        assert serializer.validated_data == {'currency': 'eth'}
        assert serializer.errors == {}

    def test_invalid_serializer(self, without_get_account_balance):
        serializer = WalletSerializer(data={'currency': 'rub'})
        assert not serializer.is_valid()
        assert serializer.validated_data == {}


class TestTransactionSerializer:
    def test_serializer(self, without_get_account_balance):
        data = {
            'send_from': '0x5C7Be6Da7eAd1801CE4Ab8A837499E444f53640a',
            'to': '0x7c528d80c6C3700EaCAfad5302b42D07eeFa07A7',
            'currency': 'eth',
            'amount': '10',
        }
        serializer = TransactionSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.errors == {}

    @pytest.mark.parametrize(
        'send_from, to, currency, amount, is_valid', [
            ('0x5C7Be6Da7eAd1801CE4Ab8A837499E444f53640a', '0x7c528d80c6C3700EaCAfad5302b42D07eeFa07A7', 'rub', '101',
             False),
            ('0x7c528d80c6C3700EaCAfad5302b42D07eeFa07A7', '0x4728B952eD162b1DB5efc44fd34f6b78741e9D17', 'eth', '',
             False),
        ]
    )
    def test_invalid_serializer(self, send_from, to, currency, amount, is_valid, without_get_account_balance):
        data = {
            'send_from': send_from,
            'to': to,
            'currency': currency,
            'amount': amount,
        }
        serializer = TransactionSerializer(data=data)
        assert not serializer.is_valid()
        assert serializer.validated_data == {}
