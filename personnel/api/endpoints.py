from rest_framework.viewsets import ModelViewSet
from serializers import CadetSerializer
from personnel.models import Cadet

class CadetEndPoint(ModelViewSet):
    queryset = Cadet.objects.all()
    serializer_class = CadetSerializer