from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from .services.user_services import register_user, login_user


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        user, errors = register_user(serializer)
        if user:
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        tokens, errors = login_user(username, password)
        if tokens:
            return Response(tokens, status=status.HTTP_200_OK)
        return Response(errors, status=status.HTTP_401_UNAUTHORIZED)
