from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def register_user(serializer):
    """Register a new user"""
    if serializer.is_valid():
        user = serializer.save()
        return user, None
    return None, serializer.errors


def login_user(username, password):
    """Authenticate user and return JWT tokens"""
    user = User.objects.filter(username=username).first()
    if user and user.check_password(password):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }, None
    return None, {"error": "Invalid credentials"}
