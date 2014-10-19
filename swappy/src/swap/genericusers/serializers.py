from .models import GenericUser

class GenericUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GenericUser