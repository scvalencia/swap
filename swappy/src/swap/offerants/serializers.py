from .models import Offerant

class OfferantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Offerant