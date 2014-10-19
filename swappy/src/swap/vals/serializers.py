from rest_framework import serializers

from .models import Rent, Val


class RentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rent

class ValSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Val