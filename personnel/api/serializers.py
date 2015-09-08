from rest_framework.serializers import ModelSerializer, RelatedField
from django.contrib.auth.models import User
from personnel.models import Cadet

class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)

class CadetSerializer(ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Cadet
