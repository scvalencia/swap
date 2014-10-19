from django.shortcuts import render
from rest_framework import viewsets

from .models import Rent, Val
from .serializers import RentSerializer, ValSerializer


class RentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows rents to be viewed or edited.
    """
    queryset = Rent.objects.all()
    serializer_class = RentSerializer    


class ValViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows vals to be viewed or edited.
    """
    queryset = Val.objects.all()
    serializer_class = ValSerializer