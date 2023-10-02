from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView

from .serializers import ProfileSerializer
from .models import Profile
# Create your views here.


class ProfileRegisterView(CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ProfileUpdateView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    


