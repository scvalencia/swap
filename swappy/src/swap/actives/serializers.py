from rest_framework import serializers

from .models import Active


class ActiveSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Active