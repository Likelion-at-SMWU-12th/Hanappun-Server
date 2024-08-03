from rest_framework.viewsets import ModelViewSet

from .serializers import ClinicSerializer, DoctorSerializer
from .models import Clinic, Doctor

# Create your views here.

# minseo : 한의원 CRUD 뷰셋
class ClinicViewSet(ModelViewSet):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer

# minseo : 의료진 CRUD 뷰셋
class DoctorViewSet(ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer