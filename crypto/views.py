from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from crypto.accounts import create_account, get_account_balance
from crypto.models import Wallet
from crypto.serializers import TransactionSerializer, WalletSerializer


class WalletView(GenericAPIView):
    serializer_class = WalletSerializer
    queryset = Wallet.objects.all()

    @extend_schema(
        operation_id="Get wallets list",
        tags=["Wallets"]
    )
    def get(self, request):
        """Get list of Wallets"""
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    @extend_schema(
        operation_id="Create wallet",
        tags=["Wallets"]
    )
    def post(self, request):
        """Create wallet"""
        serializer: WalletSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        acct = create_account()

        wallet = Wallet.objects.create(
            currency=serializer.validated_data["currency"],
            public_key=acct.address,
            private_key=acct.key
        )
        response_serializer = self.get_serializer(wallet)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class TransactionView(GenericAPIView):
    serializer_class = TransactionSerializer

    @extend_schema(
        operation_id="Create transaction",
        tags=["Transactions"]
    )
    def post(self, request):
        """Create transaction"""
        serializer: TransactionSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sender_wallet = get_object_or_404(Wallet, public_key=serializer.validated_data["send_from"])
        to_wallet = get_object_or_404(Wallet, public_key=serializer.validated_data["to"])

        sender_balance = get_account_balance(sender_wallet.public_key)
        if sender_balance < serializer.validated_data["amount"]:
            raise ValidationError("Low balance for operation")

        # ------------- Some logic -------------
        return Response({"hash": "some hash"})
