from rest_framework import viewsets, status
from rest_framework.response import Response

from ..models.user import User
from ..serializers.user_serializer import UserSerializer
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsAdminUser
from django.conf import settings


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    storage_service = settings.STORAGE_SERVICE

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        instance = self.storage_service.save(instance)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = self.storage_service.update(instance, **serializer.validated_data)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.storage_service.delete(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
