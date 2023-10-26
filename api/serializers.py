from invoice.models import Client
from rest_framework import serializers


class ClientSerializer(serializers.ModelSerializer):
    """Serializer for Client Model."""

    class Meta:
        model = Client
        exclude = ('clientId',)
