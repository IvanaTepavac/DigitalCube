from rest_framework import generics, permissions
from rest_framework.response import Response

from .serializers import RegisterSerializer, UserSerializer
from .models import Users
from .permissions import IsOwner


class Registration(generics.GenericAPIView):
    """
    Registering/Creating a User
    """
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"user": UserSerializer(user, context=self.get_serializer_context()).data,
                         "message": "User created successfully. Now perform Login to get your token", })


class UserList(generics.ListAPIView):
    """
    List of all Users
    """
    permission_classes = [permissions.IsAdminUser]
    queryset = Users.objects.all().order_by('-id')
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Editing a User, by id
    """
    permission_classes = [IsOwner | permissions.IsAdminUser]
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
