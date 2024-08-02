from rest_framework.viewsets import ModelViewSet

from .serializers import ClinicSerializer
from .models import Clinic

# Create your views here.

# minseo : 한의원 CRUD 뷰셋
class ClinicViewSet(ModelViewSet):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer
