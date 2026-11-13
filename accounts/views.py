from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .permissions import UserRecordPermission
from .serializers import UserSerializer, PersonalDataSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [UserRecordPermission]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.is_staff:
            return User.objects.all().order_by("id")
        if user.is_authenticated:
            return User.objects.filter(pk=user.pk)
        return User.objects.none()

class PersonalDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Serializer de lectura explícito; no incluye password ni password hash.
        return Response(PersonalDataSerializer(request.user).data)
