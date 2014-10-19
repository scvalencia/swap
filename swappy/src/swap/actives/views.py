from django.shortcuts import render
from rest_framework import viewsets

from .models import Active
from .serializers import ActiveSerializer


class ActiveViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows rents to be viewed or edited.
    """
    queryset = Active.objects.all()
    serializer_class = ActiveSerializer