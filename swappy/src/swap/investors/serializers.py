from .models import Investor

class InvestorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Investor