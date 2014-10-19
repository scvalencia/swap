from .models import Passive

class PassiveSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Passive