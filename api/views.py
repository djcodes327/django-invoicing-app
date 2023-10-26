from django.shortcuts import render
from rest_framework import generics
from invoice.models import Client
from .serializers import ClientSerializer


class ClientListCreateView(generics.ListCreateAPIView):
    """
    List Create API View for client.
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
